# Import the necessary libraries
import geopandas as gpd
import numpy as np
import shapely;
import matplotlib.pyplot as plt

# Read the shapefile with the data
ufs=gpd.read_file(r'C:\Users\BR_UF_2022.shp')

# Create a column to use as an attribute to dissolve the geometries of the states and
# create a unique geometry for the country
ufs['pais']=1

# Dissolving the geometries
brasil=ufs.dissolve(by='pais')

from matplotlib.patches import Patch

# Reproject the geometry
brasil_mercator= brasil.to_crs('EPSG:5641')
# Generate the buffers according to the attributes specified by the arguments
buffer= brasil_mercator.buffer(distance=100000, resolution=10,cap_style=1, join_style=1, mitre_limit=5.0, single_sided=False)

# Viewing the result
f, ax = plt.subplots()
buffer.plot(ax=ax, color='green', label='Brasil')
brasil_mercator.plot(ax=ax, color='yellow', label='Buffer')
legend_elements = [ Patch(facecolor='green', edgecolor='black',
                         label='Buffer'),
                    Patch(facecolor='yellow', edgecolor='black',
                          label='Brasil')]
ax.legend(handles=legend_elements)
plt.axis('off')
plt.show()
