import cv2
import time
import numpy as np
from detect_marker import *
import matplotlib.pyplot as plt

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

def center_point(x_list, y_list):
    count = 0
    mang = []
    x_average_list = []
    for x_point, y_point in zip(x_list, y_list):
        x_array = np.array(x_point)
        y_array = np.array(y_point)
        
        if not np.all(x_array == 0) or not np.all(y_array == 0):
            # print(f"x_array: {x_array}\ny_array: {y_array}")
            x_average = int(np.nanmean(x_array[:]))
            y_average = int(np.nanmean(y_array[:]))
        # print(f"y_average: {y_average}")
        # if x_average != x_average:
        # else:
            mang.append((x_average, y_average))
            x_average_list.append(x_average)
    return mang, x_average_list

def event_mouse(event, x, y, flag, para):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"toa do (x,y): {x},{y}")

def max_difference(arr):
    if len(arr) < 2:
        raise ValueError("Array must have at least two elements")

    # Chuyển đổi danh sách sang mảng NumPy
    np_arr = np.array(arr)
    
    # Tính toán sự chênh lệch giữa các phần tử cạnh nhau
    diff = np.abs(np.diff(np_arr))
    
    # Trả về giá trị lớn nhất của sự chênh lệch
    return np.max(diff), diff

def line_detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 60, 200, apertureSize=3)
    
    # Initialize variables for curve points
    curves = []
    x_list = []
    y_list = []
    
    height = edges.shape[0]
    width  = edges.shape[1]    
    print(f"edge \n {edges.shape}")
    
    for y in range(height):
        x = 0
        x_point = []
        y_point = []
        edge_found = False
        while x < width:
            if edges[y, x] != 0:
                # Found an edge pixel
                x_point.append(x)
                y_point.append(y)
                edge_found = True         
                # Skip pixels of the same edge
                while x < width  and edges[y, x] != 0:
                    x += 1
                x_point.append(x)
                y_point.append(y)
                
            if not edge_found:
                x += 1
            edge_found = False
    
        x_list.append(x_point)
        y_list.append(y_point)
    
    curves_1, x_average_list = center_point(x_list=x_list, y_list= y_list)
    max_diff, diff = max_difference(x_average_list)
    print(f"diff_list: \n{diff}")

    print("Sự chênh lệch lớn nhất giữa các phần tử cạnh nhau là:", max_diff)
    # Simplify the collected points
    simplified_curves = []
    if curves_1:
        simplified_curves.append(curves_1[0])  # Add the first point
        for i in range(1, len(curves_1)):
            if curves_1[i][1] != simplified_curves[-1][1]:  # Check if y-coordinate changes
                simplified_curves.append(curves_1[i])

    # Draw the curves on a blank image
    curve_image = np.zeros_like(edges)
    count = 0
    for curve in simplified_curves:
        # if (curve != curve):
        # print(f"curve {count}: {curve}")
        cv2.circle(curve_image, curve, 1, 255, -1)  # Draw a circle at the midpoint
        count = count +1

    return curve_image


def main():
    pre_time = time.time()
    
     # Khai báo thư viện mã aruco sẽ sử dụng
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
    aruco_para = cv2.aruco.DetectorParameters()
    
    url = r"F:\DATN_HK2_2024\camera_img\linearuco.jpg"
    image = cv2.imread(url)
    scale = 0.9
    
    image_clean = image.copy()
    
    marker_corners, id_list = Get_markers(image, aruco_dict= aruco_dict, aruco_para= aruco_para)
    
    draw_marker(image, marker_corners, id_list)
    center_marker = get_Marker_Center_Coordinate(marker_corners)
    
    img_with_square, square_found = draw_field(image, center_marker, id_list)
    
    if square_found:
        square_corner_point = center_marker
    
    rect = identiify_corner(center_corner=np.array(square_corner_point))
    
    img_rect = four_point_transform(image_clean, np.array(square_corner_point))
    
    curver_img = line_detect(img= img_rect)
    
    print(f" marker_corners: {marker_corners}")
    print(f"id: {id_list}")
    print(f"id theo thu tu \n{rect}")
    
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_with_square_rgb = cv2.cvtColor(img_with_square, cv2.COLOR_BGR2RGB)
    img_rect_rgb = cv2.cvtColor(img_rect, cv2.COLOR_BGR2RGB)
    curver_img_rgb = cv2.cvtColor(curver_img, cv2.COLOR_BGR2RGB)
    
    plt.figure()
    plt.subplot(221)
    plt.imshow(img_rgb)
    plt.subplot(222)
    plt.imshow(img_with_square_rgb)
    plt.subplot(223)
    plt.imshow(img_rect_rgb)
    plt.subplot(224)
    plt.imshow(curver_img_rgb)
    
    cv2.imshow("image", img_rect)
    plt.show()

if __name__ == '__main__':
    main()
    