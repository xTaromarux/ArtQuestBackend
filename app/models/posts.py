import sqlalchemy as _sql
from database import Base

class Posts(Base):
    __tablename__ = 'posts'
    id = _sql.Column(_sql.UUID, primary_key=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    state = _sql.Column(_sql.String, index=True)
    date_added = _sql.Column(_sql.String, index=True)
    date_updated = _sql.Column(_sql.String, index=True)
    picture_id = _sql.Column(_sql.UUID, index=True)
    user_id = _sql.Column(_sql.UUID, index=True)

    def __repr__(self):
        return (f"<Posts(id={self.id}, title='{self.title}', "
                f"description='{self. description}', state='{self.state}', date_added='{self.date_added}, "
                f"date_updated='{self.date_updated}, picture_id='{self.picture_id}, user_id='{self.user_id})>")