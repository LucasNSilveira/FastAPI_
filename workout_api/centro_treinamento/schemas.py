from typing import Annotated, Generic, List, TypeVar
from pydantic import  UUID4, Field, PositiveFloat
from pydantic.generics import GenericModel
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description = 'Nome do Centro de Treinamento', exemple='CT King', max_length = 20)]   
    endereco: Annotated[str, Field(description = 'Endereco do Centro de Treinamento', exemple='Rua X, 120', max_length = 60)]
    proprietario: Annotated[str, Field(description = 'Proprietario do Centro de Treinamento', exemple='Marcos', max_length = 30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description = 'Nome do Centro de Treinamento', exemple='CT King', max_length = 20)]   

class CentroTreinamentoOut(CentroTreinamentoIn):
   id: Annotated[UUID4, Field(description = 'Identificador do Centro de Treinamento')]   

   
M= TypeVar('M') 
class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Número de itens retornados')
    items: List[M] = Field(description='Lista de itens retornados pelo critério usado')
            
 
    