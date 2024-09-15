import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import sounddevice as sd
import soundfile as sf
import cv2
from datetime import datetime
from twilio.rest import Client
import vonage


def get_ip_location():
    """
    Fetches the current location based on the device's IP address.
    Returns latitude and longitude as floats.
    """
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        loc = data.get('loc', '0,0').split(',')
        latitude = float(loc[0])
        longitude = float(loc[1])
        return latitude, longitude
    except Exception as e:
        print(f"Error fetching IP location: {e}")
        return None, None


def reverse_geocode(api_key, latitude, longitude):
    """
    Converts latitude and longitude into a human-readable address using HERE Maps API.
    """
    try:
        url = f"https://geocode.reverse.hereapi.com/v1/reverse?at={latitude},{longitude}&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data['items']:
            address = data['items'][0]['address']
            return address['label']
        else:
            return "No address found"
    except Exception as e:
        print(f"Error during reverse geocoding: {e}")
        return None


def send_sms_alert(message):
    """
    Sends an SMS alert using Twilio API.
    """
    twilio_sid = ''  # Replace with your Twilio SID
    twilio_auth_token = ''  # Replace with your Twilio Auth Token
    twilio_phone_number = ''  # Replace with your Twilio phone number
    sms_recipients = ['']
    client = Client(twilio_sid, twilio_auth_token)

    for number in sms_recipients:
        try:
            message = client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=number
            )
            print(f"SMS sent to {number}, SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send SMS to {number}: {e}")

    import requests

    def send_sms_via_http(key, secret, to_number, from_name, messages):
        url = "https://rest.nexmo.com/sms/json"
        payload = {
            "api_key": key,
            "api_secret": secret,
            "to": to_number,
            "from": from_name,
            "text": messages
        }

        try:
            response = requests.post(url, data=payload)
            response_data = response.json()
            if response_data["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {response_data['messages'][0]['error-text']}")
        except Exception as e:
            print(f"Failed to send SMS: {e}")

    # Example usage:
    api_key = ""
    api_secret = ""
    send_sms_via_http(api_key, api_secret, "", "", message)


def send_email_alert(sender_email, sender_password, recipients, subject, body, audio_file, video_file):
    """
    Sends an email alert with attachments.
    """
    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach audio file
    with open(audio_file, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="wav")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(audio_file))
        msg.attach(attach)

    # Attach video file
    with open(video_file, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="avi")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(video_file))
        msg.attach(attach)

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_alert(api_key):
    """
    Sends an alert with the user's location to a predefined list of contacts.
    """
    # Fetch current location based on IP
    latitude, longitude = get_ip_location()
    if latitude is None or longitude is None:
        print("Unable to fetch location.")
        return

    location_address = reverse_geocode(api_key, latitude, longitude)

    print(f"Location: {location_address}, Latitude: {latitude}, Longitude: {longitude}")

    # Email and SMS details
    sender_email = ""
    sender_password = ""
    email_recipients = [""]  # Add more recipients as needed

    subject = "Emergency Alert!"
    body = f"Help needed! My current location is {location_address}. Latitude: {latitude}, Longitude: {longitude} and do please checkout ur email!."

    # Record audio
    audio_filename = f"alert_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    duration = 10  # seconds
    print("Recording audio...")
    recording = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
    sd.wait()
    sf.write(audio_filename, recording, 44100)
    print(f"Audio recorded and saved as {audio_filename}")

    # Capture video
    video_filename = f"alert_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
    print("Recording video...")

    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < 10:  # 10 seconds of video
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    # cv2.waitKey(1)
    # cv2.destroyAllWindows()

    print(f"Video recorded and saved as {video_filename}")

    # Send email alert
    send_email_alert(sender_email, sender_password, email_recipients, subject, body, audio_filename, video_filename)

    # Send SMS alert
    send_sms_alert(body)


def emergency_sos(api_key):
    """
    Triggers the emergency SOS process.
    """

    send_alert(api_key)


if __name__ == "__main__":
    here_maps_api_key = ''  # Replace with your HERE Maps API key

    emergency_sos(here_maps_api_key)
