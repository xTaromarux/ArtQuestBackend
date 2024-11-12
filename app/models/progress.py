import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Progress(_database.Base):
    __tablename__ = 'progress'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = _sql.Column(_sql.Integer, nullable=False)
    description = _sql.Column(_sql.String, nullable=True)
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))
    exercise_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('exercises.id'))

    user = relationship('Users', back_populates='progress')
    exercise = relationship('Exercises', back_populates='progress')

    def __repr__(self):
        return f"<Progress(id={self.id}, score={self.score}, description='{self.description}', user_id='{self.user_id}', exercise_id='{self.exercise_id}')>"
