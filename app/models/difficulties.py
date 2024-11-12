import sqlalchemy as _sql
import database as _database
import uuid
from sqlalchemy.orm import relationship

class Difficulties(_database.Base):
    __tablename__ = 'difficulties'
    id = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level = _sql.Column(_sql.Integer, nullable=False)
    color = _sql.Column(_sql.String, nullable=False)
    experience = _sql.Column(_sql.Integer, nullable=False)

    courses = relationship('Courses', back_populates='difficulties')

    def __repr__(self):
        return f"<Difficulties(id={self.id}, level='{self.level}', color='{self.color}', experience={self.experience})>"
