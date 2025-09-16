import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .dataloader import *
from .vizualization import *
from .pre_processing import *

class PointSensor(QScrollArea):

    def __init__(self):
        super(PointSensor, self).__init__()
        self.widget1 = QWidget()
        layout1 = QGridLayout(self.widget1)
        layout1.setAlignment(Qt.AlignTop)

        self.sensor = None
        self.search_text = None #TODO: make this text from user input
        self.reflectance_files = None
        self.absorbance_files = None
        self.reflectance_df = None
        self.absorbance_df = None
        self.batchname = ''
        self.lib_path = None
        self.library_df = None
        self.spectrum_paths = None
        self.refSpectrum_df = {}
        self.rescaling_flag = False
        self.average_flag = False
        self.reflectance_rescaled_df = None
        self.absorbance_rescaled_df = None
        self.reflectance_averaged_df = None
        self.absorbance_averaged_df = None
        self.download_flag = False
        self.setFixedWidth(500)
        self.setFixedHeight(700)

        # Choose sensor
        self.label1 = QLabel(self.widget1)
        self.label1.setObjectName('Choose point sensor: ')
        self.label1.setText('Choose point sensor: ')
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)  
        self.label1.setFont(font)
        self.label1.setGeometry(QRect(10, 20, 150, 20))


        # creating check box for choosing sensor
        self.checkBoxSWIR = QCheckBox("VNIR/SWIR", self.widget1) 
        self.checkBoxSWIR.setGeometry(10, 50, 100, 20) 
        self.checkBoxMWIR = QCheckBox("MWIR/LWIR", self.widget1) 
        self.checkBoxMWIR.setGeometry(120, 50, 100, 20)

        # calling the uncheck method if any check box state is changed 
        self.checkBoxSWIR.stateChanged.connect(self.select_sensor) 
        self.checkBoxMWIR.stateChanged.connect(self.select_sensor) 

         # Select Reflectance files
        self.label2 = QLabel(self.widget1)
        self.label2.setObjectName('Select single or multiple "Reflectance" files')
        self.label2.setText('Select single or multiple "Reflectance" files')  
        self.label2.setFont(font)
        self.label2.setGeometry(QRect(10, 90, 300, 20))

        # Button for loading Reflectance
        self.btn1 = QPushButton(self.widget1)
        self.btn1.setObjectName('Load Reflectance')
        self.btn1.setText('Load Reflectance')
        self.btn1.setGeometry(QRect(10, 120, 130, 40))
        self.btn1.clicked.connect(self.reflectance_file_dialog)

        # Message for loading Reflectance files
        self.label3 = QLabel(self.widget1)
        self.label3.setObjectName('Reflectance loaded')
        self.label3.setText('')
        self.label3.setStyleSheet("border: 0.5px solid gray;")
        self.label3.setGeometry(QRect(150, 125, 130, 30))


        # Label for renaming files from comment (VNIR/SWIR only)
        self.rename_label = QLabel(self.widget1)
        self.rename_label.setObjectName('Rename files from comment')
        self.rename_label.setText('Rename the files (Only applicable to VNIR/SWIR)')
        self.rename_label.setFont(font)
        self.rename_label.setGeometry(QRect(10, 170, 350, 20))

        # Checkbox for renaming
        self.rename_checkbox = QCheckBox('Rename', self.widget1)
        self.rename_checkbox.setGeometry(QRect(10, 195, 80, 25))
        # self.rename_checkbox.stateChanged.connect(self.select_rename)

        # Save button beside checkbox
        self.save_button = QPushButton('Save', self.widget1)
        self.save_button.setGeometry(QRect(100, 195, 80, 25))
        # self.save_button.clicked.connect(self.rename_files)

        # Select Absorbance files
        self.label4 = QLabel(self.widget1)
        self.label4.setObjectName('Select single or multiple "Absorbance" files (Optional)')
        self.label4.setText('Select single or multiple "Absorbance" files (Optional)')  
        self.label4.setFont(font)
        self.label4.setGeometry(QRect(10, 235, 365, 20))

        # Button for loading Absorbance
        self.btn2 = QPushButton(self.widget1)
        self.btn2.setObjectName('Load Absorbance')
        self.btn2.setText('Load Absorbance')
        self.btn2.setGeometry(QRect(10, 265, 130, 40))
        self.btn2.clicked.connect(self.absorbance_file_dialog)

        # Message for loading Absorbance files
        self.label5 = QLabel(self.widget1)
        self.label5.setObjectName('Absorbance loaded')
        self.label5.setText('')
        self.label5.setStyleSheet("border: 0.5px solid gray;")
        self.label5.setGeometry(QRect(150, 270, 130, 30))

         # Select Library file
        self.label6 = QLabel(self.widget1)
        self.label6.setObjectName('Select fingerprint library for the specified sensor (Optional)')
        self.label6.setText('Select fingerprint library for the specified sensor (Optional)')  
        self.label6.setFont(font)
        self.label6.setGeometry(QRect(10, 310, 400, 20))

        # Button for loading Library
        self.btn3 = QPushButton(self.widget1)
        self.btn3.setObjectName('Load Fingerprints')
        self.btn3.setText('Load Fingerprints')
        self.btn3.setGeometry(QRect(10, 340, 130, 40))
        self.btn3.clicked.connect(self.open_library)

        # Message for library files
        self.label7 = QLabel(self.widget1)
        self.label7.setObjectName('Fingerprints loaded')
        self.label7.setText('')
        self.label7.setStyleSheet("border: 0.5px solid gray;")
        self.label7.setGeometry(QRect(150, 345, 130, 30))

        #### test
         # Select Reference spectrum
        self.label8 = QLabel(self.widget1)
        self.label8.setObjectName('Select Reference spectrum for the specified sensor (Optional)')
        self.label8.setText('Select Reference spectrum for the specified sensor (Optional)')  
        self.label8.setFont(font)
        self.label8.setGeometry(QRect(10, 385, 420, 20))

        # Button for loading Reference spectrum
        self.btn4 = QPushButton(self.widget1)
        self.btn4.setObjectName('Load Spectrums')
        self.btn4.setText('Load Spectrums')
        self.btn4.setGeometry(QRect(10, 415, 130, 40))
        self.btn4.clicked.connect(self.open_refSpectrums)

        # Message for Reference spectrum
        self.label9 = QLabel(self.widget1)
        self.label9.setObjectName('Spectrums loaded')
        self.label9.setText('')
        self.label9.setStyleSheet("border: 0.5px solid gray;")
        self.label9.setGeometry(QRect(150, 420, 130, 30))
        #########

        # Select pre-processing method
        self.label10 = QLabel(self.widget1)
        self.label10.setObjectName('Select Pre-processing method (Optional)')
        self.label10.setText('Select Pre-processing method (Optional)')  
        self.label10.setFont(font)
        self.label10.setGeometry(QRect(10, 460, 365, 20))

        # creating check box for re-scaling
        self.checkBoxRescaling = QCheckBox("Y-axis rescaling", self.widget1) 
        self.checkBoxRescaling.setGeometry(10, 490, 160, 30)
        self.checkBoxRescaling.stateChanged.connect(self.select_rescaling)

        # creating check box for choosing sensor
        self.checkBoxAverage = QCheckBox("Average", self.widget1) 
        self.checkBoxAverage.setGeometry(160, 490, 160, 30)
        self.checkBoxAverage.stateChanged.connect(self.select_average)

        # Start visualization
        self.label11 = QLabel(self.widget1)
        self.label11.setObjectName('Data visualisation')
        self.label11.setText('Data visualisation')  
        self.label11.setFont(font)
        self.label11.setGeometry(QRect(10, 530, 365, 20))

        # creating check box for choosing sensor
        self.checkBoxDownload = QCheckBox("Download as .html", self.widget1) 
        self.checkBoxDownload.setGeometry(10, 560, 150, 30)
        self.checkBoxDownload.stateChanged.connect(self.select_download)

        # For opening data
        self.btn5 = QPushButton(self.widget1)
        self.btn5.setObjectName('Open Data')
        self.btn5.setText('Open Data')
        self.btn5.setGeometry(QRect(10, 590, 111, 40))
        self.btn5.clicked.connect(self.open_data)

        self.setWidget(self.widget1)
        self.setWidgetResizable(True)
        self.widget1.setLayout(layout1)
        
    def select_sensor(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxSWIR: 
                self.checkBoxMWIR.setChecked(False) 
                self.sensor = 'VNIR_SWIR' 
                self.search_text = 'Measurement:'
            elif self.sender() == self.checkBoxMWIR:  
                self.checkBoxSWIR.setChecked(False) 
                self.sensor = 'MWIR_LWIR' 
                self.search_text = 'XYUNITS'

    def create_batchname(self, file_path):
        # Get the batchname
        if self.sensor == 'VNIR_SWIR':
            clock = 3
        elif self.sensor == 'MWIR_LWIR':
            clock = 4
        while clock:
            file_path, folder = os.path.split(file_path)
            clock -= 1
        self.batchname = folder

    
    def reflectance_file_dialog(self):
        # Open the file dialog and get the selected file name
        self.reflectance_files, _ = QFileDialog.getOpenFileNames(self)
        if self.reflectance_files:
            self.reflectance_df, _ = load_data(self.reflectance_files, signal_type='reflectance',
                           search_text= self.search_text)
            message = "Reflectance loaded" if self.reflectance_df is not None else "Error!"
            self.label3.setText(message)
            ###
            if not self.batchname:
                self.create_batchname(self.reflectance_files[0])
        
        
    def absorbance_file_dialog(self):
        # Open the file dialog and get the selected file name
        self.absorbance_files, _ = QFileDialog.getOpenFileNames(self)
        if self.absorbance_files:
            _, self.absorbance_df = load_data(self.absorbance_files, signal_type='absorbance',
                           search_text= self.search_text)
            message = "Absorbance loaded" if self.absorbance_df is not None else "Error!"
            self.label5.setText(message)
            if not self.batchname:
                self.create_batchname(self.absorbance_files[0]) 
            

    def open_library(self):
        # Open the file dialog and get the selected excel file
        # Load the file as pandas dataframe
        self.lib_path, _ = QFileDialog.getOpenFileName(self)
        if self.lib_path:
            self.label7.setText("Library loaded")
            self.library_df = pd.read_excel(self.lib_path)

    def open_refSpectrums(self):
        # Select one or multiple .txt files for reference spectrum
        # Open the file dialog and get the selected .txt files
        # Load the file as pandas dataframe
        self.spectrum_paths, _ = QFileDialog.getOpenFileNames(self)
        if self.spectrum_paths:
            # self.refSpectrum_df = load_refSpectrum(self.spectrum_paths)
            ###
            reflectRef_df, absorbRef_df = load_data(self.spectrum_paths, signal_type='reference',
                           search_text= 'XYUNITS')
            if reflectRef_df is not None:
                # self.reflectance_df = pd.concat([self.reflectance_df, reflectRef_df], axis=0)
                self.refSpectrum_df['Reflectance'] = reflectRef_df
            if absorbRef_df is not None:
                # self.absorbance_df = pd.concat([self.absorbance_df, absorbRef_df], axis=0)
                self.refSpectrum_df['Absorbance'] = absorbRef_df
            ###
            self.label9.setText('Spectrums loaded')
        
    def select_rescaling(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxRescaling: 
                self.rescaling_flag = True
                if self.reflectance_files:
                    self.reflectance_rescaled_df = rescale_data(self.reflectance_df)
                if self.absorbance_files:
                    self.absorbance_rescaled_df = rescale_data(self.absorbance_df)

    def select_average(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxAverage: 
                self.average_flag = True
                if self.reflectance_files:
                    self.reflectance_averaged_df = average_data(self.reflectance_df, 
                                                                self.reflectance_files[0],
                                                                signal_type= 'Reflectance')
                if self.absorbance_files:
                    self.absorbance_averaged_df = average_data(self.absorbance_df, 
                                                               self.absorbance_files[0],
                                                               signal_type= 'Absorbance')

    def select_download(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxDownload: 
                self.download_flag = True
            

    def open_data(self):
        df_plot = {}
        if self.reflectance_files:
            df_plot['Reflectance'] = (self.reflectance_df, 'Reflectance')
        if self.absorbance_files:
            df_plot['Absorbance'] = (self.absorbance_df, 'Absorbance')
        if self.rescaling_flag:
            df_plot['Reflectance (Re-scaled)'] = (self.reflectance_rescaled_df, 'Reflectance')
            df_plot['Absorbance (Re-scaled)'] = (self.absorbance_rescaled_df, 'Absorbance')
            pass

        # This creates vizualization to plot multiple data
        viz(self.batchname, df_plot, fingerprint_library=self.library_df, 
            reference_Spectrums=self.refSpectrum_df,
            sensor=self.sensor, download=self.download_flag)
        # Check if del obj is possible
        self.reflectance_files = None
        self.absorbance_files = None
        self.reflectance_df = None
        self.absorbance_df = None
        self.batchname = None
        # self.library_df = None
        # self.rescaling_flag = False
        self.reflectance_rescaled_df = None
        self.absorbance_rescaled_df = None
        # self.download_flag = False
        self.label3.setText("")
        self.label5.setText("")
        self.label9.setText("")
        # self.label7.setText("")
        # if hasattr(self, 'downloadCheckBox'):
        self.checkBoxDownload.setChecked(False)
        # if hasattr(self, 'averageCheckBox'):
        self.checkBoxAverage.setChecked(False)



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())