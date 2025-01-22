from fastapi import HTTPException, Path, Query

from server import app
from server import distance_matrix
from utils.utils import get_similar_products


@app.get("/recommendations/{product_id}", summary="Similar products")
async def recommend_products(
    product_id: str = Path(..., description="Product ID"),
    number: int = Query(10, description="Number of products")
):
    if product_id not in distance_matrix.index:
        raise HTTPException(status_code=404, detail="Product not found")

    recommendations = get_similar_products(product_id, number)
    return {"product_id": product_id, "recommendations": recommendations}
