from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LocationCreate, LocationUpdate, LocationOut
from app.domain.use_cases.location_use_case import LocationUseCase
from app.api.error_handler import handle_domain_exception

router = APIRouter(prefix="/locations", tags=["Locations"])


def get_location_use_case(db: Session = Depends(get_db)) -> LocationUseCase:
    return LocationUseCase(db)


@router.get("/", response_model=List[LocationOut], summary="Список локаций")
def list_locations(skip: int = 0, limit: int = 20, use_case: LocationUseCase = Depends(get_location_use_case)):
    try:
        return use_case.get_all(skip=skip, limit=limit)
    except Exception as e:
        raise handle_domain_exception(e)


@router.get("/{location_id}", response_model=LocationOut, summary="Получить локацию")
def get_location(location_id: int, use_case: LocationUseCase = Depends(get_location_use_case)):
    try:
        return use_case.get_by_id(location_id)
    except Exception as e:
        raise handle_domain_exception(e)


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED, summary="Создать локацию")
def create_location(payload: LocationCreate, use_case: LocationUseCase = Depends(get_location_use_case)):
    try:
        return use_case.create(payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.put("/{location_id}", response_model=LocationOut, summary="Обновить локацию")
def update_location(location_id: int, payload: LocationUpdate, use_case: LocationUseCase = Depends(get_location_use_case)):
    try:
        return use_case.update(location_id, payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить локацию")
def delete_location(location_id: int, use_case: LocationUseCase = Depends(get_location_use_case)):
    try:
        use_case.delete(location_id)
    except Exception as e:
        raise handle_domain_exception(e)