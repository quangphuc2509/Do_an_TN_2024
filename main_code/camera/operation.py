import cv2
import time
import numpy as np
from detect_marker import *

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

aruco_type = "DICT_ARUCO_ORIGINAL"

def main():
    pre_time = time.time()
    
    print(f"detect {aruco_type} marker")
    
    # Khai báo thư viện mã aruco sẽ sử dụng
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
    
    aruco_para = cv2.aruco.DetectorParameters()
    
    capture = cv2.VideoCapture(1,apiPreference = cv2.CAP_DSHOW)
    
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while (capture.isOpened):
        
        current_time = time.time()
        
        ret, frame = capture.read()
        
        frame_clean = frame.copy()
        
        marker_conners, id_list = Get_markers(frame, aruco_dict, aruco_para)
        
        left_corner, id_corner = Get_Marker_Coordinate(markers= marker_conners, ids= id_list, point = 0)
        
        draw_marker(frame, marker_conners, id_list)
        center_marker = get_Marker_Center_Coordinate(marker_conners)
        
        frame_with_square, squarefound = draw_field(frame, center_marker, id_list)
        
        if squarefound:
            square_corner_point = center_marker
        
        rect = identiify_corner(center_corner= np.array(square_corner_point))
        
        img_rect = four_point_transform(frame_clean, np.array(square_corner_point))
                                    
        if ((current_time - pre_time) >= 0.5):
            
            print(f"corners: \n{center_marker} \n id list: {id_list}")
            print(f"id theo thu tu \n{rect}")
            print("-----------------------------------------")
            
            pre_time = current_time
            
        cv2.imshow("video", frame_with_square)
        cv2.imshow("hinh zuong ne", img_rect)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    
    cv2.destroyAllWindows()
    capture.release()
    
if __name__ == '__main__':
    main()
    
    