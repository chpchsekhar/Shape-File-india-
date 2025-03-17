import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

 
tif_path = r"C:\Users\chpch\OneDrive\Desktop\Geo_pandas\reprojected.tif"

 
with rasterio.open(tif_path) as src:
    num_bands = src.count   
    print(f"Number of bands in the TIFF: {num_bands}")
    
    fig, axes = plt.subplots(1, num_bands, figsize=(5 * num_bands, 5))
    
    if num_bands == 1:
     
        band = src.read(1)   
        show(band, ax=axes, cmap="gray")    
        axes.set_title(f"Band 1")
    else:
        
        for i in range(num_bands):
            band = src.read(i + 1)  
            show(band, ax=axes[i], cmap="gray")   
            axes[i].set_title(f"Band {i + 1}")

    plt.show()
