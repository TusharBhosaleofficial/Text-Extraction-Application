import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Blob Service Client
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Containers
input_container = os.getenv("INPUT_CONTAINER_NAME")
output_container = os.getenv("OUTPUT_CONTAINER_NAME")


def download_blob(blob_name, download_path):
    """
    Downloads an image blob from the input container to the local path.
    """
    blob_client = blob_service_client.get_blob_client(container=input_container, blob=blob_name)

    with open(download_path, "wb") as f:
        data = blob_client.download_blob()
        f.write(data.readall())
    print(f" Downloaded {blob_name} to {download_path}")


def upload_json_to_output_container(json_path, output_blob_name):
    """
    Uploads a JSON file to the output container.
    """
    blob_client = blob_service_client.get_blob_client(container=output_container, blob=output_blob_name)

    with open(json_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
    print(f" Uploaded JSON to output container as {output_blob_name}")
