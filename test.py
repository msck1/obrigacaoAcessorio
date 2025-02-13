import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from database import Base
from main import app, get_db
from dotenv import load_dotenv
import pytest
import models

load_dotenv()

TESTE_DB = os.getenv("TESTE_DB")

engine = create_engine(TESTE_DB)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# testes de todos os endpoints da api

@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)
    
@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def empresa_exemplo():
    return {
        "nome": "Empresa Teste",
        "cnpj": "12345678901234",
        "endereco": "Rua Teste, 123",
        "email": "teste@empresa.com",
        "telefone": "11999999999"
    }

@pytest.fixture()
def obrigacao_exemplo():
    return {
        "nome": "Obrigação Teste",
        "periodicidade": "mensal",
        "empresa_id": 1
    }

def test_create_empresa(test_db, client, empresa_exemplo):
    response = client.post("/empresas/", json=empresa_exemplo)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == empresa_exemplo["nome"]
    assert "id" in data
    return data

def test_read_empresas(test_db, client, empresa_exemplo):

    client.post("/empresas/", json=empresa_exemplo)
    
    response = client.get("/empresas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["nome"] == empresa_exemplo["nome"]

def test_read_empresa(test_db, client, empresa_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    
    response = client.get(f"/empresas/{empresa['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == empresa_exemplo["nome"]

def test_read_empresa_not_found(test_db, client):
    response = client.get("/empresas/999")
    assert response.status_code == 404

def test_update_empresa(test_db, client, empresa_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    
    empresa_atualizada = empresa_exemplo.copy()
    empresa_atualizada["nome"] = "Empresa Atualizada"
    
    response = client.put(f"/empresas/{empresa['id']}", json=empresa_atualizada)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Atualizada"

def test_update_empresa_not_found(test_db, client, empresa_exemplo):
    response = client.put("/empresas/999", json=empresa_exemplo)
    assert response.status_code == 404

def test_delete_empresa(test_db, client, empresa_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    
    response = client.delete(f"/empresas/{empresa['id']}")
    assert response.status_code == 200
    
    response = client.get(f"/empresas/{empresa['id']}")
    assert response.status_code == 404

def test_delete_empresa_not_found(test_db, client):
    response = client.delete("/empresas/999")
    assert response.status_code == 404


def test_create_obrigacao(test_db, client, empresa_exemplo, obrigacao_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    obrigacao_exemplo["empresa_id"] = empresa["id"]
    
    response = client.post("/obrigacoes/", json=obrigacao_exemplo)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == obrigacao_exemplo["nome"]
    assert "id" in data
    return data

def test_read_obrigacoes(test_db, client, empresa_exemplo, obrigacao_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    obrigacao_exemplo["empresa_id"] = empresa["id"]
    client.post("/obrigacoes/", json=obrigacao_exemplo)
    
    response = client.get("/obrigacoes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["nome"] == obrigacao_exemplo["nome"]

def test_read_obrigacao(test_db, client, empresa_exemplo, obrigacao_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    obrigacao_exemplo["empresa_id"] = empresa["id"]
    obrigacao = client.post("/obrigacoes/", json=obrigacao_exemplo).json()
    
    response = client.get(f"/obrigacoes/{obrigacao['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == obrigacao_exemplo["nome"]

def test_read_obrigacao_not_found(test_db, client):
    response = client.get("/obrigacoes/999")
    assert response.status_code == 404

def test_update_obrigacao(test_db, client, empresa_exemplo, obrigacao_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    obrigacao_exemplo["empresa_id"] = empresa["id"]
    obrigacao = client.post("/obrigacoes/", json=obrigacao_exemplo).json()
    
    obrigacao_atualizada = obrigacao_exemplo.copy()
    obrigacao_atualizada["nome"] = "Obrigação Atualizada"
    
    response = client.put(f"/obrigacoes/{obrigacao['id']}", json=obrigacao_atualizada)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Obrigação Atualizada"

def test_update_obrigacao_not_found(test_db, client, obrigacao_exemplo):
    response = client.put("/obrigacoes/999", json=obrigacao_exemplo)
    assert response.status_code == 404

def test_delete_obrigacao(test_db, client, empresa_exemplo, obrigacao_exemplo):

    empresa = client.post("/empresas/", json=empresa_exemplo).json()
    obrigacao_exemplo["empresa_id"] = empresa["id"]
    obrigacao = client.post("/obrigacoes/", json=obrigacao_exemplo).json()
    
    response = client.delete(f"/obrigacoes/{obrigacao['id']}")
    assert response.status_code == 200

    response = client.get(f"/obrigacoes/{obrigacao['id']}")
    assert response.status_code == 404

def test_delete_obrigacao_not_found(test_db, client):
    response = client.delete("/obrigacoes/999")
    assert response.status_code == 404
