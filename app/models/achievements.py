import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Achievements(_database.Base):
    __tablename__ = 'achievements'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experience = _sql.Column(_sql.Integer, nullable=False)
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))

    pictures = relationship('Pictures', back_populates='achievements')
    user_achievements = relationship('User_achievements', back_populates='achievements')

    def __repr__(self):
        return f"<Achievements(id={self.id}, experience='{self.experience}', picture_id='{self.picture_id}')>"
