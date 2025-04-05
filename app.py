from flask import Flask, request, jsonify
from PIL import Image
import io
import os
import base64
import logging

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Directory to store the pictures
UPLOAD_FOLDER = 'pictures'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-picture', methods=['POST'])
def upload_picture():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            app.logger.error("No image data found in request.")
            return jsonify({"error": "No image data provided"}), 400
        
        image_data = data['image']
        
        # Strip out the metadata (data:image/png;base64, etc.)
        if "base64" not in image_data:
            app.logger.error("Base64 data is missing in the image.")
            return jsonify({"error": "Base64 image data is malformed"}), 400

        image_data = image_data.split(",")[1]  # Remove the data URI part
        
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        
        # Convert bytes to a PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Generate a filename for the image
        file_path = os.path.join(UPLOAD_FOLDER, "picture.png")

        # Save the image to the folder
        image.save(file_path)
        
        app.logger.info(f"Image successfully saved at: {file_path}")
        return jsonify({"message": "Image saved successfully", "file_path": file_path})

    except Exception as e:
        app.logger.error(f"Error during image upload: {e}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
