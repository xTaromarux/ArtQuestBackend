import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class User_achievements(_database.Base):
    __tablename__ = 'user_achievements'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))
    achievement_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('achievements.id'))

    users = relationship('Users', back_populates='user_achievements')
    achievements = relationship('Achievements', back_populates='user_achievements')  

    def __repr__(self):
        return f"<User_achievements(id={self.id}, user_id='{self.user_id}', achievement_id='{self.achievement_id}')>"
