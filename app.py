from flask import Flask, render_template
from flask_mail import Mail, Message
from celery import Celery
from celery.utils.log import get_task_logger

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='tu_correo@gmail.com',
    MAIL_PASSWORD='tu_contraseña',
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

mail = Mail(app)
celery = make_celery(app)
logger = get_task_logger(__name__)

@celery.task
def send_async_email(subject, sender, recipients, text_body, html_body):
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)
        logger.info("Email sent successfully.")

@app.route('/send_email')
def send_email():
    subject = "Test Email"
    sender = "tu_correo@gmail.com"
    recipients = ["destinatario@example.com"]
    text_body = "This is a test email sent asynchronously."
    html_body = "<p>This is a <b>test email</b> sent asynchronously.</p>"
    
    send_async_email.delay(subject, sender, recipients, text_body, html_body)
    return "Email sent!"

if __name__ == "__main__":
    app.run(debug=True)
