import smtplib
from email.mime.text import MIMEText
import os
import pandas as pd
import config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_messages(row):
    name = row['name']
    webinar_name = row['webinar_name'] if 'webinar_name' in row and pd.notna(row['webinar_name']) else "our recent webinar"

    course_data = []
    for i in range(1, 4):  # For top 3 courses
        course_name_col = f'course_{i}_name'
        course_link_col = f'course_{i}_link'
        if course_name_col in row and pd.notna(row[course_name_col]):
            course_data.append({
                'name': row[course_name_col],
                'link': row[course_link_col] if pd.notna(row[course_link_col]) else 'https://my-communication.com'
            })
        else:
            break

    email_course_list = "\n".join([f"- {course['name']}: {course['link']}" for course in course_data])
    whatsapp_course_list = "\n".join([f"✅ {course['name']} 👉 {course['link']}" for course in course_data])

    # Email Message
    email_message = f"""Subject: 👋 {name}, here are some personalized course recommendations!

Hi {name},

Since you attended our webinar of *{webinar_name}* and your background matches our programs, we think you’ll love these courses:
{email_course_list}

Explore these and more at https://my-communication.com

Best,
My Communication Academy Team
"""

    # WhatsApp Message (not sent yet; can add Twilio integration if needed)
    whatsapp_message = f"""Hi {name} 👋
Based on your background and your interest shown in *{webinar_name}*, we think these courses are perfect for you:
{whatsapp_course_list}

Check them out 👉 https://my-communication.com

Good luck 🚀"""

    return pd.Series({'email_message': email_message, 'whatsapp_message': whatsapp_message})

def send_email(to_email, body):
    msg = MIMEText(body, 'plain')
    msg["Subject"] = config.EMAIL_SUBJECT
    msg["From"] = config.EMAIL_SENDER
    msg["To"] = to_email

    try:
        email_pass = os.environ.get("EMAIL_PASS")
        if not email_pass:
            raise ValueError("EMAIL_PASS environment variable is not set")

        # Use SSL (port 465) or TLS (port 587)
        if config.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT)
        else:
            server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
            server.starttls()  # Enable TLS

        server.login(config.SMTP_USERNAME, email_pass)
        server.sendmail(config.EMAIL_SENDER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except smtplib.SMTPAuthenticationError:
        print(f"Authentication failed for {config.SMTP_USERNAME}. Check credentials.")
    except smtplib.SMTPException as e:
        print(f"SMTP error sending to {to_email}: {e}")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error sending to {to_email}: {e}")