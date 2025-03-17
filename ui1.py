from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
from correct_code import MapPlotter

class BackgroundWidget(QtWidgets.QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            painter.drawPixmap(self.rect(), scaled_pixmap)
class Ui_MainWindow(object):
    def __init__(self):
        self.map_plotter = None
        self.figure = None
        self.canvas = None
        self.points = []
        self.line = None
        self.tif_files = []
        self.dragging = False
        self.last_x = 0
        self.last_y = 0
        self.point_markers = []
        self.distance_label = None
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)    
        self.centralwidget = BackgroundWidget(r"C:\Users\chpch\Downloads\vivid-blurred-colorful-background.jpg", MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.title_label = QtWidgets.QLabel("Interactive World Map Viewer", self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(10, 10, 1580, 60))  # Adjusted width and position
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
                background-color: rgba(33, 150, 243, 0.9);
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
            }
        """) 
         

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 90, 391, 571))
        self.verticalLayout_3_main = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3_main.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3_main.setSpacing(20)
        self.points_group = QtWidgets.QGroupBox("Coordinates")
        self.points_group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #2196F3;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #2196F3;
                font-weight: bold;
            }
        """)
        
        points_layout = QtWidgets.QVBoxLayout(self.points_group)
        
       
        point_labels = QtWidgets.QHBoxLayout()
        source_label = QtWidgets.QLabel("Source Point:")
        dest_label = QtWidgets.QLabel("Destination Point:")
        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #333333;
                padding: 5px;
            }
        """
        source_label.setStyleSheet(label_style)
        dest_label.setStyleSheet(label_style)
        point_labels.addWidget(source_label)
        point_labels.addWidget(dest_label)
        points_layout.addLayout(point_labels)
        
       
        points_input = QtWidgets.QHBoxLayout()
        self.point1_edit = QtWidgets.QLineEdit()
        self.point2_edit = QtWidgets.QLineEdit()
        input_style = """
            QLineEdit {
                background: white;
                padding: 8px;
                border: 2px solid #BBDEFB;
                border-radius: 5px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """
        self.point1_edit.setStyleSheet(input_style)
        self.point2_edit.setStyleSheet(input_style)
        points_input.addWidget(self.point1_edit)
        points_input.addWidget(self.point2_edit)
        points_layout.addLayout(points_input)
        
        
        self.distance_button = QtWidgets.QPushButton("Calculate Distance")
        self.distance_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        points_layout.addWidget(self.distance_button)
        
        self.verticalLayout_3_main.addWidget(self.points_group)
        
        
        tif_group = QtWidgets.QGroupBox("TIF Layer Controls")
        tif_group.setStyleSheet(self.points_group.styleSheet())
        tif_layout = QtWidgets.QVBoxLayout(tif_group)
        
        
        self.tif_button = QtWidgets.QPushButton("Select TIF File")
        self.submit_button = QtWidgets.QPushButton("Apply TIF Overlay")
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """
        self.tif_button.setStyleSheet(button_style)
        self.submit_button.setStyleSheet(button_style)
        tif_layout.addWidget(self.tif_button)
        tif_layout.addWidget(self.submit_button)
        
        self.verticalLayout_3_main.addWidget(tif_group)
        self.reset_button = QtWidgets.QPushButton("Reset View")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F4511E;
            }
            QPushButton:pressed {
                background-color: #E64A19;
            }
        """)
        self.verticalLayout_3_main.addWidget(self.reset_button)
        
         
        self.reset_button.clicked.connect(self.reset_view)
        self.points_clear_button = QtWidgets.QPushButton("Clear Points")
        self.points_clear_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F4511E;
            }
            QPushButton:pressed {
                background-color: #E64A19;
            }
        """)
        self.verticalLayout_3_main.addWidget(self.points_clear_button)
        self.points_clear_button.clicked.connect(self.clear_points)
        
         
        self.figure = Figure(figsize=(14, 10), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(410, 90, 1150, 800))  
        
         
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setMouseTracking(True)
        
       
        self.distance_button.clicked.connect(self.calculate_distance)
        self.tif_button.clicked.connect(self.select_tif_file)
        self.submit_button.clicked.connect(self.submit_data)
        
         
        self.canvas.mpl_connect('scroll_event', self.handle_zoom)
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        
        self.initialize_map()
        
        
        
       
    def clear_points(self):
        pass
        try:
            ax=self.figure.gca()
            
            for marker in self.point_markers:
                if marker in ax.lines:
                    marker.remove()
            self.point_markers.clear()
            if self.line and self.line in ax.lines:
                self.line.remove()
                self.line=None
            if self.distance_label and self.distance_label in ax.texts:
                self.distance_label.remove()
                self.distance_label=None
            ax.set_aspect("auto")
            self.canvas.draw()
        except Exception as e:
            print(f"Error in clear_points: {e}")
        
    def reset_view(self):
        try:
            
            self.figure.clear()  
            ax = self.figure.add_subplot(111)  

            
            self.point1_edit.clear()
            self.point2_edit.clear()

            
            self.point_markers.clear()
            self.line = None
            self.distance_label = None
            self.tif_files.clear()

          
            self.map_plotter.plot_shapefile(ax)
 
            if hasattr(self, "default_xlim") and hasattr(self, "default_ylim"):
                ax.set_xlim(self.default_xlim)
                ax.set_ylim(self.default_ylim)

           
            ax.set_aspect("auto")  
             
            self.canvas.draw()

        except Exception as e:
            print(f"Error in reset_view: {e}")

    def calculate_distance(self):
        
        try:
            if len(self.point_markers) < 2:
                QMessageBox.warning(None, "Error", "Need at least two points to calculate distance")
                return

            point2 = [float(x) for x in self.point2_edit.text().split(',')]
            point1 = [float(x) for x in self.point1_edit.text().split(',')]

            distance = self.map_plotter.calculate_distance(point1, point2)
            ax = self.figure.gca()

            if self.line and self.line in ax.lines:
                self.line.remove()
                self.line = None

           
            if self.distance_label and self.distance_label in ax.texts:
                self.distance_label.remove()
                self.distance_label = None

             
            self.line = ax.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r--', linewidth=2)[0]

            
            mid_point = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]
            self.distance_label = ax.text(mid_point[0], mid_point[1], f'{distance / 1000:.2f} km',
                                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

            self.canvas.draw()

        except ValueError:
            QMessageBox.warning(None, "Error", "Invalid point format. Use 'x,y' format")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error calculating distance: {str(e)}")
     
    
    def on_click(self, event):
         
        if event.button == 1 and event.inaxes:   
            coords = f"{event.xdata:.6f},{event.ydata:.6f}"
            ax = self.figure.gca()
            marker = ax.plot(event.xdata, event.ydata, 'ro', markersize=5)[0]
            self.point_markers.append(marker)
            if len(self.point_markers) >= 2:
                self.point1_edit.setText(self.point2_edit.text())
                self.point2_edit.setText(coords)
            else:
                self.point2_edit.setText(coords)
            self.canvas.draw()
    def handle_zoom(self, event):
            
            ax = self.figure.gca()
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
        
            xdata = event.xdata
            ydata = event.ydata
        
            if not (xdata and ydata):
                return
            
         
            base_scale = 1.1
            if event.button == 'up':
                scale_factor = 1/base_scale
            else:
                scale_factor = base_scale
            
        
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
        
            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * rely])
        
            self.canvas.draw()


     
    def on_mouse_press(self, event):
            
            if event.button == 3:  
                self.dragging = True
                self.last_x = event.x
                self.last_y = event.y

    def on_mouse_release(self, event):
       
        if event.button == 3:
            self.dragging = False

    def on_mouse_move(self, event):
       
        if self.dragging and event.inaxes:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            
            ax = self.figure.gca()
            x_lim = ax.get_xlim()
            y_lim = ax.get_ylim()
            
            x_range = x_lim[1] - x_lim[0]
            y_range = y_lim[1] - y_lim[0]
            
            x_move = -dx * x_range / self.canvas.get_width_height()[0]
            y_move = dy * y_range / self.canvas.get_width_height()[1]
            
            ax.set_xlim(x_lim[0] + x_move, x_lim[1] + x_move)
            ax.set_ylim(y_lim[0] + y_move, y_lim[1] + y_move)
            
            self.canvas.draw()
            
            self.last_x = event.x
            self.last_y = event.y

   


    def initialize_map(self):
        try:
            shapefile_path = r'C:\Users\chpch\Downloads\world-boundaries-SHP\world boundaries SHP\World_Countries_shp.shp'
            self.map_plotter = MapPlotter(shapefile_path)
            ax = self.figure.add_subplot(111)

            # Plot the shapefile
            self.map_plotter.plot_shapefile(ax)

            # Get the bounding box of the plotted map
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()

            # Adjust limits to ensure the map fits perfectly
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

            # Set the aspect ratio to 'auto' so the map stretches to fit
            ax.set_aspect('auto')

            # Remove extra white spaces
            self.figure.tight_layout()
            #plt.tight_layout()

            # Redraw canvas
            self.canvas.draw()
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to load map: {str(e)}")


    def select_tif_file(self):
        
        file_names, _ = QFileDialog.getOpenFileNames(
            None,
            "Select TIF Files",
            "",
            "TIF Files (*.tif *.tiff)"
        )
        if file_names:
            self.tif_files.extend(file_names)
            QMessageBox.information(None, "Success", f"Selected {len(file_names)} file(s)")

    def submit_data(self):
        """Process and display the selected TIF files"""
        if not self.tif_files:
            QMessageBox.warning(None, "Warning", "Please select TIF files first")
            return
            
        try:
            ax = self.figure.gca()
            self.map_plotter.plot_shapefile(ax)
            
            for tif_file in self.tif_files:
                self.map_plotter.overlay_tif(ax, tif_file)
            
            self.canvas.draw()
            QMessageBox.information(None, "Success", "TIF files overlaid successfully")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error processing TIF files: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
        
        
    app.setStyle("Fusion")
        
        
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
     