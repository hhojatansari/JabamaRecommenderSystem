from fastapi import FastAPI

from utils import distance_matrix


app = FastAPI(
    title="Jabama Recommender System",
    description="A content-based recommender system for Gilan.",
    docs_url='/swagger-ui',
    version="1.0.0"
)

distance_matrix = distance_matrix.calculate()
