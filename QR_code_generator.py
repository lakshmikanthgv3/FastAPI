import qrcode

qr_URL = input("Enter the URL: ").strip()
filename = input("Enter the file name: ").strip()
qr = qrcode.QRCode(box_size=18, border=4)
qr.add_data(qr_URL)
image = qr.make_image(fill_color='black', back_color='white')
image.save(filename)
print(f"QR code is saved as {filename}")