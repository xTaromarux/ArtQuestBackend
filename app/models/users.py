import sqlalchemy as _sql
from database import Base

class Users(Base):
    __tablename__ = 'users'
    id = _sql.Column(_sql.UUID, primary_key=True)
    group = _sql.Column(_sql.String, index=True)
    mail = _sql.Column(_sql.String, index=True)
    login = _sql.Column(_sql.String, index=True)
    password = _sql.Column(_sql.String, index=True)
    date_added = _sql.Column(_sql.Date, index=True)
    date_updated = _sql.Column(_sql.Date, index=True)
    

    def __repr__(self):
        return (f"<Users(id={self.id}, group='{self.group}', mail='{self.mail}',"
                f" login='{self.login}', password='{self.password}, date_added='{self.date_added},  "
                f"date_updated='{self.date_updated}')>")