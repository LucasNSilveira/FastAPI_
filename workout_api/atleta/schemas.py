from typing import Annotated, Optional, Generic, List, TypeVar
from pydantic import UUID4, Field, PositiveFloat
from pydantic.generics import GenericModel
from workout_api.contrib.schemas import BaseSchema, OutMixin

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta


M= TypeVar('M') 

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description = 'Nome do atleta', exemple='Joao', max_length = 50)]
    cpf: Annotated[str, Field(description = 'CPF do atleta', exemple='12345678900', max_length = 11)]
    peso: Annotated[PositiveFloat, Field(description = 'Peso do atleta', exemple='85', max_length = 3)]
    idade: Annotated[int, Field(description = 'Idade do atleta', exemple=20, max_length = 3)]
    altura: Annotated[PositiveFloat, Field(description = 'Altura do atleta', exemple=1.80)]
    sexo: Annotated[str, Field(description = 'Sexo do atleta', exemple='M', max_length = 1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do Atleta')]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass
class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description = 'Nome do atleta', exemple='Joao', max_length = 50)]
    idade: Annotated[Optional[int], Field(None, description = 'Idade do atleta', exemple='20', max_length = 3)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description = 'Altura do atleta', exemple=1.80)]


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Número de itens retornados')
    items: List[M] = Field(description='Lista de itens retornados pelo critério usado')
            
