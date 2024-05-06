#pip install qrcode



import qrcode



data = input()

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=5,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')

img.save(f'files-qr/qr-for-user-{data}.png')