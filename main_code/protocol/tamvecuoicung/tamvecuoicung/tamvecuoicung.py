import math
import socket
import threading
import time
import random



def twos_complement(binary_str):
    # Nếu đầu vào không đủ 32 bit, bổ sung số 0 vào trước chuỗi nhị phân
    binary_str = binary_str.zfill(32)

    # Đảo bit của chuỗi nhị phân đã lọc
    reversed_binary_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)

    # Cộng thêm 1
    result = bin(int(reversed_binary_str, 2) + 1)[2:]

    return result

def convert_to_scientific_notation(number):


    if number < 0:
        number = abs(number)
        # Chuyển đổi số thành dạng scientific notation
        scientific_notation = '{:.8e}'.format(number)

        # Tách phần nguyên và phần mũ từ scientific notation
        integer_part, exponent_part = scientific_notation.split('e')

        # Chuyển đổi phần nguyên thành số nguyên
        integer_value = int(integer_part.replace('.', ''))

        # Chuyển đổi phần mũ thành số nguyên
        exponent = (int(exponent_part) - 8)

        # Chuyển đổi x_value và exponent sang binary
        x_binary_repair = bin(integer_value)[2:]  # Bỏ qua tiền tố '0b'

        x_binary =  twos_complement( x_binary_repair)
        
        if len(x_binary) < 32:
            x_binary = '0' * (32 - len(x_binary)) + x_binary

        exponent_binary = bin(exponent)[3:]  # Bỏ qua tiền tố '0b'
        if len(exponent_binary) < 8:
            exponent_binary = '0' * (8 - len(exponent_binary)) + exponent_binary
        # Ghép chuỗi nhị phân của x_value và exponent lại với nhau và thêm 'b' vào đầu
        combined_binary =x_binary + exponent_binary 


    else:
        # Chuyển đổi số thành dạng scientific notation
        scientific_notation = '{:.8e}'.format(number)

        # Tách phần nguyên và phần mũ từ scientific notation
        integer_part, exponent_part = scientific_notation.split('e')

        # Chuyển đổi phần nguyên thành số nguyên
        integer_value = int(integer_part.replace('.', ''))

        # Chuyển đổi phần mũ thành số nguyên
        exponent = (int(exponent_part) - 8)

        # Chuyển đổi x_value và exponent sang binary
        x_binary = bin(integer_value)[2:]  # Bỏ qua tiền tố '0b'
        if len(x_binary) < 32:
            x_binary = '0' * (32 - len(x_binary)) + x_binary
            
        exponent_binary = bin(exponent)[3:]  # Bỏ qua tiền tố '0b'
        if len(exponent_binary) < 8:
            exponent_binary = '0' * (8 - len(exponent_binary)) + exponent_binary

        # Ghép chuỗi nhị phân của x_value và exponent lại với nhau và thêm 'b' vào đầu
        combined_binary = x_binary + exponent_binary 
        
    return combined_binary



# Khởi tạo mảng để lưu trữ 6 số float
six_floats = [1234.5678, 0.01010115, 0.678123, -56789.1233, -0.00000123, -1234.5678]
index = 0

# Hàm cập nhật giá trị original_number
def update_original_number():
    global index
    original_number = six_floats[index]
    index += 1
    if index == len(six_floats):
        index = 0
    return original_number


##########################################################################################
SERVER_ID = socket.gethostbyname(socket.gethostname())
s = socket.socket()         
s.bind((SERVER_ID , 55555))
s.listen(0)                

client_socket, addr = s.accept()
print("Server đã sẵn sàng để nhận kết nối và gửi dữ liệu cho client.")

# Khởi tạo biến count
count = 0

# Vòng lặp vô hạn
while True:
    # Cập nhật giá trị original_number
    original_number = update_original_number()
    
    # Chuyển đổi số ban đầu thành dạng scientific notation
    datasend = convert_to_scientific_notation(original_number)
    
    # Gửi dữ liệu qua kết nối
    client_socket.send(datasend.encode())
    # time.sleep(0.001)
    # Tăng biến count lên
    count += 1
    print("Đã gửi lần thứ", count)
    # Kiểm tra nếu count đạt 61 thì thoát khỏi vòng lặp
    if count == 60:
        break

# Đóng kết nối socket
client_socket.close()
