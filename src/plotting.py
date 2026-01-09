import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np


def map_plot(data:pd.DataFrame, gdf:gpd.GeoDataFrame, longitude_col:str=None, latitude_col:str=None)->None:
    """
    Plotting sample location on top of UK map.
    
    :param data: Dataframe with samples and locations.
    :type data: pd.DataFrame
    :param gdf: Geodataframe of UK.
    :type gdf: gpd.GeoDataFrame
    :param longitude_col: Name of longitude column.
    :type longitude_col: str
    :param latitude_col: Name of latitude column.
    :type latitude_col: str
    """
    cols = data.columns.tolist()
    if longitude_col and latitude_col:
        if latitude_col not in cols or longitude_col not in cols:
            raise TypeError("selected longitude column and latitude column must be available columns in the dataframe")
    else:
        raise TypeError("Please provide valid longitude and latitude columns")

    geo_data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data[longitude_col], data[latitude_col]))
    fig, ax = plt.subplots(figsize=(14, 10))
    gdf.plot(ax=ax, edgecolors="black", linewidth=1, cmap="Greens")
    ax.set_facecolor("#a2d2ff")
    geo_data.plot(ax=ax, color="red", marker="*", markersize=10)
    plt.show


def null_plot(dataframe:pd.DataFrame)->None:
    """
    A QC plot to check null values in the dataframe.
    
    :param dataframe: Description
    :type dataframe: pd.DataFrame
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("This function expects a dataframe as an input")
    else:
        nulls = (dataframe.isnull().sum()/dataframe.shape[0]) * 100
        _, ax = plt.subplots(figsize=(30, 15))
        ax.bar(nulls.index, nulls.values)
        ax.set_xlabel("Column names", fontsize=10)
        ax.set_ylabel("Null values count", fontsize=10)
        ax.set_ylim(0, 100)
        ax.tick_params(axis="x", rotation=75)
        plt.show()


def geospatail_distribution_plot(df:pd.DataFrame)-> None:
    """
    Plotting number of samples per state to determine train and test datasets.
    
    :param df: input dataframe.
    :type df: pd.DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("This function expects a dataframe as an input")
    temp = df["state"].value_counts()
    _, ax = plt.subplots(figsize=(5, 5))
    ax.bar(temp.index, temp.values)
    ax.set_xlabel("States")
    ax.set_ylabel("Number of samples")
    ax.set_title("Available regions in the dataset")
    plt.show()


def prediction_vs_observed_plot(predictions:np.ndarray, observed:np.ndarray)->None:
    """
    Creating 1 - 1 plot for predicted vs. observed values.
    
    :param predictions: Predictions array.
    :type predictions: np.ndarray
    :param observed: Observed array.
    :type observed: np.ndarray
    """
    _, ax = plt.subplots(figsize=(7,5))
    ax.scatter(predictions, observed)
    ax.plot([predictions.min(), predictions.max()], [observed.min(), observed.max()],
             color='green', linestyle='dashed',linewidth=1)
    ax.set_xlabel("Predicted carbon content")
    ax.set_ylabel("Observed carbon content")
    ax.set_title("1:1 Prediction vs Observed values plot")
    plt.show()