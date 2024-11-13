import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime

class Statistics(_database.Base):
    __tablename__ = 'statistics'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experience = _sql.Column(_sql.Integer, nullable=False)
    level = _sql.Column(_sql.Integer, nullable=False)
    courses = _sql.Column(_sql.Integer, nullable=False)
    start_strike = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp())
    end_strike = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp())
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))

    users = relationship('Users', back_populates='statistics')


    def __repr__(self):
        return f"<Statistics(id={self.id}, experience={self.experience}, level='{self.level}', courses='{self.courses}', start_strike='{self.start_strike}, end_strike='{self.end_strike}', user_id='{self.user_id}'')>"
