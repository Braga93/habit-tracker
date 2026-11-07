def test_register_login_and_me(client) -> None:
    created = client.post(
        "/api/auth/register",
        json={"username": "ana_1", "email": "Ana@Exemplo.com", "password": "12345678"},
    )
    assert created.status_code == 201
    assert created.json()["user"]["email"] == "ana@exemplo.com"

    by_email = client.post("/api/auth/login", json={"username": "ana@exemplo.com", "password": "12345678"})
    assert by_email.status_code == 200

    token = client.post("/api/auth/login", json={"username": "ana_1", "password": "12345678"}).json()["access_token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["username"] == "ana_1"


def test_password_is_not_stored_in_plain_text(client, engine) -> None:
    from sqlmodel import Session, select

    from app.models import User

    client.post("/api/auth/register", json={"username": "zeca", "email": "ze@x.com", "password": "senha-forte"})
    with Session(engine) as session:
        user = session.exec(select(User)).one()
    assert user.password_hash != "senha-forte"
    assert user.password_hash.startswith("$2")


def test_duplicate_and_wrong_password(client, auth) -> None:
    again = client.post("/api/auth/register", json={"username": "braga", "email": "o@x.com", "password": "12345678"})
    assert again.status_code == 409
    wrong = client.post("/api/auth/login", json={"username": "braga", "password": "errada!!"})
    assert wrong.status_code == 401


def test_validation(client) -> None:
    short = client.post("/api/auth/register", json={"username": "ab", "email": "a@b.co", "password": "123"})
    assert short.status_code == 422


def test_protected_routes_require_token(client) -> None:
    assert client.get("/api/habits").status_code == 401
    assert client.get("/api/progress", headers={"Authorization": "Bearer invalido"}).status_code == 401
