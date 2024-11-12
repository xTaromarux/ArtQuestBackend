import uuid
import os
from sqlalchemy.orm import Session
from database import engine, get_db
from models.users import Users
from models.posts import Posts
from PIL import Image
import io

# Function to convert images to binary
def convert_image_to_binary(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()

# Function to add sample data
def add_sample_data(db: Session):
    # Add sample users with avatars
    avatar_paths = [
        "db_scripts/images/avatars_examples/Open_Peeps_-_Avatar.png",
        "db_scripts/images/avatars_examples/Open_Peeps_-_Avatar_1.png",
        "db_scripts/images/avatars_examples/Open_Peeps_-_Avatar_2.png",
        "db_scripts/images/avatars_examples/Open_Peeps_-_Avatar_3.png",
        "db_scripts/images/avatars_examples/Open_Peeps_-_Avatar_4.png",
    ]
    users_data = [
        {
            "login": "artlover123",
            "password": "Art!st2024",
            "mail": "artlover123@example.com",
            "group": None,
            "name": "ArtLover123",
            "avatar": convert_image_to_binary(avatar_paths[0])
        },
        {
            "login": "creativesoul",
            "password": "Cre@tive123",
            "mail": "creativesoul@example.com",
            "group": None,
            "name": "CreativeSoul",
            "avatar": convert_image_to_binary(avatar_paths[1])
        },
        {
            "login": "sketchmaster",
            "password": "SketchM@ster",
            "mail": "sketchmaster@example.com",
            "group": None,
            "name": "SketchMaster",
            "avatar": convert_image_to_binary(avatar_paths[2])
        },
        {
            "login": "paintpro",
            "password": "P@intPro2024",
            "mail": "paintpro@example.com",
            "group": None,
            "name": "PaintPro",
            "avatar": convert_image_to_binary(avatar_paths[3])
        },
        {
            "login": "colorcrafter",
            "password": "Color!Craft",
            "mail": "colorcrafter@example.com",
            "group": None,
            "name": "ColorCrafter",
            "avatar": convert_image_to_binary(avatar_paths[4])
        },
        {
            "login": "drawguru",
            "password": "Dr@wGurU123",
            "mail": "drawguru@example.com",
            "group": None,
            "name": "DrawGuru",
            "avatar": None  # No avatar for the sixth user
        }
    ]
    users = [Users(**user_data) for user_data in users_data]
    db.add_all(users)
    db.commit()

    # Add sample posts with pictures
    post_descriptions = [
        "Przypominamy, że codzienna praktyka to klucz do mistrzostwa! 🎨 Nie zapomnijcie o dzisiejszej sesji rysunku. Co dzisiaj stworzycie? #CodziennaPraktyka #Sztuka",
        "Czy wiecie, że Leonardo da Vinci spędzał godziny na obserwacji przyrody? 🌿 Czerpcie inspirację z otaczającego Was świata! #Inspiracja #SztukaWNaturze",
        "Nauka nowych technik to świetny sposób na rozwijanie swoich umiejętności. Spróbujcie dzisiaj techniki cieniowania! 🖤 #NoweTechniki #Cieniowanie",
        "Warto wracać do swoich starych prac i obserwować postępy. To niesamowite, jak bardzo można się rozwinąć! 🖼️ #Progres #EwolucjaSztuki",
        "Kolory mają moc wyrażania emocji. Eksperymentujcie z paletami barw i odkryjcie, jak wpływają na Wasze prace! 🌈 #MocKolorów #Eksperymenty",
        "Nie bójcie się popełniać błędów – to one uczą nas najwięcej. Każdy szkic to krok w stronę doskonałości! ✏️ #Błędy #NaukaNaBłędach",
    ]
    post_titles = [
        "CodziennaPraktyka",
        "SztukaWNaturze",
        "NoweTechniki",
        "EwolucjaSztuki",
        "MocKolorów",
        "NaukaNaBłędach",
    ]
    posts = [
        Posts(
            title=post_titles[i], 
            description=post_descriptions[i],
            user_id=users[i].id,
            picture=convert_image_to_binary(avatar_paths[i % len(avatar_paths)]) if i < len(avatar_paths) else None
        )
        for i in range(6)
    ]
    db.add_all(posts)
    db.commit()

# Main function to create tables and add sample data
def main():
    from database import Base
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Add sample data
    db = next(get_db())
    add_sample_data(db)
    print("Sample data added successfully.")

if __name__ == "__main__":
    main()
