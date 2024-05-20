import math
import socket
import threading
import time
import random
import sys
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
        
    return combined_binary,x_binary ,exponent_binary 




# Khởi tạo mảng để lưu trữ 6 số float
six_floats = [1234.5678, 0.01010115, 0.678123, -56789.1233, -0.00000123, -1234.5678]

def convert_and_combine(six_floats):
    combined_data = ""
    for float_value in six_floats:
        converted_data, _, _ = convert_to_scientific_notation(float_value)
        combined_data += converted_data
    return combined_data


# Hàm gửi dữ liệu liên tục đến client
def continuous_send(client_socket,sending_data ):
    index = 0
    while sending_data and index < len(six_floats):
        combined_data = convert_and_combine(six_floats)  # Lấy dữ liệu đã kết hợp từ mảng six_floats
        client_socket.send(combined_data.encode())
        print("Đã gửi dữ liệu cho client:", combined_data)
        time.sleep(1)
        index += 1
        if index ==len(six_floats):
            index = 0

def stop_sending():
    """
    Hàm này sẽ chạy trong một luồng riêng biệt để chờ người dùng nhấn phím 's' để kết thúc chương trình.
    """
    global sending_data
    while True:
        user_input = input()
        if user_input.lower() == 's':
            sending_data = False  # Dừng gửi dữ liệu
            break

# Tạo socket server và chấp nhận kết nối từ client
SERVER_ID = socket.gethostbyname(socket.gethostname())
s = socket.socket()
s.bind((SERVER_ID, 55555))
s.listen(0)
print("Server đã sẵn sàng để nhận kết nối và gửi dữ liệu cho client.")
client, addr = s.accept()

sending_data = True
# Tiếp tục gửi dữ liệu trong luồng chính
continuous_send(client,sending_data)

# Bắt đầu một luồng riêng biệt để chờ người dùng nhấn phím 's' để bắt đầu gửi dữ liệu
stop_thread = threading.Thread(target=stop_sending)
stop_thread.start()
