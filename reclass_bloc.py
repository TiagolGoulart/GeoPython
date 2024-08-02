import rasterio
import numpy as np
from tqdm import tqdm

def reclassify_raster(input_raster_path, output_raster_path, output_txt_path):
    # Abrir o raster de entrada
    with rasterio.open(input_raster_path) as src:
        # Ler os metadados do raster original
        metadata = src.meta.copy()
        
        # Atualizar metadados para incluir a compressão DEFLATE e definir o tipo de dados
        metadata.update(compress='DEFLATE', dtype=rasterio.uint8)
        
        # Criar o raster de saída
        with rasterio.open(output_raster_path, 'w', **metadata) as dst:
            # Inicializar contagem de pixels
            pixel_counts = {0: 0, 1: 0, 2: 0}
            
            # Processar em blocos
            for ji, window in tqdm(src.block_windows(1), desc="Processando blocos"):
                raster_data = src.read(1, window=window)
                
                # Criar um array para os dados reclassificados
                reclassified_data = np.copy(raster_data)
                
                # Reclassificar os pixels
                reclassified_data[(raster_data == 3) | (raster_data == 4) | 
                                (raster_data == 5) | (raster_data == 6)] = 1
                reclassified_data[(raster_data != 0) & (raster_data != 1)] = 2
                
                # Pixels que já foram reclassificados para 1 devem permanecer como 1
                reclassified_data[(raster_data == 3) | (raster_data == 4) | 
                                (raster_data == 5) | (raster_data == 6)] = 1
                
                # Manter os pixels com valor 0 iguais
                reclassified_data[raster_data == 0] = 0

                # Atualizar contagem de pixels
                unique, counts = np.unique(reclassified_data, return_counts=True)
                for value, count in zip(unique, counts):
                    pixel_counts[value] += count
                
                # Escrever o bloco reclassificado no raster de saída
                dst.write(reclassified_data.astype(rasterio.uint8), 1, window=window)
        
        # Escrever a contagem dos pixels reclassificados em um arquivo TXT
        with open(output_txt_path, 'w') as txt_file:
            for value, count in pixel_counts.items():
                txt_file.write(f'Valor: {value}, Contagem: {count}\n')

# Lista de arquivos de entrada e saída para processamento em lote
input_rasters = [
    'Cobertura/1990/brazil_1990.tif',
    'Cobertura/2000/brazil_2000.tif',
    'Cobertura/2010/brazil_2010.tif',
    'Cobertura/2020/brazil_2020.tif'
]
output_rasters = [
    'Reclassificado/1990/brazil_reclass_1990.tif',
    'Reclassificado/2000/brazil_reclass_2000.tif',
    'Reclassificado/2010/brazil_reclass_2010.tif',
    'Reclassificado/2020/brazil_reclass_2020.tif'
]
output_txts = [
    'Reclassificado/1990/brazil_reclass_1990.txt',
    'Reclassificado/2000/brazil_reclass_2000.txt',
    'Reclassificado/2010/brazil_reclass_2010.txt',
    'Reclassificado/2020/brazil_reclass_2020.txt'
]

# Processar múltiplos rasters com barra de progresso
for input_raster, output_raster, output_txt in tqdm(zip(input_rasters, output_rasters, output_txts), desc="Processando rasters", total=len(input_rasters)):
    reclassify_raster(input_raster, output_raster, output_txt)
