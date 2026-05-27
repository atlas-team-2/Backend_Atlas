from pathlib import Path
from secrets import token_hex

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.settings import settings
from app.dependencies.repositories import EmailNotificationRepositoryDep
from app.models.entities.email import EmailAction, EmailNotification, EmailNotificationCreate

_TEMPLATES_DIR = Path(__file__).parent.parent.parent / 'templates'


def _get_config() -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.email.username,
        MAIL_PASSWORD=settings.email.password,
        MAIL_FROM=settings.email.from_email,
        MAIL_PORT=settings.email.port,
        MAIL_SERVER=settings.email.host,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        TEMPLATE_FOLDER=_TEMPLATES_DIR,
    )


async def send_email(
    email: str,
    subject: str,
    template_name: str,
    body: dict,
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        template_body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(_get_config())
    await fm.send_message(message, template_name=template_name)


class EmailService:
    def __init__(
        self,
        email_notification_repository: EmailNotificationRepositoryDep,
        background_tasks: BackgroundTasks,
    ):
        self.__repo = email_notification_repository
        self.__background_tasks = background_tasks

    async def send_verification_email(self, user_id, email: str) -> EmailNotification:
        code = token_hex(16)
        notification = await self.__repo.save(
            EmailNotification(
                **EmailNotificationCreate(
                    user_id=user_id,
                    code=code,
                    action=EmailAction.VERIFY_ACCOUNT,
                ).model_dump()
            )
        )
        self.__background_tasks.add_task(
            send_email,
            email=email,
            subject='Подтверждение email — Atlas Naroda',
            template_name='verify.html',
            body={'code': code, 'url': f''},
        )
        return notification

    async def send_password_reset_email(self, user_id, email: str) -> EmailNotification:
        code = token_hex(16)
        notification = await self.__repo.save(
            EmailNotification(
                **EmailNotificationCreate(
                    user_id=user_id,
                    code=code,
                    action=EmailAction.CHANGE_PASSWORD,
                ).model_dump()
            )
        )
        self.__background_tasks.add_task(
            send_email,
            email=email,
            subject='Сброс пароля — Atlas Naroda',
            template_name='password_reset.html',
            body={'code': code},
        )
        return notification

    async def verify_code(self, user_id, action: EmailAction, code: str) -> bool:
        notification = await self.__repo.get_active_code(user_id, action)
        if notification is None or notification.code != code:
            return False
        notification.is_used = True
        await self.__repo.save(notification)
        return True