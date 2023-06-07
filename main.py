from qrcodegenerator.simplegenerator import generate_qr_code
# img = generate_qr_code('Hello, World!', file_path='qr_code.png')
# img = generate_qr_code('https://www.example.com', shape='diamond', file_path='qr_code.png')


generate_qr_code('https://nearabl.com', 4, 1, 30, icon_path='icon.png', scale=0.2,  fill_color_1="red", fill_color_2="yellow")