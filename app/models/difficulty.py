import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Difficulty(_database.Base):
    __tablename__ = 'difficulty'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = _sql.Column(_sql.String, nullable=False)
    color = _sql.Column(_sql.String, nullable=False)
    score = _sql.Column(_sql.Integer, nullable=False)

    exercises = relationship('Exercises', back_populates='difficulty')

    def __repr__(self):
        return f"<Difficulty(id={self.id}, name='{self.name}', color='{self.color}', score={self.score})>"
