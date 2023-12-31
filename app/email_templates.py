from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
	email = EmailMessage()
	email["Subject"] = "Подтверждение бронирования"
	email["From"] = settings.EMAIL_USER
	email["To"] = email_to
	
	email.set_content(
		f"""
		<h1>Подтвердите бронирование с {booking['date_from']} по {booking['date_to']}
		""",
		subtype="html",
	)
	return email

# python -m smtpd -u -c DebuggingServer -n localhost:1025
