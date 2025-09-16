from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
import sys
from .point_sensor import *

# Creating the main window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PeakViz"
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.show()

# Creating tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tab1 = PointSensor()
        # self.tab2 = ImagingSensor()
        # Add tabs
        self.tabs.addTab(self.tab1, "Point Sensors")
        # self.tabs.addTab(self.tab2, "Imaging Sensors")
        # Set style for tabs
        self.tabs.setStyleSheet("""
            QTabBar::tab:selected {background: #00aa00; color: black;}
            QTabBar::tab:!selected {background: lightgray; color: black;}
        """)
        # self.new_window = None
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

def main():
    print('Starting GUI')
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
