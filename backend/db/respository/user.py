from .base import BaseRepository
from db.schema import User
from models.user import UserCreateRequest
from uuid import UUID


class UserRepository(BaseRepository):
    def create_user(self, user_data: UserCreateRequest):
        new_user = User(**user_data.model_dump(exclude_none=True))

        if self.user_exist_by_email(user_data.email):
            raise Exception("User already exists. Skipping...")

        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)

        return new_user
    
    def user_exist_by_email(self, email: str) -> bool:
        user = self._session.query(User).filter_by(email=email).first()
        return bool(user)
    
    def get_user_by_email(self, email: str) -> User | None:
        user = self._session.query(User).filter_by(email=email).first()
        return user
    
    def get_user_by_id(self, id: UUID) -> User | None:
        user = self._session.query(User).filter_by(id=id).first()
        return user
    
    def get_user(self) -> User | None:
        user = self._session.query(User).first()
        return user