import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


def test_cadastrar_produto(client):
    response = client.post(
        "/produtos/",
        json={"nome": "Mouse Gamer", "preco": 100.0, "quantidade_estoque": 10},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Mouse Gamer"


def test_venda_sucesso_com_desconto_e_baixa_estoque(client):
    res_prod = client.post(
        "/produtos/",
        json={"nome": "Monitor 24", "preco": 300.0, "quantidade_estoque": 5},
    )
    prod_id = res_prod.json()["id"]

    response_venda = client.post(
        "/vendas/",
        json={"itens": [{"produto_id": prod_id, "quantidade": 1}]},
    )
    
    assert response_venda.status_code == 201
    assert response_venda.json()["valor_total"] == 285.0

    response_produtos = client.get("/produtos/")
    produtos = response_produtos.json()
    assert produtos[0]["quantidade_estoque"] == 4


def test_venda_estoque_insuficiente(client):
    res_prod = client.post(
        "/produtos/",
        json={"nome": "Headset", "preco": 150.0, "quantidade_estoque": 2},
    )
    prod_id = res_prod.json()["id"]

    response = client.post(
        "/vendas/",
        json={"itens": [{"produto_id": prod_id, "quantidade": 5}]},
    )

    assert response.status_code == 400
    assert "Estoque insuficiente" in response.json()["detail"]