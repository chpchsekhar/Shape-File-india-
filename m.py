from matplotlib import pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import gpxpy
import gpxpy.gpx
import numpy as np
import xml.etree.ElementTree as ET
from shapely.geometry import LineString

# Load India shapefile
india = gpd.read_file(r'C:\Users\chpch\Downloads\world-boundaries-SHP\world boundaries SHP\World_Countries_shp.shp')

if india.crs != 'epsg:4326':
    india = india.to_crs(epsg=4326)

# Create figure
fig, ax = plt.subplots(figsize=(10, 10))
india.plot(ax=ax, edgecolor='black', color='white')
ax.set_title('India')

# Initialize variables
clicked_points = []
scatter_objects = []
line_object = None
distance_label = None
dragging_point = None

# Function to calculate distance
def calculate_distance(p1, p2):
    coords_1 = (p1.y, p1.x)
    coords_2 = (p2.y, p2.x)
    return geodesic(coords_1, coords_2).kilometers

# Function to find the nearest point
def find_nearest_point(event):
    threshold = 0.5  # Distance threshold
    for i, pt in enumerate(clicked_points):
        dist = np.sqrt((event.xdata - pt.x)**2 + (event.ydata - pt.y)**2)
        if dist < threshold:
            return i
    return None

# Function to handle mouse clicks
def onclick(event):
    global line_object, distance_label, dragging_point

    if event.xdata is None or event.ydata is None:
        return

    if event.button == 1:  # Left click - add point
        new_point = Point(event.xdata, event.ydata)

        if len(clicked_points) == 2:
            clicked_points.pop(0)
            scatter_objects.pop(0).remove()
            if line_object:
                line_object.remove()
            if distance_label:
                distance_label.remove()

        clicked_points.append(new_point)
        scatter = ax.scatter(event.xdata, event.ydata, color='red', marker='o', s=30, picker=True)
        scatter_objects.append(scatter)

        print(f"Point placed: Longitude {event.xdata}, Latitude {event.ydata}")

        if len(clicked_points) == 2:
            p1, p2 = clicked_points
            distance = calculate_distance(p1, p2)
            print(f"Distance between points: {distance:.2f} km")

            line_object, = ax.plot([p1.x, p2.x], [p1.y, p2.y], color='orange', linestyle='--', linewidth=1)

            mid_x, mid_y = (p1.x + p2.x) / 2, (p1.y + p2.y) / 2
            distance_label = ax.text(mid_x, mid_y, f"{distance:.2f} km", fontsize=8, color='green', ha='left')

        fig.canvas.draw()

    elif event.button == 3:  # Right click - drag point
        index = find_nearest_point(event)
        if index is not None:
            dragging_point = index

# Function to handle point dragging
def onmotion(event):
    global dragging_point, line_object, distance_label

    if dragging_point is None or event.xdata is None or event.ydata is None:
        return

    clicked_points[dragging_point] = Point(event.xdata, event.ydata)
    scatter_objects[dragging_point].set_offsets([[event.xdata, event.ydata]])

    if len(clicked_points) == 2:
        p1, p2 = clicked_points
        if line_object:
            line_object.set_data([p1.x, p2.x], [p1.y, p2.y])

        if distance_label:
            distance_label.set_position(((p1.x + p2.x) / 2, (p1.y + p2.y) / 2))
            distance_label.set_text(f"{calculate_distance(p1, p2):.2f} km")

    fig.canvas.draw()

# Function to release dragging
def onrelease(event):
    global dragging_point
    dragging_point = None

# Function to handle zooming
def onscroll(event):
    if event.xdata is None or event.ydata is None:
        return
    scale_factor = 1.2
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    x_range, y_range = (xlim[1] - xlim[0]) / scale_factor, (ylim[1] - ylim[0]) / scale_factor

    if event.step > 0:  # Zoom in
        ax.set_xlim(event.xdata - x_range / 2, event.xdata + x_range / 2)
        ax.set_ylim(event.ydata - y_range / 2, event.ydata + y_range / 2)
    else:  # Zoom out
        ax.set_xlim(event.xdata - x_range * 2, event.xdata + x_range * 2)
        ax.set_ylim(event.ydata - y_range * 2, event.ydata + y_range * 2)

    fig.canvas.draw()

# Load GPX file and extract points
gpx_file_path = r'output2.gpx'
gpx_points = []

with open(gpx_file_path, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx_points.append(Point(point.longitude, point.latitude))  # Convert to (x, y)

 
gpx_scatter = ax.scatter(
    [pt.x for pt in gpx_points], [pt.y for pt in gpx_points], 
    color='green', marker='x', s=30, label="GPX given location"
)

ax.legend()

# Connect event listeners
fig.canvas.mpl_connect('scroll_event', onscroll)
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('motion_notify_event', onmotion)
fig.canvas.mpl_connect('button_release_event', onrelease)
gpx_file_path = r"C:\Users\chpch\Downloads\output1.gpx"
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
    gdf.plot(ax=ax,  edgecolor="black", alpha=0.1,facecolor='blue', legend=True) 
    plt.show()

plot_gpx_track(gpx_file_path)

plt.show()
