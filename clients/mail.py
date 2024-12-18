import json
import uuid
from dataclasses import dataclass

from core.config import settings

import aio_pika


@dataclass
class MailClient:
    settings: settings

    async def send_welcome_email(self, to: str):
        connection = await aio_pika.connect_robust(settings.broker.url)

        email_body = {
            "message": "Welcome to the Pomodoro!",
            "user_email": to,
            "subject": "Welcome to the Mail Service!",
        }
        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=json.dumps(email_body).encode(),
                    correlation_id=str(uuid.uuid4()),
                ),
                routing_key=self.settings.broker.mail_queue,
            )
