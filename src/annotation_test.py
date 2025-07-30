import hylite
from hylite import io
import cv2

if __name__ == '__main__':
    # Load the data
    rgb = io.load('/Users/nova98/Documents/Nova/Spectrolysis/raw_data_car2car/Sisurock/20241211_Car2Car.shed/Car2Car_Table_14.hyc/b1_1_2.hyc/annotated.hyc/S1.hyc/RGB.hdr')
    fenix = io.load('/Users/nova98/Documents/Nova/Spectrolysis/raw_data_car2car/Sisurock/20241211_Car2Car.shed/Car2Car_Table_14.hyc/b1_1_2.hyc/annotated.hyc/S1.hyc/FENIX.hdr')
    rgb_image = rgb.data.astype('uint8')
    rgb.quick_plot()
    # cv2.imshow('rgb',rgb_image)
    # # cv2.imshow('fenix',rgb.data)
    # cv2.waitKey(0)

    # # closing all open windows
    # cv2.destroyAllWindows()