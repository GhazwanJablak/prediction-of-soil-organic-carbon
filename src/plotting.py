import matplotlib.pyplot as plt
import geopandas as gpd

def map_plot(data, gdf, longitude_col=None, latitude_col=None):
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