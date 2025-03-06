# Telephony Testing Platform

A robust telephony testing platform that enables comprehensive call flow management and real-time monitoring through Twilio integration, with a focus on simplified backend architecture and flexible audio routing.

## Features

- Twilio-based IVR system
- Serverless audio file serving
- Lightweight call tracking mechanism
- Modular Python and JavaScript implementation
- Minimal external dependencies
- Real-time dashboard for monitoring active calls

## Setup Instructions

### 1. Configure Twilio Credentials

The application requires Twilio credentials to function properly. There are two ways to set up your credentials:

#### Option 1: Use the Setup Script

Run the setup script to help you set up your Twilio credentials:

```bash
python setup_twilio.py
```

This script will guide you through the process of entering your Twilio credentials and provide instructions on how to add them to Replit Secrets.

#### Option 2: Manually Add to Replit Secrets

Add the following secrets to your Replit environment:

1. `TWILIO_ACCOUNT_SID` - Your Twilio Account SID
2. `TWILIO_AUTH_TOKEN` - Your Twilio Auth Token
3. `TWILIO_PHONE_NUMBER` - Your Twilio Phone Number (optional)
4. `BASE_URL` - The URL where your app is hosted (optional, will be auto-detected)

To add these secrets:
1. Click on the Tools icon in the Replit sidebar (looks like a wrench)
2. Click on 'Secrets'
3. Add each key-value pair

### 2. Run the Application

The application should start automatically when you open the Replit environment. If it doesn't:

1. Click on the "Run" button at the top of the Replit interface

### 3. Set Up Twilio Webhook

To receive calls in your application, you need to configure your Twilio phone number to point to your Replit application:

1. Log in to your [Twilio Console](https://www.twilio.com/console)
2. Navigate to Phone Numbers > Manage > Active Numbers
3. Click on your phone number
4. Under "Voice & Fax", set the webhook for "A Call Comes In" to:
   - Webhook URL: `https://your-replit-app-url/incoming_call`
   - Method: HTTP POST
5. Set the webhook for "Call Status Changes" to:
   - Webhook URL: `https://your-replit-app-url/call_status`
   - Method: HTTP POST

## Using the Application

### Dashboard

Access the dashboard by opening your Replit app URL. The dashboard displays:
- Current number of active calls
- List of active calls with caller information
- Real-time call count chart

### IVR Options

When someone calls your Twilio number, they will hear:
1. A welcome message
2. Option 1: Listen to music
3. Option 2: Hear a beep every 3 seconds

## Troubleshooting

### Missing Environment Variables

If you see warnings about missing environment variables:
1. Make sure you've added your Twilio credentials to Replit Secrets
2. Restart the application after adding secrets

### Audio Files Not Playing

The application serves audio files from the `static/audio` directory. If audio isn't playing:
1. Check that the audio files exist in the `static/audio` directory
2. Ensure your `BASE_URL` is correctly set (or let it auto-detect)
3. The application will fall back to Twilio demo sounds if local files are unavailable

### Call Limit Reached

The application is configured to handle a maximum of 20 simultaneous calls. If this limit is reached, callers will hear a busy message.