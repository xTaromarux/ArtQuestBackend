from sqlalchemy import Column, UUID, String, BLOB


class Pictures:
    __tablename__ = 'pictures'
    id = Column(UUID, primary_key=True)
    blob = Column(BLOB)
    description = Column(String)
    date_added = Column(String)

    def __repr__(self):
        return (f"<Pictures(id={self.id}, blob='{self.blob}', "
                f"description='{self. description}', date_added='{self.date_added}')>")
