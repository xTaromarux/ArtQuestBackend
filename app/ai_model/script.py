from app.ai_model.lightglue import LightGlue, SuperPoint
from app.ai_model.lightglue.utils import rbd
import torch
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import io
from torchvision import transforms

def load_image_from_bytes(image_bytes):
    """
    Ładuje obraz z danych binarnych (blob) i konwertuje go na format Torch Tensor.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Załaduj obraz i przekonwertuj na RGB
        transform = transforms.Compose([
            transforms.ToTensor(),  # Konwertuj na tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalizacja
        ])
        return transform(image)
    except Exception as e:
        raise ValueError(f"Błąd wczytywania obrazu: {e}")

def load_api_key():
     # Załaduj zmienne środowiskowe z pliku .env
    load_dotenv()

    # Odczytaj klucz API z załadowanych zmiennych
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if openai.api_key:
        print("Klucz API został załadowany.")
    else:
        print("Brak klucza API. Upewnij się, że plik .env jest poprawny.")

def set_device():
    """Ustawia urządzenie obliczeniowe (GPU jeśli dostępne)."""
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def initialize_models(device):
    """Inicjalizuje ekstraktor cech i dopasowywacz LightGlue."""
    extractor = SuperPoint(max_num_keypoints=2048).eval().to(device)
    matcher = LightGlue(features='superpoint').eval().to(device)
    return extractor, matcher

def process_images(image1_bytes, image2_bytes):
    """
    Główna funkcja przetwarzająca obrazy w formacie binarnym.
    
    Args:
        image1_bytes: Zawartość pierwszego obrazu w formacie binarnym.
        image2_bytes: Zawartość drugiego obrazu w formacie binarnym.

    Returns:
        message: Komunikat wygenerowany na podstawie porównania obrazów.
    """
    device = set_device()
    extractor, matcher = initialize_models(device)

    try:
        # Wczytaj obrazy z danych binarnych
        image1 = load_image_from_bytes(image1_bytes)
        image2 = load_image_from_bytes(image2_bytes)

        # Ekstrakcja cech
        feats1 = extractor.extract(image1.to(device))
        feats2 = extractor.extract(image2.to(device))

        # Dopasowanie cech
        matches01 = matcher({'image0': feats1, 'image1': feats2})
        feats1, feats2, matches01 = [rbd(x) for x in [feats1, feats2, matches01]]

        # Obliczanie wspólnych punktów
        kpts1, kpts2 = feats1['keypoints'], feats2['keypoints']
        matches = matches01['matches']
        num_common_points = len(matches)
        total_keypoints = (len(kpts1) + len(kpts2)) / 2
        percentage_common_points = (num_common_points / total_keypoints) * 100

        # Loguj wynik
        print(f"Liczba wspólnych punktów: {num_common_points}")
        print(f"Procent wspólnych punktów: {percentage_common_points:.2f}%")

        # Wygenerowanie wiadomości
        message = generate_message(percentage_common_points, chatgpt_enabled=False)
        return message

    except Exception as e:
        raise ValueError(f"Błąd podczas przetwarzania obrazów: {e}")

def generate_message(percentage_common_points, chatgpt_enabled):
    """
    Generuje wiadomość na podstawie procentu dopasowania.

    Args:
        percentage_common_points: Procent dopasowania.
        chatgpt_enabled: Czy używać ChatGPT do generowania wiadomości.

    Returns:
        message: Wiadomość.
    """
    if percentage_common_points < 5:
        local_message = "Następnym razem będzie lepiej"
    elif 5 <= percentage_common_points < 10:
        local_message = "Dobrze ci idzie"
    elif 10 <= percentage_common_points < 15:
        local_message = "Super wow"
    else:
        local_message = "Ideał"

    if not chatgpt_enabled:
        return local_message

    # Użycie ChatGPT (opcjonalnie)
    try:
        load_api_key()
        prompt = f"The result shows a matching percentage of {percentage_common_points}%. Please provide a motivational message."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"ChatGPT error: {e}")
        return local_message
