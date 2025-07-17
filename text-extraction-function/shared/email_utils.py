import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

load_dotenv()

def send_email_alert(subject, blob_name):
    from_email = os.getenv("EMAIL_FROM")
    to_email = os.getenv("EMAIL_TO")
    api_key = os.getenv("SENDGRID_API_KEY")

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="background-color: #ffffff; border-radius: 8px; padding: 20px; max-width: 600px; margin: auto;">
          <h2 style="color: #2E86C1;">📄 Text Extraction Complete</h2>
          <p style="font-size: 16px;">The text has been successfully extracted from:</p>
          <p style="font-size: 18px; font-weight: bold; color: #444;">{blob_name}</p>
          <p style="margin-top: 20px;">✅ A structured JSON file has been generated and uploaded to the output container in Azure Blob Storage.</p>
          <hr style="margin: 30px 0;">
          <p style="font-size: 14px; color: #888;">This is an automated alert from your text-extraction-app.</p>
        </div>
      </body>
    </html>
    """

    message = Mail(
        from_email=Email(from_email),
        to_emails=To(to_email),
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f" HTML Email sent! Status: {response.status_code}")
    except Exception as e:
        print(f" Failed to send email: {e}")
