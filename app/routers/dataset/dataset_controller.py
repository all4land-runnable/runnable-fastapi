# app/routers/dataset/dataset_controller.py
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from config.common.common_response import CommonResponse
from app.routers.dataset.dataset_service import DatasetService
from config.external.hospital_api import get_hospitals

router = APIRouter(prefix="/dataset", tags=["dataset"])

# DI 헬퍼: 필요 시 다른 레이어처럼 Depends 주입도 가능하지만,
# 이 서비스는 외부 상태가 없어 간단히 팩토리로 씁니다.
def get_dataset_service() -> DatasetService:
    return DatasetService()

@router.get("/drinkingFountains")
def read_drinking_fountains(
    lat: Optional[float] = Query(37.566406, description="카메라 위도(도)"),
    lon: Optional[float] = Query(126.977822, description="카메라 경도(도)"),
    radius_m: float = Query(500.0, description="반경(미터)"),
):
    """
    로컬에 저장된 음수대 JSON을 FastAPI가 중계.
    - 쿼리파라미터(lat, lon)를 주면 반경 필터 적용
    - 파일은 { "DATA": [...] } 형식이라고 가정
    """
    svc = get_dataset_service()
    data = svc.read_drinking_fountains(lat, lon, radius_m)
    return CommonResponse(code=200, message="음수대 조회 성공", data=data)

@router.get("/crosswalks")
def read_crosswalks(
    lat: Optional[float] = Query(37.566406, description="카메라 위도(도)"),
    lon: Optional[float] = Query(126.977822, description="카메라 경도(도)"),
    radius_m: float = Query(500.0, description="반경(미터)"),
):
    """
    로컬에 저장된 횡단보도 JSON을 FastAPI가 중계.
    - 쿼리파라미터(lat, lon)를 주면 반경 필터 적용
    - 파일은 { "DATA": [...] } 형식이라고 가정
    """
    svc = get_dataset_service()
    data = svc.read_crosswalks(lat, lon, radius_m)
    return CommonResponse(code=200, message="횡단보도 조회 성공", data=data)

@router.get("/hospitals")
def read_crosswalks(
    lat: Optional[float] = Query(37.566406, description="카메라 위도(도)"),
    lon: Optional[float] = Query(126.977822, description="카메라 경도(도)"),
    radius_m: float = Query(500.0, description="반경(미터)"),
):
    data = get_hospitals(lon, lat, radius_m)
    return CommonResponse(code=200, message="병원 조회 성공", data=data["items"])