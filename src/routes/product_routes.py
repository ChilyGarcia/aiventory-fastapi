from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from fastapi.responses import JSONResponse
from src.database import database
from src.dependencies.auth import get_usuario_actual
from src.dependencies.permissions import require_permission
from src.models.product_model import product
from src.schemas.product_schema import Product, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user = Depends(require_permission("create_product"))
):
    if not getattr(current_user, "enterprise_id", None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario debe pertenecer a una empresa para crear productos"
        )

    product_values = {
        **product_data.model_dump(),
        "enterprise_id": current_user.enterprise_id
    }

    query = product.insert().values(**product_values)
    try:
        product_id = await database.execute(query)
        return {**product_values, "id": product_id}
    except Exception as e:
        print(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el producto: {str(e)}"
        )


@router.get("/", response_model=List[Product])
async def get_products(current_user = Depends(require_permission("read_product"))):
    if not getattr(current_user, "enterprise_id", None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario debe pertenecer a una empresa para ver productos"
        )

    query = product.select().where(
        product.c.enterprise_id == current_user.enterprise_id)
    return await database.fetch_all(query)


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    current_user = Depends(require_permission("read_product"))
):
    if not getattr(current_user, "enterprise_id", None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario debe pertenecer a una empresa para ver productos"
        )

    query = product.select().where(
        (product.c.id == product_id) &
        (product.c.enterprise_id == current_user.enterprise_id))
    product_data = await database.fetch_one(query)
    
    if not product_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return product_data


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user = Depends(require_permission("update_product"))
):
    if not getattr(current_user, "enterprise_id", None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario debe pertenecer a una empresa para actualizar productos"
        )

    query = product.select().where(
        (product.c.id == product_id) &
        (product.c.enterprise_id == current_user.enterprise_id))
    existing_product = await database.fetch_one(query)

    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    update_query = product.update().where(
        (product.c.id == product_id)).values(**product_data.model_dump())

    await database.execute(update_query)
    return {
        **product_data.model_dump(),
        "id": product_id,
        "enterprise_id": current_user.enterprise_id
    }


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user = Depends(require_permission("delete_product"))
):
    if not getattr(current_user, "enterprise_id", None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario debe pertenecer a una empresa para eliminar productos"
        )

    query = product.select().where(
        (product.c.id == product_id) &
        (product.c.enterprise_id == current_user.enterprise_id))
    existing_product = await database.fetch_one(query)
    
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    delete_query = product.delete().where(product.c.id == product_id)
    await database.execute(delete_query)

    return JSONResponse(
        content={"message": "Producto eliminado exitosamente"},
        status_code=status.HTTP_200_OK
    )
