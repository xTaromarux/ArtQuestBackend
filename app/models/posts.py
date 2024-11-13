import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Posts(_database.Base):
    __tablename__ = 'posts'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = _sql.Column(_sql.String, nullable=True)
    reactions = _sql.Column(_sql.Integer, nullable=False)
    date_added = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp())
    date_updated = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp())
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))

    user = relationship('Users', back_populates='posts')
    pictures = relationship('Pictures', back_populates='posts')
    comments = relationship('Comments', back_populates='posts')


    def __repr__(self):
        return f"<Posts(id={self.id}, description='{self.description}', reactions='{self.reactions}', date_added='{self.date_added}', date_updated='{self.date_updated}', user_id='{self.user_id}', picture_id={self.id}>"
