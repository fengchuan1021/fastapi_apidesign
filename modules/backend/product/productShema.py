#   timestamp: 2022-07-19T01:35:20+00:00

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class AddproductPostRequest(BaseModel):
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


class AddproductPostResponse(BaseModel):
    status: Status
    product: Product
