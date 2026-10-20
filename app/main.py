from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, get_db
from app import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestão de Vendas e Estoque",
    description="Sistema para controle de produtos, baixa automática de estoque e cálculo de descontos.",
    version="1.0.0"
)

@app.post("/produtos/", response_model=schemas.ProdutoResponse, status_code=201)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db, produto)

@app.get("/produtos/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.listar_produtos(db)

# VERIFIQUE SE ESTA ROTA ABAIXO ESTÁ PRESENTE NO SEU main.py:
@app.post("/vendas/", response_model=schemas.VendaResponse, status_code=201)
def realizar_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    return crud.processar_venda(db, venda)