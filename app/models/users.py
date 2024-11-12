import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Users(_database.Base):
    __tablename__ = 'users'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = _sql.Column(_sql.String, nullable=False)
    mail = _sql.Column(_sql.String, nullable=False)
    group = _sql.Column(_sql.String, nullable=True)
    name = _sql.Column(_sql.String, nullable=False)
    password = _sql.Column(_sql.String, nullable=False)
    avatar = _sql.Column(_sql.LargeBinary, nullable=True)

    posts = relationship('Posts', back_populates='user')
    progress = relationship('Progress', back_populates='user')

    def __repr__(self):
        return f"<Users(id={self.id}, login='{self.login}', mail='{self.mail}', group='{self.group}', name='{self.name}', password='{self.password}')>"
