import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Exercise_feedback(_database.Base):
    __tablename__ = 'exercise_feedback'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message = _sql.Column(_sql.String, nullable=False)
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))
    exercise_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('exercises.id'))

    users = relationship('Users', back_populates='exercise_feedback')
    pictures = relationship('Pictures', back_populates='exercise_feedback')
    exercises = relationship('Exercises', back_populates='exercise_feedback')

    def __repr__(self):
        return f"<Exercise_feedback(id={self.id}, message={self.message}, user_id={self.user_id}, picture_id={self.picture_id}, exercise_id={self.exercise_id}'')>"
