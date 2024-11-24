import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime

class Users(_database.Base):
    __tablename__ = 'users'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = _sql.Column(_sql.String, nullable=False)
    mail = _sql.Column(_sql.String, nullable=False)
    group = _sql.Column(_sql.String, nullable=True)
    user_name = _sql.Column(_sql.String, nullable=False)
    created_date = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp())
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))


    pictures = relationship('Pictures', back_populates='users')
    posts = relationship('Posts', back_populates='user')
    comments = relationship('Comments', back_populates='users')
    statistics = relationship('Statistics', back_populates='users')
    user_course = relationship('User_course', back_populates='users')
    user_achievements = relationship('User_achievements', back_populates='users')
    exercise_feedback = relationship('Exercise_feedback', back_populates='users')


    def __repr__(self):
        return f"<Users(id={self.id}, login='{self.login}', mail='{self.mail}', group='{self.group}', user_name='{self.user_name}', created_date='{self.created_date}', picture_id='{self.picture_id}')>"
