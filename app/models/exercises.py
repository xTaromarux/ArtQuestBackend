import sqlalchemy as _sql
from database import Base
class Exercises(Base):
    __tablename__ = 'exercises'
    id = _sql.Column(_sql.UUID, primary_key=True)
    state = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    title = _sql.Column(_sql.Integer, index=True)
    picture_id = _sql.Column(_sql.UUID, index=True)
    difficulty_id = _sql.Column(_sql.UUID, index=True)

    def __repr__(self):
        return (f"<Exercises(id={self.id}, state='{self.state}', "
                f"description='{self. description}', title='{self.title}', picture_id='{self.picture_id}, difficulty_id='{self.difficulty_id})>")
