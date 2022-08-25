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
