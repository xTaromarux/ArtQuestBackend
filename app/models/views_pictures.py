import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Views_pictures(_database.Base):
    __tablename__ = 'views_pictures'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    view_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('views.id'))
    picture_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('pictures.id'))

    views = relationship('Views', back_populates='views_pictures')
    pictures = relationship('Pictures', back_populates='views_pictures')

    def __repr__(self):
        return f"<Views_pictures(id={self.id}, view_id={self.view_id}, picture_id={self.picture_id}'')>"
