from sqlalchemy import Column, UUID, String


class Posts:
    __tablename__ = 'posts'
    id = Column(UUID, primary_key=True)
    title = Column(String)
    description = Column(String)
    state = Column(String)
    date_added = Column(String)
    date_updated = Column(String)
    picture_id = Column(UUID)
    user_id = Column(UUID)

    def __repr__(self):
        return (f"<Posts(id={self.id}, title='{self.title}', "
                f"description='{self. description}', state='{self.state}', date_added='{self.date_added}, "
                f"date_updated='{self.date_updated}, picture_id='{self.picture_id}, user_id='{self.user_id})>")
