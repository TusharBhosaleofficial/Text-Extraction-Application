from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

AZURE_CONN_STR = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_INPUT_CONTAINER")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        image = request.files.get('image')
        user_email = request.form.get('email')

        if image and user_email:
            try:
                # Upload to Azure Blob
                blob_service = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
                blob_client = blob_service.get_blob_client(CONTAINER_NAME, image.filename)
                blob_client.upload_blob(image, overwrite=True)

                # Send email
                mail = Mail(
                    from_email=EMAIL_FROM,
                    to_emails=user_email,
                    subject='Your image was received!',
                    html_content=f"<strong>Thanks! {image.filename} is being processed.</strong>"
                )
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(mail)

                message = {
                    "type": "success",
                    "text": f"✅ File <strong>{image.filename}</strong> uploaded to Azure Blob and email sent to <strong>{user_email}</strong>!"
                }

            except Exception as e:
                message = {
                    "type": "error",
                    "text": f"❌ Something went wrong: {str(e)}"
                }

    return render_template('upload.html', message=message)


if __name__ == '__main__':
    print("✅ Flask app is starting...")
    app.run(debug=True)
