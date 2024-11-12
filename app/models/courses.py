import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Courses(_database.Base):
    __tablename__ = 'courses'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = _sql.Column(_sql.String, nullable=False)
    short_description = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=False)
    experience = _sql.Column(_sql.Integer, nullable=False)
    points = _sql.Column(_sql.Integer, nullable=False)
    difficulty_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('difficulties.id'))
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))

    difficulties = relationship('Difficulties', back_populates='courses')
    pictures = relationship('Pictures', back_populates='courses')
    progresses = relationship('Progresses', back_populates='courses')
    exercises = relationship('Exercises', back_populates='courses')
    user_course = relationship('User_course', back_populates='courses')
    views = relationship('Views', back_populates='courses')

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', short_description='{self.short_description}', description='{self.description}', experience='{self.experience}', points='{self.points}', difficulty_id='{self.difficulty_id}', picture_id='{self.picture_id}')>"
