import time
from uuid import UUID

from worker import celery


@celery.task(name="auth.send_welcome_email", bind=True)
def send_welcome_email_task(self, username: str) -> UUID:
    time.sleep(5)
    print(f"Sending welcome email to {username}")
    return self.request.id
