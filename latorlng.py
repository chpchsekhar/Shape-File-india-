import geopandas as gpd
import matplotlib.pyplot as plt

# Load shapefile
gdf = gpd.read_file(r'C:\Users\chpch\OneDrive\Desktop\shape_file_data\gadm41_IND_2.shp')

# Ensure it's in latitude/longitude (WGS 84)
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs(epsg=4326)

# Plot the map
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color="lightgray", edgecolor="black")

# Get coordinates by clicking on the map
print("Click on a point in the map...")
coords = plt.ginput(1)  # User clicks on one point, stores (x, y) coordinates
plt.show()

# Extract x and y from clicked point
x, y = coords[0]

# Print real-world latitude & longitude
print(f"Selected Coordinates: Longitude = {x}, Latitude = {y}")
