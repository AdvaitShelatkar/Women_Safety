# 🚨 Emergency SOS Alert System

The **Emergency SOS Alert System** is a Python-based solution that enables users to send out immediate emergency notifications. It captures the user's location, records audio and video, and sends this information to predefined contacts via email and SMS.

## Features

- **Location Detection**: Automatically fetches the user's location using their IP address and reverse-geocodes it to a readable address via HERE Maps API.
- **Email Alerts**: Sends email alerts with the current location, along with attached audio and video recordings.
- **SMS Alerts**: Sends SMS messages containing the location information via the Twilio or Vonage APIs.
- **Audio & Video Recording**: Records a 10-second audio message and video clip for additional context.

## Prerequisites

Before you can run the project, you need the following:
- Python 3.x
- Required API keys:
  - [Twilio API](https://www.twilio.com/console) for SMS alerts.
  - [Vonage API](https://developer.vonage.com) as an alternative for SMS alerts.
  - [HERE Maps API](https://developer.here.com/) for reverse geocoding.
- Gmail credentials or SMTP credentials for sending email alerts.

### Required Libraries

Install the required libraries using `pip`:

```bash
pip install requests sounddevice soundfile opencv-python twilio
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/emergency-sos-system.git
   ```

2. Add your credentials:
   - **Twilio/Vonage**: Replace the placeholders in the `send_sms_alert` function.
   - **HERE Maps**: Add your API key to the `emergency_sos()` function.
   - **Email Credentials**: Replace the `sender_email` and `sender_password` with your credentials.

3. Set the recipient details for both email and SMS in the respective functions.

## Usage

1. Run the script:

   ```bash
   python sos_alert.py
   ```

2. The system will:
   - Fetch the user’s location.
   - Record a 10-second audio message.
   - Record a 10-second video clip.
   - Send an email and SMS with the location, audio, and video attached.

## Future Enhancements

- Multi-threading for simultaneous recording of audio and video.
- GPS-based location tracking.
- Real-time push notifications.
