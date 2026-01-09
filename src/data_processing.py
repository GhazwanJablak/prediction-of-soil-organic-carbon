import pandas as pd
import numpy as np
import geopandas as gpd
import joblib
from pyproj import CRS
import reverse_geocode as rg
from sklearn.decomposition import PCA
from pathlib import Path
from typing import Tuple, List
from src.logging_configuration import logger


def geospatial_data_processing(df:pd.DataFrame, bare_soil_months:List)->gpd.GeoDataFrame:
    if not isinstance(bare_soil_months, list):
         logger.Error("Selected months is not provided as a list")
         raise TypeError("Selected months must be provided as list")
    df["Year"] = pd.to_datetime(df["SampleDate"], format="mixed").dt.year
    df["Month"] = pd.to_datetime(df["SampleDate"], format="mixed").dt.month
    if not all(s in df["Month"].unique().tolist() for s in bare_soil_months):
         logger.Error("Selected months are not available in the data")
         raise TypeError(f"Provided months are not valid region in the dataset")
    df_baresoil = df[df["Month"].isin(bare_soil_months)]
    geo_df = gpd.GeoDataFrame(df_baresoil, geometry=gpd.points_from_xy(df_baresoil["X"], df_baresoil["Y"], crs=CRS.from_epsg(27700)))
    geo_df = geo_df.to_crs(crs="EPSG:4326")
    geo_df['longitude'] = geo_df.geometry.x
    geo_df['latitude'] = geo_df.geometry.y
    geo_df.index = pd.RangeIndex(geo_df.shape[0])
    state, county = [], []
    for coord in zip(geo_df["latitude"].values, geo_df["longitude"].values):
        location = rg.get(coord)
        state.append(location["state"])
        county.append(location["county"])
    location_df = pd.DataFrame({"state":state, "county":county})
    geo_df_fin = pd.concat([geo_df, location_df], axis=1)
    return geo_df_fin


def train_test_split(df:pd.DataFrame, train_state:List,test_state:List)->Tuple[pd.DataFrame]:
     train_state = [s.capitalize() for s in train_state]
     test_state = [s.capitalize() for s in test_state]
     ignore_cols = ["SiteName", "X", "Y", 
                    "SampleDate", "TargetSOC", 
                    "longitude", "latitude", 
                    "state", 'geometry', 'county']
     if not isinstance(train_state, list) or not isinstance(test_state, list):
         logger.Error("Train and Test states are not lists")
         raise TypeError("Train states and test states must be provided as list")
     if not all(s in df["state"].unique().tolist() for s in train_state) or \
         not all(s in df["state"].unique().tolist() for s in test_state):
         logger.Error("Selected states are not available in the data")
         raise TypeError(f"Provided states are not valid region in the dataset")
     
     train = df[df["state"].isin(train_state)]
     logger.info(f"training data has {train.shape[0]} rows and {train.shape[1]} columns")
     test = df[df["state"].isin(test_state)]
     logger.info(f"testing data has {test.shape[0]} rows and {train.shape[1]} columns")
     Xtrain = train[[col for col in train if col not in ignore_cols]]
     Xtest = test[[col for col in test if col not in ignore_cols]]
     ytrain = train["TargetSOC"]
     ytest = test["TargetSOC"]
     logger.info(f"testing data is {np.round(Xtest.shape[0]/df.shape[0] * 100)}% of original data")
     return Xtrain, Xtest, ytrain, ytest


def training_data_processing(Xtrain, Xtest, n_components=5, output_dir=None):
    if output_dir is None:
        logger.error("directory to save the models has not been provided")
        raise TypeError("Please provide a valid directory to save models")
    else:
        Path(f"{output_dir}").mkdir(exist_ok=True)
        pca = PCA(n_components=n_components)
        Xtrain_reduced = pca.fit_transform(Xtrain)
        Xtest_reduced = pca.transform(Xtest)
        logger.info(f"training data dimensions are {Xtrain_reduced.shape[0]} rows and {Xtrain_reduced.shape[1]} features")
        joblib.dump(pca, f"{output_dir}/pca.pkl")
        return pca, Xtrain_reduced,Xtest_reduced