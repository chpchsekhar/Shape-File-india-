import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show
from rasterio.warp import transform_bounds, calculate_default_transform, reproject, Resampling
import os
from geopy.distance import geodesic
from shapely.geometry import Point

class MapPlotter:
    def __init__(self, shp_path):
        """Initialize MapPlotter with shapefile path"""
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
        """Plots the shapefile on the given Matplotlib axis."""
        try:
            ax.clear()
            self.world_map.boundary.plot(ax=ax, edgecolor="black", alpha=0.4)
            ax.set_title("Interactive World Map Viewer", pad=20, fontsize=14, fontweight='bold')
            
            # Store default view limits if not already stored
            if self.default_xlim is None or self.default_ylim is None:
                self.default_xlim = ax.get_xlim()
                self.default_ylim = ax.get_ylim()
                
            return True
        except Exception as e:
            print(f"Error plotting shapefile: {e}")
            return False

    def reset_view(self, ax):
        """Reset the view to default limits"""
        if self.default_xlim and self.default_ylim:
            ax.set_xlim(self.default_xlim)
            ax.set_ylim(self.default_ylim)
            return True
        return False

    def overlay_tif(self, ax, tif_path):
        """Overlays a TIF file on the shapefile."""
        try:
            with rasterio.open(tif_path) as src:
                tif_crs = src.crs
                world_crs = self.world_map.crs
                
                # Reproject if necessary
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
                    
                    # Save reprojected TIF
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
                
                # Get TIF extent and overlay on map
                minx, miny, maxx, maxy = transform_bounds(src.crs, world_crs, *src.bounds)
                show(src, ax=ax, cmap="gray", alpha=0.6, extent=[minx, maxx, miny, maxy])
                
                # Reset to default view after overlay
                self.reset_view(ax)
                return True
        except Exception as e:
            print(f"Error overlaying TIF: {e}")
            return False

    def calculate_distance(self, point1, point2):
        """Calculate distance between two points using geopy"""
        try:
            # Convert to lat/lon for geopy
            p1 = self.world_map.geometry.iloc[0].projection_point(Point(point1))
            p2 = self.world_map.geometry.iloc[0].projection_point(Point(point2))
            
            # Calculate distance using geopy
            distance = geodesic((p1.y, p1.x), (p2.y, p2.x)).meters
            return distance
        except Exception as e:
            print(f"Error calculating distance: {e}")
            raise