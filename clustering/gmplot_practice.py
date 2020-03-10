import gmplot
import pandas as pd
import numpy as np

df = pd.read_csv("locs/location_4.csv", header=0, index_col=0)
latitudes = np.array(df["latitude"])
longitudes = np.array(df["longitude"])

gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 16)

gmap.scatter(latitudes, longitudes, 'cornflowerblue', edge_width=10)

gmap.draw("mymap.html")