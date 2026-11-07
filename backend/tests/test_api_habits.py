from datetime import timedelta


def create(client, auth, payload) -> dict:
    response = client.post("/api/habits", json=payload, headers=auth)
    assert response.status_code == 201
    return response.json()


def test_create_habit_unlocks_architect(client, auth, habit_payload) -> None:
    body = create(client, auth, habit_payload)
    assert body["habit"]["xp"] == 20
    assert [b["code"] for b in body["new_badges"]] == ["arquiteto"]
    assert client.get("/api/habits", headers=auth).json()[0]["name"] == "Ler"


def test_check_in_awards_xp_once(client, auth, habit_payload) -> None:
    habit_id = create(client, auth, habit_payload)["habit"]["id"]
    first = client.post(f"/api/habits/{habit_id}/checkins", json={"mood": 4}, headers=auth)
    assert first.status_code == 201
    body = first.json()
    assert body["xp_gained"] == 20
    assert body["habit"]["done_today"] is True
    assert "primeiro_passo" in [b["code"] for b in body["new_badges"]]
    assert body["level"]["total_xp"] == 20 + 25 + 25

    second = client.post(f"/api/habits/{habit_id}/checkins", headers=auth)
    assert second.status_code == 409


def test_undo_returns_xp(client, auth, habit_payload) -> None:
    habit_id = create(client, auth, habit_payload)["habit"]["id"]
    xp_before = client.get("/api/progress", headers=auth).json()["level"]["total_xp"]
    client.post(f"/api/habits/{habit_id}/checkins", headers=auth)
    undone = client.delete(f"/api/habits/{habit_id}/checkins/today", headers=auth)
    assert undone.status_code == 200
    assert undone.json()["done_today"] is False
    xp_after = client.get("/api/progress", headers=auth).json()["level"]["total_xp"]
    assert xp_after == xp_before + 25
    assert client.delete(f"/api/habits/{habit_id}/checkins/today", headers=auth).status_code == 404


def test_streak_bonus_and_badges_over_a_week(client, auth, habit_payload, clock) -> None:
    habit_id = create(client, auth, habit_payload)["habit"]["id"]
    start = clock.today
    last = None
    for offset in range(7):
        clock.today = start + timedelta(days=offset)
        last = client.post(f"/api/habits/{habit_id}/checkins", headers=auth).json()
    assert last["streak"] == 7
    assert last["streak_bonus"] == 50
    assert "semana_de_ferro" in [b["code"] for b in last["new_badges"]]
    assert last["habit"]["streak"] == 7
    assert last["habit"]["completion_rate"] == 1.0


def test_update_and_archive(client, auth, habit_payload) -> None:
    habit_id = create(client, auth, habit_payload)["habit"]["id"]
    updated = client.patch(f"/api/habits/{habit_id}", json={"difficulty": "hard", "weekdays": [0, 2]}, headers=auth)
    assert updated.json()["xp"] == 30
    assert updated.json()["weekdays"] == [0, 2]
    assert client.delete(f"/api/habits/{habit_id}", headers=auth).status_code == 204
    assert client.get("/api/habits", headers=auth).json() == []


def test_cannot_touch_other_users_habit(client, auth, habit_payload) -> None:
    habit_id = create(client, auth, habit_payload)["habit"]["id"]
    other = client.post("/api/auth/register", json={"username": "outro", "email": "o@x.com", "password": "12345678"})
    headers = {"Authorization": f"Bearer {other.json()['access_token']}"}
    assert client.post(f"/api/habits/{habit_id}/checkins", headers=headers).status_code == 404
    assert client.patch(f"/api/habits/{habit_id}", json={"name": "x"}, headers=headers).status_code == 404


def test_invalid_weekday_is_rejected(client, auth, habit_payload) -> None:
    habit_payload["weekdays"] = [7]
    assert client.post("/api/habits", json=habit_payload, headers=auth).status_code == 422
