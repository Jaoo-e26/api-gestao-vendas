from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# --- SCHEMAS DE PRODUTO ---
class ProdutoBase(BaseModel):
    nome: str = Field(..., example="Teclado Mecânico")
    preco: float = Field(..., gt=0, description="O preço deve ser maior que zero", example=250.00)
    quantidade_estoque: int = Field(..., ge=0, description="O estoque não pode ser negativo", example=15)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

# --- SCHEMAS DE VENDA ---
class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0, description="A quantidade deve ser de pelo menos 1 item")

class ItemVendaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True

class VendaCreate(BaseModel):
    itens: List[ItemVendaCreate]

class VendaResponse(BaseModel):
    id: int
    data_venda: datetime
    valor_total: float
    itens: List[ItemVendaResponse]

    class Config:
        from_attributes = True