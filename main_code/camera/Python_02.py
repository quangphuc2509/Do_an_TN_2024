import cv2
import numpy as np

# Load the image
image = cv2.imread(r'F:\DATN_HK2_2024\camera_img\line15.jpg')

##
# Create a window
cv2.namedWindow('Edges')

# Create trackbars for threshold values
cv2.createTrackbar('Lower Threshold', 'Edges', 0, 255, lambda x: None)
cv2.createTrackbar('Upper Threshold', 'Edges', 0, 255, lambda x: None)
cv2.createTrackbar('V', 'Edges', 1, 10, lambda x: None) 

# Initialize trackbar positions
cv2.setTrackbarPos('Lower Threshold', 'Edges', 80)
cv2.setTrackbarPos('Upper Threshold', 'Edges', 200)
cv2.setTrackbarPos('V', 'Edges', 3)


while True:
    # Get current trackbar positions
    lower_threshold = cv2.getTrackbarPos('Lower Threshold', 'Edges')
    upper_threshold = cv2.getTrackbarPos('Upper Threshold', 'Edges')
    V = cv2.getTrackbarPos('V', 'Edges')
    blur_val = V*2 - 1
    print(f"v la: {blur_val}")
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (blur_val, blur_val), 0) 

    # Perform edge detection
    edges = cv2.Canny(blurred, lower_threshold, upper_threshold, apertureSize=3)
    
    edges_resize = cv2.resize(edges, (0,0), fx=0.5, fy = 0.5)
    cv2.imshow('Detected Lines', edges_resize)

    # Check for 'ESC' key press to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break
##


# # Convert the image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Perform edge detection
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# print(edges)

# # Detect lines using Hough Line Transform
# lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# # Draw detected lines on the original image
# if lines is not None:
#     for rho, theta in lines[:, 0]:
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 1000 * (-b))
#         y1 = int(y0 + 1000 * (a))
#         x2 = int(x0 - 1000 * (-b))
#         y2 = int(y0 - 1000 * (a))
#         #cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# # Display the result
# cv2.imshow('Detected Lines', edges)
# cv2.waitKey(0)
cv2.destroyAllWindows()
