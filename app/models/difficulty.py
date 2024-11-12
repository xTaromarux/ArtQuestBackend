import sqlalchemy as _sql
import database as _database

class Difficulty(_database.Base):
    __tablename__ = 'difficulty'
    id = _sql.Column(_sql.UUID, primary_key=True)
    name = _sql.Column(_sql.String, index=True)
    color = _sql.Column(_sql.String, index=True)
    score = _sql.Column(_sql.Integer, index=True)
    

    def __repr__(self):
        return (f"<Difficulty(id={self.id}, name='{self.name}', "
                f"color='{self. color}', score='{self.score}')>")
