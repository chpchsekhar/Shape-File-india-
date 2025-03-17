import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show
from rasterio.warp import transform_bounds, calculate_default_transform, reproject, Resampling
import os
from geopy.distance import geodesic
from pyproj import Transformer
from shapely.geometry import Point
import numpy as np

class MapPlotter:
    def __init__(self, shp_path):
        self.shp_path = shp_path
        try:
            self.world_map = gpd.read_file(shp_path)
            self.default_xlim = None
            self.default_ylim = None
            print(f"Successfully loaded shapefile from {shp_path}")
        except Exception as e:
            print(f"Error loading shapefile: {e}")
            raise
    def plot_shapefile(self, ax):  
        try:
             
            ax.set_yticks([]) 
            ax.set_yticklabels([]) 
            ax.set_xticks([]) 
            ax.set_xticklabels([])
            
            self.world_map.boundary.plot(ax=ax,edgecolor="black", alpha=0.4)
            
            if self.default_xlim is None or self.default_ylim is None:
                self.default_xlim = ax.get_xlim()
                self.default_ylim = ax.get_ylim()     
            return True
        except Exception as e:
            print(f"Error plotting shapefile: {e}")
            return False
    def overlay_tif(self, ax, tif_path):
        try:
            with rasterio.open(tif_path) as src:
                tif_crs = src.crs
                world_crs = self.world_map.crs
                
                if tif_crs != world_crs:
                    transform, width, height = calculate_default_transform(
                        tif_crs, world_crs, src.width, src.height, *src.bounds
                    )
                    kwargs = src.meta.copy()
                    kwargs.update({
                        "crs": world_crs,
                        "transform": transform,
                        "width": width,
                        "height": height
                    }) 
                    reprojected_tif = "reprojected_" + os.path.basename(tif_path)
                    with rasterio.open(reprojected_tif, "w", **kwargs) as dst:
                        for i in range(1, src.count + 1):
                            reproject(
                                source=rasterio.band(src, i),
                                destination=rasterio.band(dst, i),
                                src_transform=src.transform,
                                src_crs=src.crs,
                                dst_transform=transform,
                                dst_crs=world_crs,
                                resampling=Resampling.nearest
                            )
                    src = rasterio.open(reprojected_tif)
                    
                # Get the bounds of the TIF file
                minx, miny, maxx, maxy = transform_bounds(src.crs, world_crs, *src.bounds)
                
                # Show the TIF overlay
                show(src, ax=ax, cmap="gray", alpha=0.6, extent=[minx, maxx, miny, maxy])
                
                # Add padding to the zoom (10% of the TIF dimensions)
                x_padding = (maxx - minx) * 0.1
                y_padding = (maxy - miny) * 0.1
                
                # Set the axis limits to zoom to the TIF location with padding
                ax.set_xlim([minx - x_padding, maxx + x_padding])
                ax.set_ylim([miny - y_padding, maxy + y_padding])
                
                # Maintain aspect ratio
                ax.set_aspect('auto')
                
                # Clean up temporary file if it exists
                #if 'reprojected_' in tif_path:
                    #try:
                      #  os.remove(reprojected_tif)
                   # except:
                     #   pass
                    
                return True
                
        except Exception as e:
            print(f"Error overlaying TIF: {e}")
            return False
    def calculate_distance(self, point1, point2):
        try:
            transformer = Transformer.from_crs(self.world_map.crs, "EPSG:4326", always_xy=True)
            lon1, lat1 = transformer.transform(point1[0], point1[1])
            lon2, lat2 = transformer.transform(point2[0], point2[1])
            distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
            return distance * 1000  
        except Exception as e:
            print(f"Error calculating distance: {e}")
            raise