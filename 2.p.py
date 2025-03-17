import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import numpy as np
import xml.etree.ElementTree as ET
from shapely.geometry import Point, LineString
import matplotlib.ticker as mticker
from geopy.distance import geodesic
from rasterio.plot import show

# File Paths
shp_path1 = r'C:\Users\chpch\OneDrive\Desktop\shape_file_data\gadm41_IND_0.shp'
shp_path2 = r'C:\Users\chpch\Downloads\world-boundaries-SHP\world boundaries SHP\World_Countries_shp.shp'
gpx_file_path = r"C:\Users\chpch\Downloads\output1.gpx"
tif_path = r"C:\Users\chpch\Downloads\twow.tif"

# Load Shapefiles
ind = gpd.read_file(shp_path1)
ind2 = gpd.read_file(shp_path2)

# Initialize Plot
fig, ax = plt.subplots(figsize=(10, 10))
ind2.plot(ax=ax, edgecolor="black", alpha=0.5, facecolor='none', legend=True)
ind.plot(ax=ax, edgecolor="black", alpha=0.7, facecolor='none', legend=True)
ax.set_title("Overlay of Gujarat TIFF on India and World Map")

# Load and Display TIFF File
with rasterio.open(tif_path) as src:
    show(src, ax=ax, cmap="gray", alpha=0.6)

# Ensure proper coordinate formatting
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.5f'))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.5f'))

# Interactive Zooming
def on_scroll(event):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zoom_factor = 1.2 if event.step < 0 else 1 / 1.2
    ax.set_xlim([event.xdata - (event.xdata - xlim[0]) * zoom_factor,
                 event.xdata + (xlim[1] - event.xdata) * zoom_factor])
    ax.set_ylim([event.ydata - (event.ydata - ylim[0]) * zoom_factor,
                 event.ydata + (ylim[1] - event.ydata) * zoom_factor])
    plt.draw()

fig.canvas.mpl_connect("scroll_event", on_scroll)

# Interactive Click for Distance Calculation
clicked_points = []
scatter_plots = []
line_plot = None
distance_text = None

def on_click(event):
    global line_plot, distance_text
    if event.xdata is not None and event.ydata is not None:
        lon, lat = event.xdata, event.ydata
        clicked_points.append((lat, lon))

        scatter = ax.scatter(lon, lat, color='gray', marker='o', s=30)
        scatter_plots.append(scatter)

        print("Clicked Points:", clicked_points)

        if len(clicked_points) > 1:
            lat1, lon1 = clicked_points[-2]
            lat2, lon2 = clicked_points[-1]
            dist = geodesic((lat1, lon1), (lat2, lon2)).kilometers
            print(f"Distance between {clicked_points[-2]} and {clicked_points[-1]}: {dist:.3f} km")

            if line_plot:
                line_plot[0].remove()
            if distance_text:
                distance_text.remove()

            line_plot = ax.plot([lon1, lon2], [lat1, lat2], color='red', linestyle='--', linewidth=2)

            mid_lat = (lat1 + lat2) / 2
            mid_lon = (lon1 + lon2) / 2
            distance_text = ax.text(mid_lon, mid_lat, f"{dist:.2f} km", fontsize=12, color='black',
                                    ha='right', va='baseline', bbox=dict(facecolor='none', alpha=0))
        plt.draw()

fig.canvas.mpl_connect("button_press_event", on_click)

# GPX Track Plotting
def plot_gpx_track(gpx_file_path):
    points = []
    try:
        context = ET.iterparse(gpx_file_path, events=("start", "end"))
        for event, elem in context:
            if event == "end" and elem.tag.endswith("trkpt"):
                lat = float(elem.attrib["lat"])
                lon = float(elem.attrib["lon"])
                points.append(Point(lon, lat))
                elem.clear()
    except ET.ParseError as e:
        print(f"Error parsing GPX file: {e}")
        return
    except FileNotFoundError:
        print(f"Could not find file: {gpx_file_path}")
        return

    if not points:
        print("No points found in the GPX file.")
        return

    gdf = gpd.GeoDataFrame(geometry=[LineString(points)], crs="EPSG:4326")
    gdf.plot(ax=ax, edgecolor="blue", alpha=0.7, linewidth=2, label="GPX Track")
    plt.draw()

plot_gpx_track(gpx_file_path)

plt.show()
