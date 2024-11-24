import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class User_course(_database.Base):
    __tablename__ = 'user_course'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('courses.id'))
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))

    courses = relationship('Courses', back_populates='user_course')
    users = relationship('Users', back_populates='user_course')
    progresses = relationship('Progresses', back_populates='user_course')


    def __repr__(self):
        return f"<User_course(id={self.id}, course_id={self.course_id}, user_id={self.user_id})>"
