#   timestamp: 2022-07-19T01:39:31+00:00

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class AddproductInShema(BaseModel):
    productName: str
    price: float
    barcode: str
    skuId: int


class Status(Enum):
    success = 'success'
    skunotfound = 'skunotfound'


class Product(BaseModel):
    id: int
    productName: str
    price: float
    barcode: str
    skuId: int


class AddproductOutShema(BaseModel):
    status: Status
    product: Product
