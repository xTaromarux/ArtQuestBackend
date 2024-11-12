import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Exercises(_database.Base):
    __tablename__ = 'exercises'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=False)
    aipart = _sql.Column(_sql.String, nullable=True)
    colSpan = _sql.Column(_sql.Integer, nullable=True)
    rowSpan = _sql.Column(_sql.Integer, nullable=True)
    cols = _sql.Column(_sql.Integer, nullable=True)
    rows = _sql.Column(_sql.Integer, nullable=True)
    difficulty_id = _sql.Column(_sql.UUID(as_uuid=True), _sql.ForeignKey('difficulty.id'))

    difficulty = relationship('Difficulty', back_populates='exercises')
    pictures = relationship('Pictures', back_populates='exercise')
    progress = relationship('Progress', back_populates='exercise')

    def __repr__(self):
        return f"<Exercises(id={self.id}, title='{self.title}', description='{self.description}', difficulty_id='{self.difficulty_id}')>"
