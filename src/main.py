import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import database, engine, metadata
from src.routes import auth_routes, product_routes, prediction_products_routes

app = FastAPI(title="AIVentory API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
metadata.create_all(engine)

# Incluir rutas
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(prediction_products_routes.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Bienvenido a AIVentory API"}
