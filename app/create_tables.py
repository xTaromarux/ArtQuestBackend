from database import engine, Base
from models.difficulties import Difficulties
from models.users import Users
from models.posts import Posts
from models.progresses import Progresses
from models.courses import Courses
from models.pictures import Pictures
from sqlalchemy import inspect, text
from sqlalchemy.orm import configure_mappers

# Bezpośrednie usunięcie zależnych tabel `pictures` i `courses` przy użyciu CASCADE
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS pictures CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS courses CASCADE"))

# Odświeżenie metadanych bazy po usunięciu tabel
Base.metadata.reflect(bind=engine)

# Próba ponownego usunięcia pozostałych tabel, aby upewnić się, że baza jest wyczyszczona
Base.metadata.drop_all(bind=engine, checkfirst=True)
print("Tabele zostały usunięte.")

# Debugowanie relacji w modelach, aby potwierdzić ich prawidłowość
for cls in [Courses, Progresses, Users, Difficulties]:
    print(f"{cls.__name__} relationships: {inspect(cls).relationships.keys()}")

# Tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)
print("Tabele zostały utworzone.")
