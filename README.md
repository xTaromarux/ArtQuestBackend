# ArtQuestBackend

ArtQuestBackend to backendowa aplikacja wspierająca platformę ArtQuest, która łączy artystów i miłośników sztuki. Projekt umożliwia zarządzanie użytkownikami, kursami, postami oraz innymi funkcjami wspierającymi rozwój artystyczny społeczności.

## Spis treści

- [Technologie](#technologie)
- [Instalacja](#instalacja)
- [Uruchomienie](#uruchomienie)
- [Struktura bazy danych](#struktura-bazy-danych)
- [Użycie](#użycie)
- [Funkcjonalności](#funkcjonalności)
- [Przykłady API](#przykłady-api)
- [Autor](#autor)

---

## Technologie

Projekt został stworzony z wykorzystaniem następujących technologii:
- **Python 3.11**
- **FastAPI** – framework do budowy aplikacji webowych
- **SQLAlchemy** – ORM do pracy z bazami danych
- **PostgreSQL** – baza danych
- **Pandas** – przetwarzanie danych z plików CSV
- **Uvicorn** – serwer ASGI

---

## Instalacja

### Wymagania wstępne
1. Python 3.11
2. PostgreSQL
3. Virtualenv (opcjonalnie, dla izolacji środowiska)

### Kroki instalacji
1. Sklonuj repozytorium:
   ```bash
   git clone <url_do_repozytorium>
   cd ArtQuestBackend
   ```

2. Stwórz wirtualne środowisko:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

4. Skonfiguruj bazę danych PostgreSQL i ustaw zmienne środowiskowe w pliku `.env`:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database_name>
   ```

---

## Uruchomienie

### Lokalny serwer
Aby uruchomić aplikację, wykonaj następujące kroki:
1. Zainicjalizuj bazę danych:
   ```bash
   python3 app/populate_database.py
   ```

2. Uruchom serwer:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Aplikacja będzie dostępna pod adresem:
   ```
   http://127.0.0.1:8000
   ```

### Dokumentacja API
FastAPI automatycznie generuje dokumentację API. Możesz ją zobaczyć pod:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Struktura bazy danych

Aplikacja wykorzystuje PostgreSQL z następującymi kluczowymi tabelami:
- **users** – informacje o użytkownikach
- **courses** – kursy dostępne na platformie
- **pictures** – obrazy związane z postami, ćwiczeniami i osiągnięciami
- **posts** – posty użytkowników
- **comments** – komentarze na postach
- **views** – widoki dla ćwiczeń
- **statistics** – statystyki użytkowników
- **achievements** – osiągnięcia użytkowników

---

## Funkcjonalności

- Zarządzanie użytkownikami (rejestracja, logowanie).
- Dodawanie i przeglądanie kursów.
- Dodawanie postów i komentarzy.
- Obsługa obrazów w kursach, postach i ćwiczeniach.
- Automatyczne wczytywanie danych z plików CSV.

---

## Przykłady API

### Pobranie listy użytkowników
**GET** `/api/users`
```json
[
  {
    "id": "0f41b706-85a8-4457-8046-132f5505b47d",
    "login": "Mikę",
    "user_name": "BoyAs",
    "mail": "user1@example.com"
  }
]
```

### Dodanie nowego komentarza
**POST** `/api/comments`
```json
{
  "description": "Wow, świetny rysunek!",
  "reactions": 5,
  "user_id": "387e1c9f-83c0-4ca4-ac59-47a16529e867",
  "post_id": "a66e0f77-bdec-4cf7-ae9d-a88eb8edc34f"
}
```

---

## Autor

Projekt został stworzony przez Małgorzatę Tomiło.  
E-mail: gosiatomilo@gmail.com  

