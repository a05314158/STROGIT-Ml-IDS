"""
Pydantic схемы для валидации входных данных API
"""
from pydantic import BaseModel, Field, validator
from typing import Dict
from config import NUM_FEATURES


class SensorDataPayload(BaseModel):
    """Схема для валидации данных от сенсора"""
    features: list[float] = Field(..., description="Вектор признаков трафика")
    packet_count: int = Field(..., ge=0, description="Количество пакетов")
    total_bytes: int = Field(..., ge=0, description="Общий объем данных в байтах")
    ip_summary: Dict[str, int] = Field(default_factory=dict, description="Статистика по IP адресам")
    domain_summary: Dict[str, int] = Field(default_factory=dict, description="Статистика по доменам")
    
    @validator('features')
    def validate_features_length(cls, v):
        """Проверяем, что вектор признаков имеет правильную длину"""
        if len(v) != NUM_FEATURES:
            raise ValueError(f'Features vector must have exactly {NUM_FEATURES} elements, got {len(v)}')
        return v
    
    @validator('features')
    def validate_features_values(cls, v):
        """Проверяем, что все значения валидны (не NaN, не Inf)"""
        import math
        for i, val in enumerate(v):
            if math.isnan(val) or math.isinf(val):
                raise ValueError(f'Feature at index {i} has invalid value: {val}')
        return v
    
    @validator('ip_summary')
    def validate_ip_summary(cls, v):
        """Проверяем, что значения в ip_summary положительные"""
        for ip, bytes_count in v.items():
            if not isinstance(bytes_count, int) or bytes_count < 0:
                raise ValueError(f'Invalid byte count for IP {ip}: {bytes_count}')
        return v
    
    @validator('domain_summary')
    def validate_domain_summary(cls, v):
        """Проверяем, что значения в domain_summary положительные"""
        for domain, hits in v.items():
            if not isinstance(hits, int) or hits < 0:
                raise ValueError(f'Invalid hit count for domain {domain}: {hits}')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [10.0, 1500.0, 60.0, 2.5, 0.1, 0.8, 5, 0.9, 0.1, 3, 0.01, 0.001, 8],
                "packet_count": 10,
                "total_bytes": 1500,
                "ip_summary": {"192.168.1.100": 1500},
                "domain_summary": {"google.com": 5, "github.com": 3}
            }
        }


class CreateModelPayload(BaseModel):
    """Схема для создания новой модели"""
    model_name: str = Field(..., min_length=1, max_length=100, description="Название модели")
    model_type: str = Field(..., description="Тип модели")
    
    @validator('model_type')
    def validate_model_type(cls, v):
        """Проверяем, что тип модели поддерживается"""
        allowed_types = ['tensorflow', 'isolation_forest']
        if v not in allowed_types:
            raise ValueError(f'Model type must be one of {allowed_types}, got {v}')
        return v


class ActivateModelPayload(BaseModel):
    """Схема для активации модели"""
    model_id: int = Field(..., gt=0, description="ID модели для активации")


class DeleteModelPayload(BaseModel):
    """Схема для удаления модели"""
    model_id: int = Field(..., gt=0, description="ID модели для удаления")


class CreateApiKeyPayload(BaseModel):
    """Схема для создания API ключа"""
    name: str = Field(..., min_length=1, max_length=100, description="Название сенсора")


class DeleteApiKeyPayload(BaseModel):
    """Схема для удаления API ключа"""
    key_id: int = Field(..., gt=0, description="ID ключа для удаления")


class ToggleApiKeyPayload(BaseModel):
    """Схема для активации/деактивации API ключа"""
    key_id: int = Field(..., gt=0, description="ID ключа")
