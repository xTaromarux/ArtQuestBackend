from sqlalchemy import Column, UUID, String, Date


class Users:
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True)
    group = Column(String)
    mail = Column(String)
    login = Column(String)
    password = Column(String)
    date_added = Column(Date)
    date_updated = Column(Date)

    def __repr__(self):
        return (f"<Users(id={self.id}, group='{self.group}', mail='{self.mail}',"
                f" login='{self.login}', password='{self.password}, date_added='{self.date_added},  "
                f"date_updated='{self.date_updated}')>")