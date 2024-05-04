from workout_api.contrib.schemas import BaseSchema
from pydantic import Field, UUID4
from pydantic.generics import GenericModel
from typing import Annotated, Generic, List, TypeVar



M= TypeVar('M') 


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description = 'Nome da categoria', exemple='Scale', max_length = 10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]

class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Número de itens retornados')
    items: List[M] = Field(description='Lista de itens retornados pelo critério usado')
            
