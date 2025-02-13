from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db

app = FastAPI(title="API de Empresas e Obrigações Acessórias")

# crud de empresa
@app.post("/empresas/", response_model=schemas.Empresa)
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[schemas.Empresa])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empresas = db.query(models.Empresa).offset(skip).limit(limit).all()
    return empresas

@app.get("/empresas/{empresa_id}", response_model=schemas.Empresa)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@app.put("/empresas/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(empresa_id: int, empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    for key, value in empresa.dict().items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    db.delete(empresa)
    db.commit()
    return {"message": "Empresa deletada com sucesso"}

# crud de obrigacoes
@app.post("/obrigacoes/", response_model=schemas.ObrigacaoAcessoria)
def create_obrigacao(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/", response_model=List[schemas.ObrigacaoAcessoria])
def read_obrigacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    obrigacoes = db.query(models.ObrigacaoAcessoria).offset(skip).limit(limit).all()
    return obrigacoes

@app.get("/obrigacoes/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def read_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return obrigacao

@app.put("/obrigacoes/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def update_obrigacao(obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    
    for key, value in obrigacao.dict().items():
        setattr(db_obrigacao, key, value)
    
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.delete("/obrigacoes/{obrigacao_id}")
def delete_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    
    db.delete(obrigacao)
    db.commit()
    return {"message": "Obrigação deletada com sucesso"}