from clients.mail import MailClient
from core.config import settings


async def get_mail_client() -> MailClient:
    return MailClient(settings=settings)
