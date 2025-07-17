import os
import logging
import azure.functions as func
from pathlib import Path

from shared.blob_utils import upload_json_to_output_container
from shared.vision_utils import extract_text_from_image, save_text_to_json
from shared.email_utils import send_email_alert

app = func.FunctionApp()

@app.function_name(name="TextExtractorFunction")
@app.blob_trigger(arg_name="myblob",
    path="input-container/{name}",
    connection="AzureWebJobsStorage")
def extract_text_from_blob(myblob: func.InputStream):
    logging.info(f" New blob detected: {myblob.name}")

    blob_name = os.path.basename(myblob.name)
    download_dir = Path("/tmp" if os.name != "nt" else "downloads")
    output_dir = Path("/tmp" if os.name != "nt" else "outputs")

    download_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    local_image_path = download_dir / blob_name
    local_json_path = output_dir / f"{blob_name}.json"

    # Save the image locally
    with open(local_image_path, "wb") as f:
        f.write(myblob.read())

    # Extract text
    result = extract_text_from_image(local_image_path)

    # Save as JSON
    save_text_to_json(result, local_json_path)

    # Upload to output container
    upload_json_to_output_container(local_json_path, local_json_path.name)

    # Send email
    send_email_alert(
        subject=f"Text extracted from {blob_name}",
        blob_name=blob_name
    )

    logging.info(f" Processing complete for: {blob_name}")
