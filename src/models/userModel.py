from pydantic import BaseModel, EmailStr
from enum import Enum

class NivelEnum(str, Enum):
    principiante = "Principiante"
    intermedio = "Intermedio"
    avanzado = "Avanzado"

class ObjetivoEnum(str, Enum):
    perder_peso = "Perder peso"
    ganar_musculo = "Ganar músculo"
    mantener = "Mantener"
    definir = "Definir"

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    tipo_cuenta: str  # Personal o Profesional
    altura: float  # en metros
    peso: float  # en kg
    nivel: NivelEnum  # Solo acepta los valores del Enum
    objetivo: ObjetivoEnum  # Solo acepta los valores del Enum
    alergenos: str  # Ninguno o lista separada por comas
    google_id: str = None  # ID de Google, opcional
    