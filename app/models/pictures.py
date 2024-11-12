import sqlalchemy as _sql
import database as _database

class Pictures(_database.Base):
    __tablename__ = 'pictures'
    id = _sql.Column(_sql.UUID, primary_key=True)
    blob = _sql.Column(_sql.BLOB, index=True)
    description = _sql.Column(_sql.String, index=True)
    date_added = _sql.Column(_sql.String, index=True)
    

    def __repr__(self):
        return (f"<Pictures(id={self.id}, blob='{self.blob}', "
                f"description='{self. description}', date_added='{self.date_added}')>")