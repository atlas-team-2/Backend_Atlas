from app.models.entities.nation_info import NationInfo
from app.repositories.base import Repository

class NationInfoRepository(Repository[NationInfo]):
    def __init__(self, session):
        super().__init__(session, NationInfo)
