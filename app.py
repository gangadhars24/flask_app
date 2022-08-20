from flask import Flask
from connect_azure import AzureBlob
import os

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


def val_append(dct, key, value):
    if key in dct:
        if not isinstance(dct[key], list):

            # converting key to list type
            dct[key] = [dct[key]]

            # Append the key's value in list
            dct[key].append(value)
    return dct


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
