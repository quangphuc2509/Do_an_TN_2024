import time
import cv2
import numpy as np
import math


# Hàm xác định vị trí pixel và id của mã aruco trên bức ảnh
# ======= Các thông số đầu vào =======
# vid_frame: ảnh từ camera
# aruco_dict: Thư viện mã aruco sử dụng
# aruco_para: Thông số khởi tạo của mã aruco
# ======= Các thông số trả về =======
# coners: Vị trí marker theo pixel trên ảnh
# ids_sorted: mảng 1 chiều chứa id của mã 
def Get_markers(vid_frame, aruco_dict, aruco_para):
    coners, ids, rejected = cv2.aruco.detectMarkers(vid_frame, aruco_dict, parameters = aruco_para)
    if ids is not None:
        ids_sorted = []
        for id_number in ids:
            ids_sorted.append(id_number[0])
    else:
        ids_sorted = ids
    return coners, ids_sorted


def Get_Marker_Coordinate(markers, ids, point):
    marker_array = []
    for marker in markers:
        marker_array.append([int(marker[0][point][0]), int(marker[0][point][1])])
    return marker_array, ids


def get_Marker_Center_Coordinate(corners):
    marker_center_array = []
    for corner in corners:
        corner_reshape = corner.reshape((4, 2))
        # print('corner: {}'.format(corners))
        (topLeft, topRight, bottomRight, bottomLeft) = corner_reshape

        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

        marker_center_array.append([cX,cY])
    
    return marker_center_array

def draw_marker(img, corners, ids):
    if corners:
        for (markerCorner, markerID) in zip(corners, ids):    
            corners = markerCorner.reshape((4, 2))
            # print('corner: {}'.format(corners))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)

            cv2.putText(img, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
    else:
        print("không có marker")
        
def partition(arr, low, high):
    i = (low-1)         
    pivot = arr[high]    

    for j in range(low, high):

        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def quick_sort(arr, low, high):
    if low < high:

        pi = partition(arr, low, high)

        quick_sort(arr, low, pi-1)
        quick_sort(arr, pi+1, high)
        
def draw_field(img, corners, ids):
    if len(corners) == 4:
        markers_sorted = [0,0,0,0]
        ids_sorted = ids[:]
        quick_sort(ids_sorted,0,len(ids_sorted)-1)
        count = 0
        for sorted_corner_id in ids_sorted:
            index = ids.index(sorted_corner_id)
            markers_sorted[count]=corners[index]
            count = count +1
        contours = np.array(markers_sorted)      
        overlay = img.copy()
        cv2.fillPoly(overlay, pts =[contours], color=(255,215,0))
        alpha = 0.4  # Transparency factor.
        # Following line overlays transparent rectangle over the image
        img_new=cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        squarefound=True
    else:
        img_new=img
        squarefound=False
    return img_new,squarefound


# hàm để xác định ra 4 góc của hình chữ nhật theo thứ tự 
# góc hình chữ nhật: trên-trái,  trên-phải, dưới_phải,  dưới-trái 
def identiify_corner(center_corner):
    rect = np.zeros((4,2), dtype= "float32")
    
    # Sử dụng hàm tổng trên từng cặp điểm (x,y) tìm thấy ở các góc
    # cặp điểm nào có tổng bé nhất là tọa độ góc trên - trái
    # cặp điểm nào có tổng lớn nhất là tọa độ góc dưới - phải 
    s = center_corner.sum(axis = 1)         # tổng mảng theo hàng
    rect[0] = center_corner[np.argmin(s)]   # giá trị tọa độ trên-trái
    rect[2] = center_corner[np.argmax(s)]   # giá trị tọa độ dưới-phải
    
    # Sử dụng hàm tìm sự chênh lệch giữa x và y của từng cặp tọa độ
    # cặp điểm nào có sự chênh lệch bé nhất là tọa độ góc trên-phải 
    # cặp điểm nào có sự chênh lệch lớn nhất là tọa độ góc dưới-trái
    diff = np.diff(center_corner, axis=1)    # hàm tính chênh lệch theo hàng 
    rect[1] = center_corner[np.argmin(diff)] # giá trị tọa độ trên-phải
    rect[3] = center_corner[np.argmax(diff)] # giá trị tọa độ dưới-trái
    
    return rect


# Hàm sử dụng biến đổi bằng phép chiếu phối cảnh để đưa ảnh mới được
# xác định nếu đang bị méo do góc camera nghiên chuyển thành góc camera
# nhìn từ trên xuống.
def four_point_transform(video_frame, center_corner):
    # Xác định lại 4 điểm góc theo thứ tự 
    rect = identiify_corner(center_corner)
    (topLeft, topRight, bottomRight, bottomLeft) = rect
    
    # Xác định chiều rộng của ảnh mới được tính theo khoảng cách lớn nhất
    # giữa 2 điểm trên-trái và trên-phải hoặc giữa 2 điểm dưới-trái và dưới-phải
    width_top = np.sqrt(((topRight[0] - topLeft[0]) ** 2) + ((topRight[1] - topLeft[1]) ** 2))
    width_bottom = np.sqrt(((bottomRight[0] - bottomLeft[0]) ** 2) + ((bottomRight[1] - bottomLeft[1]) ** 2))
    width_max = max(int(width_top), int(width_bottom))
    
    # Xác định chiều dài của ảnh mới được tính theo khoảng cách lớn nhất
    # giữa 2 điểm trên-trái và dưới-trái hoặc giữa 2 điểm trên-phải và dưới-phải
    height_right = np.sqrt(((topRight[0] - bottomRight[0]) ** 2) + ((topRight[1] - bottomRight[1]) ** 2))
    height_left = np.sqrt(((topLeft[0] - bottomLeft[0]) ** 2) + ((topLeft[1] - bottomLeft[1]) ** 2))
    height_max = max(int(height_left), int(height_right))
    
    # Tạo ra một mảng chứa các tọa độ mới được xác định với góc camera từ trên xuống 
    dst = np.array([[0,             0],
                    [width_max - 1, 0],
                    [width_max - 1, height_max - 1],
                    [0            , height_max - 1]], dtype= "float32")
    
    # tính toán ma trận chiếu phối cảnh
    Matrix_perspective = cv2.getPerspectiveTransform(rect, dst)
    Img_warpPerspective = cv2.warpPerspective(video_frame, Matrix_perspective, (width_max, height_max))
    
    return Img_warpPerspective 
    