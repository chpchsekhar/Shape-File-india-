import geopandas as gpd
from matplotlib import pyplot as plt


india =gpd.read_file(r'C:\Users\chpch\OneDrive\Desktop\shape_file_data\gadm41_IND_0.shp')
india1=gpd.read_file(r'C:\Users\chpch\OneDrive\Desktop\shape_file_data\gadm41_IND_1.shp')
india2=gpd.read_file(r'C:\Users\chpch\OneDrive\Desktop\shape_file_data\gadm41_IND_2.shp')
#india=india.to_crs(epsg=3857) #converting the crs to 3857 -> merccator projection
print(india.crs)
print(india1.crs)
print(india2.crs)
#print(india.crs)
#print(india.head())
print(india.geometry)
#for 
#ndia.plot(figsize=(10,10),edgecolor='black',cmap='hsv',column='GID_0')
#plt.show()

#india1.plot(figsize=(10,10),edgecolor='black',cmap='jet',column='GID_1')
#plt.show()

#india2.plot(figsize=(10,10),edgecolor='black',cmap='jet',column='GID_2')
#plt.show()

#fig,(ax1,ax2,ax3)=plt.subplots(ncols=3,figsize=(15,15)) 

# Load shape files
 
# Print CRS information
print("CRS Information:")
print("India:", india.crs)
print("India1:", india1.crs)
print("India2:", india2.crs)

# Create a figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(15, 15))

# Plot each shape file on a separate subplot
india.plot(ax=ax1, edgecolor='black', cmap='jet', column='GID_0')
ax1.set_title('India')

india1.plot(ax=ax2, edgecolor='black', cmap='jet', column='GID_1')
ax2.set_title('India1')

india2.plot(ax=ax3, edgecolor='black', cmap='jet', column='GID_2')
ax3.set_title('India2')

# Layout so plots do not overlap
fig.tight_layout()

# Show the plot
plt.show()
india.plot(ax=ax1,figsize=(10,10),edgecolor='black',cmap='jet',column='GID_0')
india1.plot(ax=ax2,figsize=(10,10),edgecolor='black',cmap='jet',column='GID_1')
india2.plot(ax=ax3,figsize=(10,10),edgecolor='black',cmap='jet',column='GID_2')
plt.show()
plt.show()
plt.show()
