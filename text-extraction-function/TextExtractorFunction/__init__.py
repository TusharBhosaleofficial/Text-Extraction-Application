import logging
import os
import azure.functions as func
from shared.blob_utils import upload_json_to_output_container
from shared.vision_utils import extract_text_from_image, save_text_to_json
from shared.email_utils import send_email_alert

DOWNLOAD_DIR = "/tmp" if os.name != "nt" else "downloads"
OUTPUT_DIR = "/tmp" if os.name != "nt" else "outputs"

def main(myblob: func.InputStream):
    logging.info(f" Blob trigger function started for: {myblob.name}")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    blob_name = os.path.basename(myblob.name)
    local_image_path = os.path.join(DOWNLOAD_DIR, blob_name)
    local_json_path = os.path.join(OUTPUT_DIR, blob_name + ".json")

    # Save the blob locally
    with open(local_image_path, "wb") as f:
        f.write(myblob.read())

    # Extract text
    result = extract_text_from_image(local_image_path)

    # Save to JSON
    save_text_to_json(result, local_json_path)

    # Upload JSON to output container
    upload_json_to_output_container(local_json_path, os.path.basename(local_json_path))

    # Send email alert
    send_email_alert(subject=f"Text extracted: {blob_name}", blob_name=blob_name)

    logging.info(f" Processing complete for: {blob_name}")
