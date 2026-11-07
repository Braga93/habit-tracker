import httpx

from app.config import Settings


def test_progress_summary(client, auth, habit_payload) -> None:
    habit_id = client.post("/api/habits", json=habit_payload, headers=auth).json()["habit"]["id"]
    client.post(f"/api/habits/{habit_id}/checkins", headers=auth)
    body = client.get("/api/progress", headers=auth).json()
    assert body["streak"] == 1
    assert body["today"] == {"done": 1, "scheduled": 1}
    assert len(body["heatmap"]) == 84
    assert body["heatmap"][-1]["count"] == 1
    assert sum(b["earned"] for b in body["badges"]) == 2
    assert body["recent_xp"][0]["reason"].startswith("Medalha")


def test_insights_and_rule_based_chat(client, auth, habit_payload) -> None:
    client.post("/api/habits", json=habit_payload, headers=auth)
    insights = client.get("/api/coach/insights", headers=auth).json()
    assert insights["ai_enabled"] is False
    assert insights["insights"]

    reply = client.post("/api/coach/chat", json={"message": "Como estou?"}, headers=auth).json()
    assert reply["source"] == "regras"
    assert "nível" in reply["reply"]


def test_chat_falls_back_when_ai_fails(client, auth, settings: Settings, monkeypatch) -> None:
    settings.openai_api_key = "chave-falsa"

    async def failing(*args, **kwargs):
        raise httpx.ConnectError("sem rede")

    monkeypatch.setattr(httpx.AsyncClient, "post", failing)
    reply = client.post("/api/coach/chat", json={"message": "oi"}, headers=auth).json()
    assert reply["source"] == "regras"
    assert reply["notice"]


def test_chat_uses_ai_when_available(client, auth, settings: Settings, monkeypatch) -> None:
    settings.openai_api_key = "chave"

    async def fake_post(self, url, **kwargs):
        assert url.endswith("/chat/completions")
        request = httpx.Request("POST", url)
        return httpx.Response(200, json={"choices": [{"message": {"content": "Resposta da IA"}}]}, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    reply = client.post("/api/coach/chat", json={"message": "oi"}, headers=auth).json()
    assert reply == {"reply": "Resposta da IA", "source": "ia", "notice": None}
