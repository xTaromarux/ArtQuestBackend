import sqlalchemy as _sql
from database import Base

class Progress(Base):
    __tablename__ = 'progress'
    id = _sql.Column(_sql.UUID, primary_key=True)
    implementation_stage = _sql.Column(_sql.Integer, index=True)
    picture_id = _sql.Column(_sql.UUID, index=True)
    exercises_id = _sql.Column(_sql.UUID, index=True)
    user_id = _sql.Column(_sql.UUID, index=True)
    

    def __repr__(self):
        return (f"<Progress(id={self.id}, implementation_stage='{self.implementation_stage}', "
                f"picture_id='{self. picture_id}', exercises_id='{self.exercises_id}', user_id='{self.user_id})>")