from sqlalchemy import Column, Integer, UUID, String


class Exercises:
    __tablename__ = 'exercises'
    id = Column(UUID, primary_key=True)
    state = Column(String)
    description = Column(String)
    title = Column(Integer)
    picture_id = Column(UUID)

    def __repr__(self):
        return (f"<Exercises(id={self.id}, state='{self.state}', "
                f"description='{self. description}', title='{self.title}', picture_id='{self.picture_id})>")
