import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Exercises(_database.Base):
    __tablename__ = 'exercises'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = _sql.Column(_sql.String, nullable=False)
    done = _sql.Column(_sql.Boolean, nullable=False)
    position = _sql.Column(_sql.Integer, nullable=False, default=0)
    course_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('courses.id'))
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))

    courses = relationship('Courses', back_populates='exercises')
    pictures = relationship('Pictures', back_populates='exercises')
    views = relationship('Views', back_populates='exercises')
    exercise_feedback = relationship('Exercise_feedback', back_populates='exercises')

    def __repr__(self):
        return f"<Exercises(id={self.id}, title='{self.title}', done='{self.done}', position='{self.position}', course_id={self.course_id}, picture_id={self.picture_id})>"
