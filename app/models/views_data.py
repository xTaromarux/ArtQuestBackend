import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Views_data(_database.Base):
    __tablename__ = 'views_data'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_description = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=True)
    view_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('views.id'))

    views = relationship('Views', back_populates='views_data')

    def __repr__(self):
        return f"<Views(id={self.id}, short_description='{self.description}', description='{self.description}', view_id='{self.view_id}')>"
