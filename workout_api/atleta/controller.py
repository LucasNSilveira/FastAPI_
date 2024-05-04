from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from pydantic.generics import GenericModel

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, PaginatedResponse
from workout_api.atleta.models import Atleta
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.contrib.repository.dependencies import DatabaseDependency
from sqlalchemy.future import select
router = APIRouter()

@router.post(
        path='/',
        summary='Criar novo atleta',
        status_code=status.HTTP_201_CREATED)
   
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn=Body(...)
    ):

    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria =(await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))
                ).scalars().first()
    centro_treinamento =(await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
                ).scalars().first()
    atleta_cpf = atleta_in.cpf

    atleta = (await db_session.execute(select(Atleta).filter_by(nome=atleta_cpf))).scalars().first()
    if atleta:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com esse cpf: {atleta_cpf}'
        )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )
    try:
        atleta_out = AtletaOut(id=uuid4, created_at=datetime.utcnow())
        atleta_model = Atleta(**atleta_out.model_dump(exclude={'categoria, centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )
    return atleta_out


@router.get(
        path='/',
        summary='Consultar um atleta',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
        )
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:

    atleta: AtletaOut = (
        await db_session.execute(select(Atleta).filter_by(id=id))
        ).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não foi encontrado no id: {id}'
        )
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)    
    return atleta


@router.get(
        path='/atletas',
        summary='Consultar todos os atletas',
        status_code=status.HTTP_200_OK,
        response_model=PaginatedResponse[AtletaOut],
        )
async def get_atletas(db_session: DatabaseDependency) -> PaginatedResponse[AtletaOut]:

    atletas = paginate(await db_session.execute(select(Atleta)).scalars().all())
    
    return atletas

@router.delete(
        path='/{id}',
        summary='Deletar um Atleta pelo id',
        status_code=status.HTTP_204_NO_CONTENT
        )

async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(Atleta).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_204_NOT_FOUND, 
            detail=f'Atleta não foi encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()