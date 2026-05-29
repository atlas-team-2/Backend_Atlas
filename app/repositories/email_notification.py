from typing import Optional
from uuid import UUID

from app.dependencies.session import SessionDep
from app.models.entities.email import EmailAction, EmailNotification
from app.repositories.base import Repository


class EmailNotificationRepository(Repository[EmailNotification]):
    def __init__(self, session: SessionDep):
        super().__init__(session, EmailNotification)

    async def get_active_code(
        self,
        user_id: UUID,
        action: EmailAction,
    ) -> Optional[EmailNotification]:
        return await self.fetch_one(
            filters={'user_id': user_id, 'action': action, 'is_used': False},
        )