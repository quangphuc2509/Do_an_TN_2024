import cv2
import numpy as np

# Load the image
image = cv2.imread(r'F:\DATN_HK2_2024\camera_img\line2.jpg')

cv2.imshow("Raw Image", image)
# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform edge detection
edges = cv2.Canny(blurred, 0, 210, apertureSize=3)
edges_resize = cv2.resize(edges, (0,0), fx=0.1, fy = 0.1)
# Display the curves
cv2.imshow('edges', edges_resize)

# Define a function to save points of a curve
def save_curve(x0, y0, x1, y1, curves):
    curves.append(((x0 + x1) // 2, (y0 + y1) // 2))
    
def center_point(x_list, y_list):
    count = 0
    mang = []
    for x_point, y_point in zip(x_list, y_list):
        x_average = int(np.mean(x_point[:4]))
        y_average = int(np.mean(y_point[:4]))
        mang.append((x_average, y_average))
    return mang
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

print(f"x_list[0]:\n{x_list[0]}")
print(f"length of x_list: {len(x_list)}\n")
print(f"y_list[0]:\n{y_list[0]}")
print(f"length of y_list: {len(y_list)}\n")

curves_1 = center_point(x_list=x_list, y_list= y_list)
# Simplify the collected points
simplified_curves = []
if curves_1:
    simplified_curves.append(curves_1[0])  # Add the first point
    for i in range(1, len(curves_1)):
        if curves_1[i][1] != simplified_curves[-1][1]:  # Check if y-coordinate changes
            simplified_curves.append(curves_1[i])

# Draw the curves on a blank image
curve_image = np.zeros_like(edges)
for curve in simplified_curves:
    x, y = curve
    cv2.circle(curve_image, (x, y), 1, 255, -1)  # Draw a circle at the midpoint

# # Display the curves
# cv2.imshow('edges', image)
# Display the curves
curve_image_resize = cv2.resize(curve_image, (0,0), fx=1, fy = 1)
cv2.imshow('Curves', curve_image_resize)
cv2.waitKey(0)
cv2.destroyAllWindows()
