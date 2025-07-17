import os
import json
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

load_dotenv()

endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")
key = os.getenv("COMPUTER_VISION_KEY")

client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))


def extract_text_from_image(image_path):
    """
    Extract text using Read API (v3.2)
    """
    with open(image_path, "rb") as image_stream:
        read_response = client.read_in_stream(image_stream, raw=True)

    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Poll for result
    while True:
        result = client.get_read_result(operation_id)
        if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break

    lines = []
    if result.status == OperationStatusCodes.succeeded:
        for page in result.analyze_result.read_results:
            for line in page.lines:
                lines.append(line.text)

    return {
        "text": lines,
        "summary": f"{len(lines)} lines extracted."
    }


def save_text_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f" JSON saved to {output_path}")
