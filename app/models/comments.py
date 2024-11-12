import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime

class Comments(_database.Base):
    __tablename__ = 'comments'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = _sql.Column(_sql.String, nullable=False)
    reactions = _sql.Column(_sql.Integer, nullable=False)
    date_added = _sql.Column(_sql.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    date_updated = _sql.Column(_sql.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))
    post_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('posts.id'))

    users = relationship('Users', back_populates='comments')
    posts = relationship('Posts', back_populates='comments')


    def __repr__(self):
        return f"<comments(id={self.id}, description='{self.description}', reactions='{self.reactions}', date_added='{self.date_added}', date_updated='{self.date_updated}', user_id='{self.user_id}', post_id='{self.post_id}')>"
