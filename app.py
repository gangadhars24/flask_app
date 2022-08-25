import pickle
from flask import Flask, jsonify, request
from sklearn.metrics import mean_absolute_error, mean_squared_error
from connect_azure import AzureBlob
import os
import pandas as pd
import numpy as np
import logging

os.makedirs("logs", exist_ok=True)
# Create and configure logger
logging.basicConfig(
    filename="logs/logs.log", format="%(asctime)s %(message)s", filemode="w"
)

# Creating an object
logger = logging.getLogger()
logger.propagate = False
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


ab = AzureBlob()
container_client = ab.auth_connection_string()


@app.route("/")
def index():
    return "<h1>Welcome to Flask Application</h1>"


@app.route("/foldername")
def list_container_folders():

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    folder_name = []
    for blob in blob_list:
        folder_name.append(os.path.dirname(blob.name))

    return dict(list(enumerate(folder_name)))


@app.route("/filename")
def list_container_files():
    blob_list = container_client.list_blobs()
    file_name = []
    for blob in blob_list:
        file_name.append(blob.name)

    file_dict = {}
    for item in file_name:
        key = os.path.dirname(item)
        value = os.path.basename(item)
        if key in file_dict.keys():
            file_dict = val_append(file_dict, key, value)
        else:
            file_dict |= {key: value}
    return file_dict


@app.route("/predict", methods=["POST"])
def predict():
    test_data = request.files["test_data"]
    test_data = pd.read_csv(test_data, encoding="latin1")
    test_label = request.files["test_label"]
    test_label = pd.read_csv(test_label, encoding="latin1")
    prediction = model.predict(test_data)

    test_label = test_label.iloc[:, 1]
    lin_mse = mean_squared_error(test_label, prediction)
    lin_rmse = np.sqrt(lin_mse)

    lin_mae = mean_absolute_error(test_label, prediction)
    logger.info("Test data : {}".format(test_data))
    logger.info("Test label : {}".format(test_label))
    logger.info("Predictions : {}".format(prediction))
    return jsonify(
        {"RMSE": lin_rmse, "MAE": lin_mae, "prediction": list(prediction)}
    )


def val_append(dct, key, value):
    if key in dct:
        if not isinstance(dct[key], list):

            # converting key to list type
            dct[key] = [dct[key]]

            # Append the key's value in list
            dct[key].append(value)
    return dct


def download_model():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    artifact_path = os.path.join(current_dir, "artifacts")
    os.makedirs(artifact_path, exist_ok=True)
    download_file_path = os.path.join(
        artifact_path, "linear_regression_model.pkl"
    )
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        if blob.name == "mle_training_models/linear_regression_model.pkl":
            with open(download_file_path, "wb") as download_file:
                download_file.write(
                    container_client.download_blob(blob.name).readall()
                )
    model = pickle.load(
        open(os.path.join(artifact_path, "linear_regression_model.pkl"), "rb")
    )
    return model


if __name__ == "__main__":
    model = download_model()
    app.run(debug=True, host="0.0.0.0", port=5001)
