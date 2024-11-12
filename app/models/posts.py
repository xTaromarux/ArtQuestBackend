import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Posts(_database.Base):
    __tablename__ = 'posts'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=False)
    picture = _sql.Column(_sql.LargeBinary, nullable=True)
    date_added = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp())
    date_updated = _sql.Column(_sql.DateTime, nullable=False, default=_sql.func.current_timestamp(), onupdate=_sql.func.current_timestamp())
    user_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('users.id'))

    user = relationship('Users', back_populates='posts')

    def __repr__(self):
        return f"<Posts(id={self.id}, title='{self.title}', description='{self.description}', picture='{self.picture}', date_added='{self.date_added}', date_updated='{self.date_updated}', user_id='{self.user_id}')>"
