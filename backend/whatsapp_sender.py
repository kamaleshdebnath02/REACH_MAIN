import sys
import pywhatkit as kit
import os

def send_whatsapp_message(phone, message_file_path):
    try:
        print(f"Sending message to {phone}...")

        # Read the message from the file
        with open(message_file_path, 'r') as file:
            message = file.read()

        # Send the message instantly
        kit.sendwhatmsg_instantly(phone, message)
        print(f"Message sent to {phone}")
    except Exception as e:
        print(f"Failed to send message to {phone}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python whatsapp_sender.py <phone> <message_file_path>")
        sys.exit(1)

    phone_number = sys.argv[1]
    message_file_path = sys.argv[2]

    send_whatsapp_message(phone_number, message_file_path)
