import cv2
import numpy as np
import backend.cnn_model as cnn_model
from backend.cnn_model import CNN
from flask import Flask, Response, render_template, request, jsonify
# from flask_cors import CORS
from PIL import Image
import json
app = Flask(__name__)
# CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['GET'])
@app.route("/static/dashboard", methods=['GET'])
@app.route("/static/support", methods=['GET'])
@app.route("/dashboard", methods=['GET'])
@app.route("/support", methods=['GET'])
def main():
    model = {"title": "Handwritten Digit Recognition."}
    return render_template('index.html', model=model)

@app.route("/recognize", methods=["POST"])
def process_image():
    """
        Returns the recognized digit from the cnn model from the image
        POST: /recognize
        Payload: Image

        Returns: (JSON)
        - message
        - image size
        - prediction (recognized digit)
    """
    try:
        nparr = np.fromstring(request.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        im_pil = Image.fromarray(img)
    except:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "Invalid file or Broken Image."}))
    else:
        try:
            pred_y = cnn_model.predict_image(im_pil)
        except:
            return Response(status=400, content_type='application/json', response=json.dumps({"message": "Could not resize image dimesnions to 28x28."}))

    return jsonify({'message': 'success', 'size': 'size={}x{}'.format(img.shape[1], img.shape[0]), 'Prediction': np.ndarray.item(pred_y)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
