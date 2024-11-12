from sqlalchemy import Column, Integer, UUID


class Progress:
    __tablename__ = 'progress'
    id = Column(UUID, primary_key=True)
    implementation_stage = Column(Integer)
    picture_id = Column(UUID)
    exercises_id = Column(UUID)
    user_id = Column(UUID)


    def __repr__(self):
        return (f"<Progress(id={self.id}, implementation_stage='{self.implementation_stage}', "
                f"picture_id='{self. picture_id}', exercises_id='{self.exercises_id}', user_id='{self.user_id})>")
