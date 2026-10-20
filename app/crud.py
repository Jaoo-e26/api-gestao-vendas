from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

def criar_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def listar_produtos(db: Session):
    return db.query(models.Produto).all()

def processar_venda(db: Session, venda_data: schemas.VendaCreate):
    valor_total = 0.0
    itens_para_salvar = []

    for item in venda_data.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id} não encontrado.")
        
        if produto.quantidade_estoque < item.quantidade:
            raise HTTPException(
                status_code=400, 
                detail=f"Estoque insuficiente para '{produto.nome}'. Disponível: {produto.quantidade_estoque}"
            )

        produto.quantidade_estoque -= item.quantidade
        subtotal = produto.preco * item.quantidade
        valor_total += subtotal

        itens_para_salvar.append(
            models.ItemVenda(
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=produto.preco
            )
        )

    if valor_total > 200.0:
        valor_total *= 0.95

    nova_venda = models.Venda(valor_total=valor_total, itens=itens_para_salvar)
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)
    return nova_venda