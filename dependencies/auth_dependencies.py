from fastapi import Depends

from clients.mail import MailClient
from dependencies.mail_dependencies import get_mail_client
from services.auth_service import AuthService
from utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_auth_service(
    uow: IUnitOfWork = Depends(UnitOfWork),
    mail_client: MailClient = Depends(get_mail_client),
) -> AuthService:
    return AuthService(uow, mail_client=mail_client)
