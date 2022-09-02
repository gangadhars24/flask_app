from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
import os


class AzureBlob:
    def auth_connection_string(self):
        # [START auth_from_connection_string]
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        # Create the BlobServiceClient object which will be used to
        # create a container client
        BlobServiceClient.from_connection_string(connect_str)

        container_client = ContainerClient.from_connection_string(
            connect_str, container_name="gangadharcontainer"
        )
        return container_client


"""
from urllib.parse import urlparse
from azure.storage.blob import BlobServiceClient
import os
modelpath = os.getenv("MODELPATH")
blobkey = os.getenv("BLOB_KEY")
uri = urlparse(modelpath)
account_url = uri.scheme + "://" + uri.netloc
container_path = uri.path.lstrip("/").split("/")
container = container_path.pop(0)
path = "/".join(container_path)

client = BlobServiceClient(account_url=account_url,credential=blobkey)

blob = client.get_blob_client(container=container, blob=path)
download_stream = blob.download_blob()
model = download_stream.readall()
"""
