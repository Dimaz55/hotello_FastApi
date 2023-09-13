import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.email_templates import create_booking_confirmation_template
from app.tasks.celery_app import celery


@celery.task
def process_pic(path: str):
    print("===TASK===")
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized = img.resize((1000, 500))
    img_thumbnail = img.resize((200, 100))
    static_path = f"app/static/images/resized/"
    img_resized.save(f"{static_path}1000x500_{img_path.name}")
    img_thumbnail.save(f"{static_path}200x100_{img_path.name}")


@celery.task
def send_booking_confirmation(booking: dict, email_to: EmailStr):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        # server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
        server.send_message(msg_content)
