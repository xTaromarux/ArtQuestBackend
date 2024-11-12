import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Pictures(_database.Base):
    __tablename__ = 'pictures'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    picture = _sql.Column(_sql.LargeBinary, nullable=True)
    exercise_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('exercises.id'))

    exercise = relationship('Exercises', back_populates='pictures')

    def __repr__(self):
        return f"<Pictures(id={self.id}, picture='{self.picture}', exercise_id='{self.exercise_id}')>"
