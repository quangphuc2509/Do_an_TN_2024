import cv2
import numpy as np
import copy

# Load the image
image = cv2.imread(r'F:\DATN_HK2_2024\camera_img\line15.jpg')
scale = 0.7
image_resize = cv2.resize(image, (0,0), fx=scale, fy = scale)
cv2.imshow("Raw Image", image_resize)
# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform edge detection
edges = cv2.Canny(blurred, 80, 210, apertureSize=3)
edges_resize = cv2.resize(edges, (0,0), fx=scale, fy = scale)
# Display the curves
cv2.imshow('edges', edges_resize)

# Define a function to save points of a curve
def save_curve(x0, y0, x1, y1, curves):
    curves.append(((x0 + x1) // 2, (y0 + y1) // 2))
    
def center_point(x_list, y_list):
    count = 0
    average_array = []
    x_average_list = []
    x_array_not_none = []
    for x_point, y_point in zip(x_list, y_list):
        x_array = np.array(x_point)
        y_array = np.array(y_point)
        
        if not np.all(x_array == 0) or not np.all(y_array == 0):
            # print(f"x_array: {x_array}\ny_array: {y_array}")
            x_array_not_none.append(x_array)
            
            x_average = int(np.nanmean(x_array[:]))
            y_average = int(np.nanmean(y_array[:]))
            
            average_array.append((x_average, y_average))
            x_average_list.append(x_average)
            # print(f"x_average: {x_average}\n")
            
    return average_array, x_average_list, x_array_not_none

def check_average(average_array, curve, x_array):
    average_array_copy = copy.deepcopy(average_array)
    x_array_copy = copy.deepcopy(list(x_array))
    count = 1
    y_value = 1
    result_average = [(average_array_copy[0], 0)]
    
    for i in range(1,len(average_array_copy)):
        
        diff = np.abs(average_array_copy[i-1] - average_array[i])

        if diff > 5:
            result = np.abs(average_array_copy[i-1] - x_array_copy[i])

            bool_condition = result < 7
            
            value_condition = x_array_copy[i][bool_condition]
            
            if not np.all(value_condition == 0):
                average_array_copy[i] = int(np.ceil(np.nanmean(value_condition[:])))
            else:
                average_array_copy[i] = average_array_copy[i-1]
            
            # print(f"value_condition {i}: {value_condition}")
            # print(f"average_array_copy {i}: {average_array_copy[i]}")
        # if 
        result_average.append((average_array_copy[i],y_value))
        y_value = y_value + 1
        # print(f"diff {count}: {diff}")
        # count = count +1
    print(f"result_average:{result_average}\n len of {len(result_average)}")
    
    return result_average
    
def event_mouse(event, x, y, flag, para):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"toa do (x,y): {x},{y}")

def max_difference(arr):
    if len(arr) < 2:
        raise ValueError("Array must have at least two elements")

    # Chuyển đổi danh sách sang mảng NumPy
    np_arr = np.array(arr)
    
    # Tính toán sự chênh lệch giữa các phần tử cạnh nhau
    diff = np.diff(np_arr)
    
    # Trả về giá trị lớn nhất của sự chênh lệch
    return np.max(diff), diff

# Initialize variables for curve points
curves = []
x_list = []
y_list = []
x0, y0, x1, y1 = 0, 0, 0, 0
found_curve = False
print(f"edge \n {edges.shape}")

height = edges.shape[0]
width = edges.shape[1]
# Iterate through each pixel in the edge-detected image
for y in range(height):
    x = 0
    x_point = []
    y_point = []
    edge_found = False
    while x < width:
        if edges[y, x] != 0:
            # Found an edge pixel
            # if not found_curve:
                # Start of a new curve
            x_point.append(x)
            y_point.append(y)
            edge_found = True         
            # Skip pixels of the same edge
            while x < width  and edges[y, x] != 0:
                x += 1
            x_point.append(x)
            y_point.append(y)
        # elif found_curve:
        #     # End of the current curve
        #     # save_curve(x0, y0, x1, y1, curves)
        #     # print(f"x0: {x0} / y0: {y0} / x1: {x1} / y1: {y1}")
        #     found_curve = False
            
        if not edge_found:
            x += 1
        edge_found = False
    
    x_list.append(x_point)
    y_list.append(y_point)



# x_array = np.array(x_list)
# print(f"x_list[0]:\n{x_list}")
# print(f"length of x_list: {x_array.shape}\n")
# print(f"y_list[0]:\n{y_list[0]}")
# print(f"length of y_list: {len(y_list)}\n")

curves_1, x_average_list, x_array = center_point(x_list=x_list, y_list= y_list)
# max_diff, diff = max_difference(x_average_list)
curves_2 = check_average(x_average_list, curves_1, x_array)
# print(f"x_array: \n{len(x_array)}")
# print(f"diff: \n{diff}")
# print(f"Sự chênh lệch lớn nhất giữa các phần tử cạnh nhau là: {max_diff}", )
# print(f"curvers_1: {curves_1}")
# Simplify the collected points
simplified_curves = []
if curves_2:
    simplified_curves.append(curves_2[0])  # Add the first point
    for i in range(1, len(curves_2)):
        if curves_2[i][1] != simplified_curves[-1][1]:  # Check if y-coordinate changes
            simplified_curves.append(curves_2[i])

print(f"simplified_curves: \n{simplified_curves}")
# Draw the curves on a blank image
curve_image = np.zeros_like(edges)
count = 0
# print(f"simple:\n{simplified_curves}")
for curve in simplified_curves:
    # if (curve != curve):
    # print(f"curve {count}: {curve[0]}")
    cv2.circle(curve_image, curve, 1, 255, -1)  # Draw a circle at the midpoint
    count = count +1

# # Display the curves
# cv2.imshow('edges', image)
# Display the curves
curve_image_resize = cv2.resize(curve_image, (0,0), fx=scale, fy = scale)
cv2.imshow('Curves', curve_image_resize)
cv2.setMouseCallback('Curves',event_mouse)
cv2.waitKey(0)
cv2.destroyAllWindows()
