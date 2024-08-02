import rasterio
import numpy as np
from tqdm import tqdm

def reclassify_raster(input_raster_path, output_raster_path, output_txt_path):
    # Open the input raster
    with rasterio.open(input_raster_path) as src:
        # Read the original raster metadata
        metadata = src.meta.copy()
        
        # Update metadata to include DEFLATE compression and set data type
        metadata.update(compress='DEFLATE', dtype=rasterio.uint8)
        
        # Create the output raster
        with rasterio.open(output_raster_path, 'w', **metadata) as dst:
            # Initialize pixel count
            pixel_counts = {0: 0, 1: 0, 2: 0}
            
            # Process in blocks
            for ji, window in tqdm(src.block_windows(1), desc="Processing blocks"):
                raster_data = src.read(1, window=window)
                
                # Create an array for the reclassified data
                reclassified_data = np.copy(raster_data)
                
                # Reclassify the pixels
                reclassified_data[(raster_data == 3) | (raster_data == 4) | 
                                (raster_data == 5) | (raster_data == 6)] = 1
                reclassified_data[(raster_data != 0) & (raster_data != 1)] = 2
                
                # Pixels that have already been reclassified to 1 should remain as 1
                reclassified_data[(raster_data == 3) | (raster_data == 4) | 
                                (raster_data == 5) | (raster_data == 6)] = 1
                
                # Keep the pixels with value 0 the same
                reclassified_data[raster_data == 0] = 0

                # Update pixel count
                unique, counts = np.unique(reclassified_data, return_counts=True)
                for value, count in zip(unique, counts):
                    pixel_counts[value] += count
                
                # Write the reclassified block to the output raster
                dst.write(reclassified_data.astype(rasterio.uint8), 1, window=window)
        
        # Write the count of reclassified pixels to a TXT file
        with open(output_txt_path, 'w') as txt_file:
            for value, count in pixel_counts.items():
                txt_file.write(f'Value: {value}, Count: {count}\n')

# List of input and output files for batch processing
input_rasters = [
    'Cobertura/1990/brazil_1990.tif',
    'Cobertura/2000/brazil_2000.tif',
    'Cobertura/2010/brazil_2010.tif',
    'Cobertura/2020/brazil_2020.tif'
]
output_rasters = [
    'Reclassified/1990/brazil_reclass_1990.tif',
    'Reclassified/2000/brazil_reclass_2000.tif',
    'Reclassified/2010/brazil_reclass_2010.tif',
    'Reclassified/2020/brazil_reclass_2020.tif'
]
output_txts = [
    'Reclassified/1990/brazil_reclass_1990.txt',
    'Reclassified/2000/brazil_reclass_2000.txt',
    'Reclassified/2010/brazil_reclass_2010.txt',
    'Reclassified/2020/brazil_reclass_2020.txt'
]

# Process multiple rasters with progress bar
for input_raster, output_raster, output_txt in tqdm(zip(input_rasters, output_rasters, output_txts), desc="Processing rasters", total=len(input_rasters)):
    reclassify_raster(input_raster, output_raster, output_txt)
