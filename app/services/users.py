from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models.users import Users
from models.pictures import Pictures
from schemas.Susers import Users as UsersSchema, UsersMinimalResponse  # Użyj schematu Pydantic dla serializacji danych

router = APIRouter()

@router.get("/user/{user_id}/minimal", response_model=UsersMinimalResponse)
def get_user_minimal_details(user_id: UUID, db: Session = Depends(get_db)):
    """
    Pobiera minimalne szczegóły użytkownika (login, mail, user_name) na podstawie user_id.
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def convert_image_to_binary(image_file: UploadFile) -> bytes:
    """
    Konwertuje plik obrazu na dane binarne.
    """
    return image_file.file.read()

@router.put("/user/{user_id}/edit", response_model=UsersMinimalResponse)
async def update_user(
    user_id: UUID,
    login: str,
    mail: str,
    user_name: str,
    picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Edytuje login, mail, user_name użytkownika oraz zapisuje nowy obraz w formacie blob w tabeli pictures.
    """
    # Pobranie użytkownika z bazy danych
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Aktualizacja danych użytkownika
    user.login = login
    user.mail = mail
    user.user_name = user_name

    # Jeśli przekazano obraz, zaktualizuj zdjęcie profilowe
    if picture:
        # Pobierz istniejące zdjęcie lub utwórz nowe
        if user.picture_id:
            user_picture = db.query(Pictures).filter(Pictures.id == user.picture_id).first()
        else:
            user_picture = Pictures(id=UUID(uuid4().hex))  # Tworzenie nowego wpisu w tabeli Pictures
            db.add(user_picture)
            db.flush()  # Upewnij się, że nowy obraz ma ID

            # Przypisz ID nowego zdjęcia do użytkownika
            user.picture_id = user_picture.id

        # Konwertuj obraz do danych binarnych i zapisz
        user_picture.picture = convert_image_to_binary(picture)

    # Zapisz zmiany
    db.commit()

    # Przygotowanie odpowiedzi
    return UsersMinimalResponse(login=user.login, mail=user.mail, user_name=user.user_name)

@router.delete("/user/{user_id}", response_model=dict)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Usuwa wszystkie informacje dotyczące użytkownika na podstawie user_id, w tym powiązane zdjęcie.
    """
    # Pobranie użytkownika z bazy danych
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Sprawdzenie, czy użytkownik ma powiązane zdjęcie i jego usunięcie
    if user.picture_id:
        picture = db.query(Pictures).filter(Pictures.id == user.picture_id).first()
        if picture:
            db.delete(picture)
    
    # Usunięcie wszystkich powiązanych danych użytkownika (posty, komentarze, itp.)
    # Jeśli masz powiązania kaskadowe, te kroki mogą nie być konieczne
    # W przeciwnym razie dodaj usuwanie postów, komentarzy, osiągnięć itp.
    # db.query(...).filter(...).delete() dla każdej powiązanej tabeli

    # Usunięcie użytkownika
    db.delete(user)
    db.commit()
    
    return {"message": "User and associated data deleted successfully"}