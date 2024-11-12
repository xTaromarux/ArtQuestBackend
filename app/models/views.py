import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Views(_database.Base):
    __tablename__ = 'views'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template = _sql.Column(_sql.Integer, nullable=False)
    ai_part = _sql.Column(_sql.Boolean, nullable=False)
    next_view_id = _sql.Column(_sql.UUID(as_uuid=True))
    previous_view_id = _sql.Column(_sql.UUID(as_uuid=True))
    exercise_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('exercises.id'))
    course_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('courses.id'))

    exercises = relationship('Exercises', back_populates='views')
    views_data = relationship('Views_data', back_populates='views')
    views_pictures = relationship('Views_pictures', back_populates='views')
    courses = relationship('Courses', back_populates='views')

    def __repr__(self):
        return f"<Views(id={self.id}, template='{self.template}', ai_part='{self.ai_part}', next_view_id='{self.next_view_id}', previous_view_id='{self.previous_view_id}', exercise_id='{self.exercise_id}')>"
