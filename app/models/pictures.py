import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Pictures(_database.Base):
    __tablename__ = 'pictures'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    picture = _sql.Column(_sql.LargeBinary, nullable=True)

    courses = relationship('Courses', back_populates='pictures')
    exercises = relationship('Exercises', back_populates='pictures')
    posts = relationship('Posts', back_populates='pictures')
    views_pictures = relationship('Views_pictures', back_populates='pictures')
    achievements = relationship('Achievements', back_populates='pictures')
    users = relationship('Users', back_populates='pictures')
    
    def __repr__(self):
        return f"<Pictures(id={self.id}, picture='{self.picture}')>"
