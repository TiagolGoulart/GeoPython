# Importe as bibliotecas necessárias
import geopandas as gpd
import numpy as np
import shapely;
import matplotlib.pyplot as plt

# Leia o shapefile com os dados 
ufs=gpd.read_file(r'C:\Users\tiago\Área de Trabalho\PROJECTS\MAPA DENSIDADE BRASIL\BR_UF_2022\BR_UF_2022.shp')

# Criei uma coluna para utilizar de atributo para dissolver as geometrias dos estados e
# criar uma geometria única para o país
ufs['pais']=1

# Dissolvendo as geometrias
brasil=ufs.dissolve(by='pais')

from matplotlib.patches import Patch

# Reprojeta a geometria
brasil_mercator= brasil.to_crs('EPSG:5641')
# Gera os buffers  de acordo com os atributos especificados pelos argumentos
buffer= brasil_mercator.buffer(distance=100000, resolution=10,cap_style=1, join_style=1, mitre_limit=5.0, single_sided=False)

# Visualizando o resultado
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