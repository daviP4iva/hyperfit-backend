from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Any, List, Dict, Optional
import json
import re

router = APIRouter()

class RoutineRequest(BaseModel):
    response: str

@router.post("/process-routine")
async def process_routine(req: RoutineRequest):
    """
    Procesa el string JSON generado por el modelo y devuelve la rutina como lista de días normalizada.
    """
    try:
        json_string = req.response.strip()
        # Elimina posibles marcadores de código
        json_string = re.sub(r"^```json", "", json_string)
        json_string = re.sub(r"^```", "", json_string)
        json_string = re.sub(r"```$", "", json_string)
        json_string = json_string.strip()

        # Intenta parsear el JSON
        rutina_array = []
        if json_string.startswith('['):
            rutina_array = json.loads(json_string)
        else:
            rutina_json = json.loads(json_string)
            if isinstance(rutina_json, dict) and "rutina" in rutina_json:
                if isinstance(rutina_json["rutina"], list):
                    rutina_array = rutina_json["rutina"]
                elif isinstance(rutina_json["rutina"], dict):
                    rutina_array = list(rutina_json["rutina"].values())
            elif isinstance(rutina_json, list):
                rutina_array = rutina_json
            else:
                rutina_array = [rutina_json]

        # Normaliza y filtra días vacíos o sin ejercicios
        rutina_final = []
        for i, dia in enumerate(rutina_array):
            # Si el día es un dict con ejercicios
            if isinstance(dia, dict):
                ejercicios = dia.get("ejercicios") or dia.get("ejercicios_dia") or []
                # Si ejercicios es un dict, conviértelo a lista
                if isinstance(ejercicios, dict):
                    ejercicios = list(ejercicios.values())
                # Filtra días sin ejercicios
                if ejercicios and isinstance(ejercicios, list) and len(ejercicios) > 0:
                    rutina_final.append({
                        "nombre": dia.get("nombre", f"Día {i+1}"),
                        "ejercicios": ejercicios
                    })
            # Si el día es una lista de ejercicios directamente
            elif isinstance(dia, list) and len(dia) > 0:
                rutina_final.append({
                    "nombre": f"Día {i+1}",
                    "ejercicios": dia
                })

        return {"routine": rutina_final}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando la rutina: {str(e)}")