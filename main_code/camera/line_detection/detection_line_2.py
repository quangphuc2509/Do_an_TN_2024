import cv2
import numpy as np
import copy

class Detection_line():
    def __init__(self, image):
        self.image = image
        self.scale = 0.5
        
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)    
        self.blured_image = cv2.GaussianBlur(self.gray_image, (5, 5), 0)
        self.edges_image = cv2.Canny(self.blured_image, 80, 210, apertureSize=3)

        self.x_edges_list, self.y_edges_list = self.make_edges_list()
        # print(f"self.x_edges_list:\n{self.x_edges_list}")
        self.average_points, self.x_average_list, self.x_edges_exist = self.find_average_point(self.x_edges_list, self.y_edges_list)
        self.average_points_filted = self.centerline_filter(self.x_average_list, self.x_edges_exist)
        # print(f"self.average_points_filted\n{self.average_points_filted}")
        self.create_curves_image(self.average_points_filted)
        
        self.image_resize = cv2.resize(self.image, (0,0), fx=self.scale, fy = self.scale)
        self.edges_image_resize = cv2.resize(self.edges_image, (0,0), fx=self.scale, fy = self.scale)
        self.curves_image_resize = cv2.resize(self.curves_image, (0,0), fx=self.scale, fy = self.scale)
        
        
    
    def make_edges_list(self):
        height = self.edges_image.shape[0]
        width = self.edges_image.shape[1]
        x_list = []
        y_list = []
   
        for y in range(height):
            x = 0
            x_point = []
            y_point = []
            
            edge_found = False
            
            while x < width:
                if self.edges_image[y, x] != 0:
                    x_point.append(x)
                    y_point.append(y)
                    edge_found = True
                    
                    while x < width and self.edges_image[y,x] != 0:
                        x = x+1
                    
                    x_point.append(x)
                    y_point.append(y)
                
                else:
                    x = x + 1

            x_list.append(x_point)
            y_list.append(y_point)
        
        return x_list, y_list       

    def find_average_point(self, x_list, y_list):
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

    def centerline_filter(self, average_array, x_array):
        average_array_copy = copy.deepcopy(average_array)
        x_array_copy = copy.deepcopy(list(x_array))
        y_value = 1
        result_average = [(average_array_copy[0], 0)]
        
        for i in range(1, len(average_array_copy)):
            diff = np.abs(average_array_copy[i-1] - average_array[i])

            if diff > 5:
                result = np.abs(average_array_copy[i-1] - x_array_copy[i])

                bool_condition = result < 7
                
                value_condition = x_array_copy[i][bool_condition]
                
                if not np.all(value_condition == 0):
                    average_array_copy[i] = int(np.ceil(np.nanmean(value_condition[:])))
                else:
                    average_array_copy[i] = average_array_copy[i-1]
                
            result_average.append((average_array_copy[i],y_value))
            y_value = y_value + 1

        # print(f"result_average:{result_average}\n len of {len(result_average)}")
        
        return result_average
    
    def create_curves_image(self, average_points_filted):
        self.curves_image = np.zeros_like(self.edges_image)
        for curve in average_points_filted:
            cv2.circle(self.curves_image, curve, 1, 255, -1)

# if __name__ == "__main__":
#     url = r"F:\DATN_HK2_2024\camera_img\line9.jpg"
#     image = cv2.imread(url)
#     average = Detection_line(image)
    
#     cv2.imshow("Raw Image", average.image_resize)
#     cv2.imshow('edges', average.edges_image_resize)
#     cv2.imshow('Curves', average.curves_image_resize)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()