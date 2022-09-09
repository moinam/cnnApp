import cv2
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, Response, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['GET'])
@app.route("/static/dashboard", methods=['GET'])
@app.route("/static/support", methods=['GET'])
@app.route("/dashboard", methods=['GET'])
@app.route("/support", methods=['GET'])
def main():
    model = {"title": "Handwritten Digit Recognition."}
    return render_template('index.html', model=model)


@app.get("/clients")
def get_client():
    """
        Returns a list of all clients
        GET: /clients
        Returns: (JSON, Array)
        - clientId
        - name
        - location
    """
    return {}


@app.get("/types")
def get_task_types():
    """
        Returns a list of all task types
        GET: /types
        Returns: (JSON, String Array)
    """
    return {}


@app.route("/im_size", methods=["POST"])
def process_image():
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    im_pil = Image.fromarray(img)
    return jsonify({'msg': 'success', 'size': 'size={}x{}'.format(img.shape[1], img.shape[0])})


@app.post("/predict")
def predict():
    """
        Returns the most fitting team for a task
        POST: /predict
        Payload: (JSON)
        - taskType
        - clientId
        - quantity
        - limit (optional) - max teams that will be returned (defaults to 10)

        Returns: (JSON) [Time data is provided in seconds]
        - teamId
        - location
        - prediction (TimeSpentNorm prediction [in seconds])
        - predictedWorkingTime (TimeSpentNorm prediction multiplied by quantity [in seconds])
        - travelDuration (Time it takes to get to the clients location by driving [in seconds])
        - total (predictedWorkingTime + travelDuration [in seconds])
    """
    content = request.json

    # Check if every required parameter is defined
    if not 'clientId' in content:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "clientId is missing."}))

    if not 'taskType' in content:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "taskType is missing."}))

    if not 'quantity' in content:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "quantity is missing."}))

    return {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
