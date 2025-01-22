from typing import List

from server import distance_matrix


def get_similar_products(product_id: str, top: int) -> List[int]:
    return distance_matrix.loc[product_id].iloc[:].sort_values().head(top).index.to_list()
