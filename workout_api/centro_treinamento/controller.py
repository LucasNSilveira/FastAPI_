from http.client import HTTPException
from uuid import uuid4
from fastapi import APIRouter,Body, status
from pydantic import UUID4
from workout_api.contrib.repository.dependencies import DatabaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut, PaginatedResponse
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy import select
router = APIRouter()

@router.post(
        path='/',
        summary='Criar um novo centro de treinamento',
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut
        )
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn=Body(...)
    ) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
        path='/centro_treinamento',
        summary='Consultar todos os centros de treinamento',
        status_code=status.HTTP_200_OK,
        response_model=PaginatedResponse[CentroTreinamentoOut],
        )
async def query(db_session: DatabaseDependency) -> PaginatedResponse[CentroTreinamentoOut]:

    centros_treinamentos = paginate(await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    return centros_treinamentos


@router.get(
        path='/{id}',
        summary='Consultar um centro de treinamento',
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut,
        )
async def query(id: UUID4,db_session: DatabaseDependency) -> CentroTreinamentoOut:

    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_204_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')
    return centro_treinamento