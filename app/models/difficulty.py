from sqlalchemy import Column, Integer, UUID, String


class Difficulty:
    __tablename__ = 'difficulty'
    id = Column(UUID, primary_key=True)
    name = Column(String)
    color = Column(String)
    score = Column(Integer)
    exercises_id = Column(UUID)

    def __repr__(self):
        return (f"<Difficulty(id={self.id}, name='{self.name}', "
                f"color='{self. color}', score='{self.score}', exercises_id='{self.exercises_id})>")