from fastapi import APIRouter, Depends, UploadFile, File

from src.dependencies.auth import get_usuario_actual
import joblib
import pandas as pd
from io import StringIO

router = APIRouter(prefix="/prediction_products", tags=["prediction_products"])

model = joblib.load("modelo_prediccion_ventas.pkl")


def predecir_ventas_csv(file: UploadFile, agrupacion: str = "mes"):

    contents = file.file.read().decode("utf-8")
    df = pd.read_csv(StringIO(contents))

    df["mes"] = df["mes"].map(
        {
            "Enero": 1,
            "Febrero": 2,
            "Marzo": 3,
            "Abril": 4,
            "Mayo": 5,
            "Junio": 6,
            "Julio": 7,
            "Agosto": 8,
            "Septiembre": 9,
            "Octubre": 10,
            "Noviembre": 11,
            "Diciembre": 12,
        }
    )

    df["evento_especial"] = df["evento_especial"].map(
        {
            "Ninguno": 0,
            "Black Friday": 1,
            "Navidad": 2,
            "Día del Padre": 3,
            "Lanzamiento": 4,
        }
    )

    X = df[
        [
            "precio",
            "precio_anterior",
            "descuento_aplicado",
            "mes",
            "evento_especial",
            "stock_inicial",
            "stock_restante",
        ]
    ]

    predicciones = model.predict(X)

    df["ventas_predichas"] = predicciones

    if agrupacion == "semana":
        df["semana"] = (
            pd.to_datetime(df["mes"].astype(str), format="%m").dt.isocalendar().week
        )
        ventas_agrupadas = (
            df.groupby(["semana"])
            .agg({"ventas_predichas": "sum", "stock_inicial": "sum"})
            .reset_index()
        )
    elif agrupacion == "mes":
        ventas_agrupadas = (
            df.groupby(["mes"])
            .agg({"ventas_predichas": "sum", "stock_inicial": "sum"})
            .reset_index()
        )

    resultados = ventas_agrupadas.to_dict(orient="records")
    return resultados


@router.post("/")
async def get_prediction_products(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_usuario_actual),
    agrupacion: str = "mes",
):
    predicciones = predecir_ventas_csv(file, agrupacion)
    return {"predicciones": predicciones}
