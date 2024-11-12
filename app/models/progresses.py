import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Progresses(_database.Base):
    __tablename__ = 'progresses'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stage = _sql.Column(_sql.Integer, nullable=False)
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))
    user_course_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('courses.id'))

    users = relationship('Users', back_populates='progresses')
    courses = relationship('Courses', back_populates='progresses')

    def __repr__(self):
        return f"<Progresses(id={self.id}, stage={self.stage}, user_id='{self.user_id}', course_id='{self.user_course_id}')>"
