import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import xml.etree.ElementTree as ET
from shapely.geometry import Point
from rasterio.plot import show
from rasterio.warp import transform_bounds, calculate_default_transform, reproject, Resampling


shp_path1 = r'C:\Users\chpch\Downloads\world-boundaries-SHP\world boundaries SHP\World_Countries_shp.shp'  # World shapefile
gpx_file_path = r"C:\Users\chpch\Downloads\output4.gpx"
tif_path = r"C:\Users\chpch\Downloads\twow.tif"

 
world_map = gpd.read_file(shp_path1)

 
fig, ax = plt.subplots(figsize=(12, 8))
world_map.boundary.plot(ax=ax, edgecolor="black", alpha=0.4)   
ax.set_title("TIFF Overlay on Gujarat Using GPX Coordinates", fontsize=14)

def get_gpx_coordinates(gpx_file_path):
    """Extracts the first lat/lon coordinate from the GPX file."""
    try:
        tree = ET.parse(gpx_file_path)
        root = tree.getroot()

        for trkpt in root.iter("{http://www.topografix.com/GPX/1/1}trkpt"):  
            lat = float(trkpt.attrib["lat"])
            lon = float(trkpt.attrib["lon"])
            return lon, lat   

    except ET.ParseError as e:
        print(f"Error parsing GPX file: {e}")
    except FileNotFoundError:
        print(f"GPX file not found: {gpx_file_path}")

    return None

 
gpx_coord = get_gpx_coordinates(gpx_file_path)
if gpx_coord:
    gpx_lon, gpx_lat = gpx_coord
    print(f"GPX Reference Coordinate: Longitude={gpx_lon}, Latitude={gpx_lat}")

    
    with rasterio.open(tif_path) as src:
        tif_crs = src.crs.to_string()
        world_crs = world_map.crs.to_string()
        print(tif_crs)
        print(world_crs)

         
        if tif_crs != world_crs:
            transform, width, height = calculate_default_transform(
                src.crs, world_map.crs, src.width, src.height, *src.bounds)
            
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': world_map.crs,
                'transform': transform,
                'width': width,
                'height': height
            })
            
             
            with rasterio.open("reprojected.tif", "w", **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=world_map.crs,
                        resampling=Resampling.nearest)
            
            src = rasterio.open("reprojected.tif")  

         
        minx, miny, maxx, maxy = transform_bounds(src.crs, world_map.crs, *src.bounds)

    
        tif_extent = [
            gpx_lon,               
            gpx_lon + (maxx - minx),   
            gpx_lat,               
            gpx_lat + (maxy - miny)   
        ]

         
        show(src, ax=ax, cmap="gray", alpha=0.6, extent=tif_extent)

 
ax.set_xlim(world_map.total_bounds[0], world_map.total_bounds[2])
ax.set_ylim(world_map.total_bounds[1], world_map.total_bounds[3])

 
plt.show()
