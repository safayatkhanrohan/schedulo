from datetime import datetime
from app.core.email import send_email
from app.utils.template_renderer import render_template


def format_time(time: datetime):
    return time.strftime("%B %d, %Y at %I:%M %p")


def notify_client_on_booking_request(
    client_email: str, client_name: str, freelancer_name: str, booking_time: datetime
):
    subject = "Booking Request Received"
    html_content = render_template(
        "client_booking_request.html",
        client_name=client_name,
        freelancer_name=freelancer_name,
        time=format_time(booking_time),
        current_year=datetime.now().year,
    )
    send_email(to_email=client_email, subject=subject, html_content=html_content)


def notify_freelancer_on_booking_request(
    freelancer_name: str, freelancer_email: str, client_name: str, booking_time: datetime
):
    subject = "New Booking Request"
    html_content = render_template(
        "freelancer_booking_request.html",
        freelancer_name=freelancer_name,
        client_name=client_name,
        booking_time=format_time(booking_time),
        current_year=datetime.now().year,
    )
    send_email(to_email=freelancer_email, subject=subject, html_content=html_content)


def notify_client_on_booking_confirmation(
    client_email: str,
    client_name: str,
    booking_time: datetime,
    freelancer_name: str,
    meeting_link: str,
):
    subject = "Booking Confirmation"
    html_content = render_template(
        "client_booking_confirmation.html",
        client_name=client_name,
        booking_time=format_time(booking_time),
        freelancer_name=freelancer_name,
        meeting_link=meeting_link,
        current_year=datetime.now().year,
    )
    send_email(to_email=client_email, subject=subject, html_content=html_content)


def notify_client_on_booking_cancellation(
    client_email: str, client_name: str, booking_time: datetime, freelancer_name: str
):
    subject = "Booking Cancellation"
    html_content = render_template(
        "client_booking_cancellation.html",
        client_name=client_name,
        booking_time=format_time(booking_time),
        freelancer_name=freelancer_name,
    )
    send_email(to_email=client_email, subject=subject, html_content=html_content)
