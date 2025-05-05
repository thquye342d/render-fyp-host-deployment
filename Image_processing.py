from flask import Flask, request, jsonify
from flask_cors import CORS

import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Apply bilateral filtering to the image.
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def apply_kmeans(image, k=4):
    """
    Apply K-means clustering to the image.
    """
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)
    return segmented_image, centers

def rgb_to_cmyk(r, g, b):
    """
    Convert RGB values to CMYK.
    """
    r_prime, g_prime, b_prime = r / 255, g / 255, b / 255
    k = 1 - max(r_prime, g_prime, b_prime)
    if k == 1:
        return 0, 0, 0, 1
    c = (1 - r_prime - k) / (1 - k)
    m = (1 - g_prime - k) / (1 - k)
    y = (1 - b_prime - k) / (1 - k)
    return c, m, y, k

def process_image(image_path):
    try:
        print(f"Loading image from: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Failed to load image")
            return None

        print("Applying bilateral filter...")
        filtered_image = apply_bilateral_filter(image)

        print("Applying K-means clustering...")
        _, centers = apply_kmeans(filtered_image)

        print("Calculating CMYK values...")
        cmyk_values = []
        for center in centers:
            r, g, b = center
            c, m, y, k = rgb_to_cmyk(r, g, b)
            cmyk_values.append({
                'C': round(c * 100, 2),
                'M': round(m * 100, 2),
                'Y': round(y * 100, 2),
                'K': round(k * 100, 2)
            })

        return {"cmyk_values": cmyk_values}  # Return as a JSON object
    except Exception as e:
        print(f"Error during image processing: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        print("Error: No image provided in request")
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    print(f"Received file: {file.filename}")
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    print("Processing image...")
    cmyk_data = process_image(filepath)
    os.remove(filepath)  # Remove after processing

    if cmyk_data is None:
        print("Error: Image processing failed")
        return jsonify({"error": "Image processing failed"}), 500

    print(f"Returning CMYK data: {cmyk_data}")
    return jsonify(cmyk_data)  # Returning JSON object instead of a list

@app.route('/', methods=['GET'])
def home():
    return "Flask server is up and running!"

if __name__ == '__main__':
    print("Flask app starting...")  # Ensure this appears in logs
    app.run(host="0.0.0.0", port=8000)
