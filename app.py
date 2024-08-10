from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
  data = request.form.get('data')
  if not data:
    return render_template('index.html', error="Please enter some data to generate QR code.")
  
  # Create QR code instance
  qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_H,
      box_size=10,
      border=4,
  )
  
  # Add data to QR code
  qr.add_data(data)
  qr.make(fit=True)
  
  # Create an image buffer
  img_buffer = BytesIO()
  qr.make_image(fill_color="black", back_color="white").save(img_buffer, format="PNG")
  img_buffer.seek(0)
  
  return send_file(img_buffer, mimetype="image/png", download_name="qr_code.png")

if __name__ == '__main__':
  app.run(debug=True)
