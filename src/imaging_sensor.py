import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .dataloader import *
from .vizualization import *
from .pre_processing import *
from hylite import HyImage

class ImagingSensor(QScrollArea):
    def __init__(self):
        super(ImagingSensor, self).__init__()
        self.widget1 = QWidget()
        layout1 = QGridLayout(self.widget1)
        layout1.setAlignment(Qt.AlignTop)

        self.image_folder = None
        self.averaged_df = None
        self.batchname = ""
        self.sensor = ""
        self.output_path = None
        self.header_files = None
        self.hylib_dict = None
        self.lib_path = None
        self.library_df = None
        self.spectrum_paths = None
        self.refSpectrum_df = None
        self.rescaling_flag = False
        self.download_flag = False

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)  

         # Select image folder for creating 'masked_spectrum'
        self.label1 = QLabel(self.widget1)
        self.label1.setObjectName('Select image folder (i.e b1.1.2.hyc) for creating "masked_spectrum"')
        self.label1.setText('Select image folder (i.e b1.1.2.hyc) for creating "masked_spectrum"')  
        self.label1.setFont(font)
        self.label1.setGeometry(QRect(10, 20, 455, 20))

        # Button for loading folder and creating 
        self.btn1 = QPushButton(self.widget1)
        self.btn1.setObjectName('Load Folder')
        self.btn1.setText('Load Folder')
        self.btn1.setGeometry(QRect(10, 50, 130, 40))
        self.btn1.clicked.connect(self.open_image_data)

        # Message for creating "masked_spectrum" folder
        self.label2 = QLabel(self.widget1)
        self.label2.setObjectName('Dataset created')
        self.label2.setText('')
        self.label2.setStyleSheet("border: 0.5px solid gray;")
        self.label2.setGeometry(QRect(150, 55, 130, 30))

        # Select hylib objects from 'masked_spectrum'
        self.label3 = QLabel(self.widget1)
        self.label3.setObjectName('Select hylib objects from "masked_spectrum" (Optional)')
        self.label3.setText('Select hylib objects from "masked_spectrum" (Optional)')  
        self.label3.setFont(font)
        self.label3.setGeometry(QRect(10, 105, 455, 20))

        # Button for loading hylib objects 
        self.btn2 = QPushButton(self.widget1)
        self.btn2.setObjectName('Load Hylib')
        self.btn2.setText('Load Hylib')
        self.btn2.setGeometry(QRect(10, 135, 130, 40))
        self.btn2.clicked.connect(self.open_hylib)

        # Message for for loading hylib objects 
        self.label4 = QLabel(self.widget1)
        self.label4.setObjectName('Hylib loaded')
        self.label4.setText('')
        self.label4.setStyleSheet("border: 0.5px solid gray;")
        self.label4.setGeometry(QRect(150, 140, 130, 30))

         # Select Library file
        self.label5 = QLabel(self.widget1)
        self.label5.setObjectName('Select fingerprint library (Optional)')
        self.label5.setText('Select fingerprint library (Optional)')  
        self.label5.setFont(font)
        self.label5.setGeometry(QRect(10, 190, 400, 20))

        # Button for loading Library
        self.btn3 = QPushButton(self.widget1)
        self.btn3.setObjectName('Load Fingerprints')
        self.btn3.setText('Load Fingerprints')
        self.btn3.setGeometry(QRect(10, 220, 130, 40))
        self.btn3.clicked.connect(self.open_library)

        # Message for library files
        self.label6 = QLabel(self.widget1)
        self.label6.setObjectName('Fingerprints loaded')
        self.label6.setText('')
        self.label6.setStyleSheet("border: 0.5px solid gray;")
        self.label6.setGeometry(QRect(150, 225, 130, 30))

         # Select Reference spectrum
        self.label7 = QLabel(self.widget1)
        self.label7.setObjectName('Select Reference spectrum (Optional)')
        self.label7.setText('Select Reference spectrum (Optional)')  
        self.label7.setFont(font)
        self.label7.setGeometry(QRect(10, 275, 420, 20))

        # Button for loading Reference spectrum
        self.btn4 = QPushButton(self.widget1)
        self.btn4.setObjectName('Load Spectrums')
        self.btn4.setText('Load Spectrums')
        self.btn4.setGeometry(QRect(10, 305, 130, 40))
        self.btn4.clicked.connect(self.open_spectrums)

        # Message for Reference spectrum
        self.label8 = QLabel(self.widget1)
        self.label8.setObjectName('Spectrums loaded')
        self.label8.setText('')
        self.label8.setStyleSheet("border: 0.5px solid gray;")
        self.label8.setGeometry(QRect(150, 310, 130, 30))

        # Select pre-processing method
        self.label9 = QLabel(self.widget1)
        self.label9.setObjectName('Select Pre-processing method (Optional)')
        self.label9.setText('Select Pre-processing method (Optional)')  
        self.label9.setFont(font)
        self.label9.setGeometry(QRect(10, 360, 365, 20))

        # creating check box for choosing sensor
        self.checkBoxAbsorbance = QCheckBox("Absorbance", self.widget1) 
        self.checkBoxAbsorbance.setGeometry(10, 390, 160, 30)
        self.checkBoxAbsorbance.stateChanged.connect(self.select_absorbance)

        # Start visualization
        self.label10 = QLabel(self.widget1)
        self.label10.setObjectName('Data visualisation')
        self.label10.setText('Data visualisation')  
        self.label10.setFont(font)
        self.label10.setGeometry(QRect(10, 440, 365, 20))

        # creating check box for choosing sensor
        self.checkBoxDownload = QCheckBox("Download as .html", self.widget1) 
        self.checkBoxDownload.setGeometry(10, 470, 150, 30)
        self.checkBoxDownload.stateChanged.connect(self.select_download)

        # For opening data
        self.btn5 = QPushButton(self.widget1)
        self.btn5.setObjectName('Open Data')
        self.btn5.setText('Open Data')
        self.btn5.setGeometry(QRect(10, 510, 111, 40))
        self.btn5.clicked.connect(self.open_data)

        self.setWidget(self.widget1)
        self.setWidgetResizable(True)
        self.widget1.setLayout(layout1)
        
    def select_sensor(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxSWIR: 
                self.checkBoxMWIR.setChecked(False) 
                self.sensor = 'VNIR_SWIR' 
            elif self.sender() == self.checkBoxMWIR:  
                self.checkBoxSWIR.setChecked(False) 
                self.sensor = 'MWIR_LWIR' 


    def open_image_data(self):
        # Open dialog and get the selected image folder
        self.image_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.image_folder:
            # batchname
            path_components = self.image_folder.split(os.sep)
            last_two = path_components[-2:]
            result = '_'.join(last_two)
            self.batchname = result
            # self.batchname = os.path.join(*os.path.normpath(self.image_folder).split(os.sep)[-2:])
            # For creating undersampled masked image
            create_masked_image(self.image_folder)
            # Create hylib files from the masked area
            # Averaged_df for visualisation
            self.averaged_df = create_masked_spec(self.image_folder)
            self.label2.setText('Dataset created')
            
    def open_hylib(self):
        self.header_files, _ = QFileDialog.getOpenFileNames(self)
        if self.header_files:
            self.sensor = self.header_files[0].split(os.sep)[-2]
            self.output_path, _ = os.path.split(self.header_files[0])
            # self.batchname = os.path.join(*os.path.normpath(self.header_files[0]).split(os.sep)[-2:])
            self.hylib_dict = load_hylib(self.header_files)
            message = "Hylib loaded" if self.hylib_dict is not None else "Error!"
            self.label4.setText(message)
            # self.reflectance_df = load_reflectance(self.reflectance_files)
            # self.label3.setText("Reflectance loaded")
            pass


    # TODO
    # Remove repeatative function as PointSensor
    def open_library(self):
        # Open the file dialog and get the selected excel file
        # Load the file as pandas dataframe
        self.lib_path, _ = QFileDialog.getOpenFileName(self)
        if self.lib_path:
            self.label6.setText("Library loaded")
            self.library_df = pd.read_excel(self.lib_path)

    def open_spectrums(self):
        # Select one or multiple .txt files for reference spectrum
        # Open the file dialog and get the selected .txt files
        # Load the file as pandas dataframe
        self.spectrum_paths, _ = QFileDialog.getOpenFileNames(self)
        if self.spectrum_paths:
            self.refSpectrum_df = load_refSpectrum(self.spectrum_paths)
            self.label8.setText('Spectrums loaded')
        
    # TODO
    # Fix this
    def select_absorbance(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxAbsorbance: 
                self.rescaling_flag = True
                if self.hylib_dict is not None:
                    self.absorbance_df = self.convert_absorbance()

    def convert_absorbance(self):
        new_path = os.path.join(self.output_path, "absorbance")
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        for file_name, df in self.hylib_dict.items():
            # Convert df to HyImage
            hy_image = HyImage(df.values[:, np.newaxis, :])
            absorbance = kubelka_munk_hylite(hy_image)
            absorbance.set_wavelengths(df.columns.tolist())
            new_file = file_name.split(".hdr")[0] + "_absorbance.hdr"
            new_file_path = os.path.join(new_path, new_file)
            if not os.path.exists(new_file_path):
                io.save(new_file_path, absorbance)


        pass
    
    def select_download(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxDownload: 
                self.download_flag = True
            

    def open_data(self):
        viz_image_data(self.batchname, self.hylib_dict, output_path=self.output_path, 
                       sensor=self.sensor, 
                       download=self.download_flag)
        # Check if del obj is possible
        self.hylib_dict = None
        self.label4.setText("")



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())