# GeoPandas Visualization Project

This project visualizes geographical data using GeoPandas and Matplotlib. It overlays two shapefiles and allows interactive zooming and clicking to measure distances between points. Additionally, it plots GPX tracks on the map.

## Requirements

- Python 3.6+
- GeoPandas
- Matplotlib
- Shapely
- Geopy
- GPXPy

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required packages:
    ```sh
    pip install geopandas matplotlib shapely geopy gpxpy
    ```

## Usage

1. Place your shapefiles and GPX files in the appropriate directories.
2. Update the file paths in `1.py` to point to your shapefiles and GPX files.
3. Run the script:
    ```sh
    python 1.py
    ```

## Features

- **Overlay Shapefiles**: The script overlays two shapefiles on a Matplotlib plot.
- **Interactive Zoom**: Use the scroll wheel to zoom in and out of the plot.
- **Click to Measure Distance**: Click on the plot to measure the distance between points.
- **Plot GPX Tracks**: Plot GPX tracks on the map.

## File Structure

```
.
├── 1.py
├── 2.p.py
├── 2.py
├── a.py
├── b.py
├── correct_code.py
├── correct_code1.py
├── intro.py
├── latorlng.py
├── m.py
├── output.mp4
├── output2.gpx
├── reprojected_srilanka.tif
├── reprojected.tif
├── sample.py
├── ui.py
├── ui1.py
├── UI2.PY
└── __pycache__/
    ├── b.cpython-311.pyc
    ├── correct_code.cpython-311.pyc
    └── correct_code1.cpython-311.pyc
```

## Example

```python
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.ticker as mticker
from geopy.distance import geodesic
import gpxpy
from shapely.geometry import Point, LineString
import xml.etree.ElementTree as ET

# Load shapefiles
shp_path1 = r'C:\path\to\your\shapefile1.shp'
shp_path2 = r'C:\path\to\your\shapefile2.shp'
ind = gpd.read_file(shp_path1)
ind2 = gpd.read_file(shp_path2)

# Plot shapefiles
fig, ax = plt.subplots(figsize=(10, 10))
ind2.plot(ax=ax, edgecolor="black", alpha=0.5, facecolor='none', legend=True)
ind.plot(ax=ax, edgecolor="black", alpha=0.7, facecolor='none', legend=True)

# Interactive zoom and click events
# ... (rest of the code)
```

## License

This project is licensed under the MIT License.
