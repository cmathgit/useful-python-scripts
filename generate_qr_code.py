import qrcode

# Your destination URL
url = "https://github.com/"

# Create QR code
qr = qrcode.QRCode(
    version=1,  # Controls size: 1 is smallest, 40 is largest
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
    box_size=10,  # Size of each "box" in the QR
    border=4,  # Thickness of the border (minimum 4)
)

qr.add_data(url)
qr.make(fit=True)

# Create and save the image
img = qr.make_image(fill_color="black", back_color="white")
img.save("github_qr_code.png")
