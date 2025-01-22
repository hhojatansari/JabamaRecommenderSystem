import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import pairwise_distances

from configs import data_path
from configs import geo_weight
from configs import num_weights


def calculate():
    data = pd.read_pickle(data_path)

    # --------- Preprocessing --------->
    data.loc[data.score.isna(), 'score'] = 0
    data.loc[data.stair.isna(), 'stair'] = 0

    data.iranian_toilet = data.iranian_toilet.apply(lambda x: 1 if x else 0)
    data.western_toilet = data.western_toilet.apply(lambda x: 1 if x else 0)
    data.bathroom = data.bathroom.apply(lambda x: 1 if x else 0)
    data.exclusive = data.exclusive.apply(lambda x: 1 if x else 0)
    data.breakfast = data.breakfast.apply(lambda x: 1 if x else 0)

    data['type'] = data.product_id.apply(lambda x: x.split('-')[0])
    encoder = OneHotEncoder(sparse_output=False)
    encoded_array = encoder.fit_transform(data[['type']])
    encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(['type']))
    data = pd.concat([data, encoded_df], axis=1)
    del data['type']

    # ------- Numerical features ------>
    num_product = data.drop(['product_id', 'lat', 'lng'], axis=1)
    num_columns = num_product.columns

    num_scaler = MinMaxScaler()
    scaled_num = num_scaler.fit_transform(num_product)

    num_weights_df = pd.DataFrame(num_weights, columns=num_columns, index=num_product.index)
    num_products_vector = pd.DataFrame(scaled_num, columns=num_columns).mul(num_weights_df)
    num_distance_matrix = pairwise_distances(num_products_vector.values, metric='euclidean')

    # ----- Geographical features ----->
    geo_product = data[['lat', 'lng']]

    geo_product_radians = np.radians(geo_product.values)
    geo_distance_matrix = pairwise_distances(geo_product_radians, metric='haversine')
    geo_distance_matrix_km = geo_distance_matrix * 6371

    s_min = 0
    s_max = 10
    geo_distance_matrix = (geo_distance_matrix - geo_distance_matrix.min()) / (
                geo_distance_matrix.max() - geo_distance_matrix.min())
    geo_distance_matrix = geo_distance_matrix * (s_max - s_min) + s_min

    # --------- Distance Matrix --------->
    total_rooms_distance = 1 * num_distance_matrix + geo_weight * geo_distance_matrix
    result_df = pd.DataFrame(total_rooms_distance, index=data.product_id, columns=data.product_id)

    return result_df
