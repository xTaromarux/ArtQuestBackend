from pathlib import Path
from lightglue import LightGlue, SuperPoint, DISK
from lightglue.utils import load_image, rbd
from lightglue import viz2d
import torch
import os
import openai
import matplotlib.pyplot as plt
from dotenv import load_dotenv




torch.set_grad_enabled(False)

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

def load_images(images_path):
    """Ładuje obrazy z określonej ścieżki."""
    image0 = load_image(images_path / 'Obraz.jpg')
    image1 = load_image(images_path / 'bb.jpg')
    return image0, image1

def initialize_models(device):
    """Inicjalizuje ekstraktor cech i dopasowywacz LightGlue."""
    extractor = SuperPoint(max_num_keypoints=2048).eval().to(device)
    matcher = LightGlue(features='superpoint').eval().to(device)
    return extractor, matcher

def extract_features(extractor, image0, image1, device):
    """Ekstrahuje cechy z obrazów."""
    feats0 = extractor.extract(image0.to(device))
    feats1 = extractor.extract(image1.to(device))
    return feats0, feats1

def match_features(matcher, feats0, feats1):
    """Dopasowuje cechy między dwoma obrazami."""
    matches01 = matcher({'image0': feats0, 'image1': feats1})
    feats0, feats1, matches01 = [rbd(x) for x in [feats0, feats1, matches01]]
    return feats0, feats1, matches01

def calculate_common_points(matches01, kpts0, kpts1):
    """Oblicza liczbę wspólnych punktów oraz procentową ich ilość."""
    matches = matches01['matches']
    num_common_points = len(matches)
    total_keypoints = (len(kpts0) + len(kpts1)) / 2
    percentage_common_points = (num_common_points / total_keypoints) * 100
    return num_common_points, percentage_common_points

def get_chatgpt_message(percentage_common_points, chatgpt_state):
    """Generuje odpowiedni komunikat z modelu ChatGPT lub lokalny komunikat w przypadku błędu."""
    if percentage_common_points < 5:
        local_message = "Następnym razem będzie lepiej"
    elif 5 <= percentage_common_points < 10:
        local_message = "Dobrze ci idzie"
    elif 10 <= percentage_common_points < 15:
        local_message = "Super wow"
    else:
        local_message = "Ideał"

    # Sprawdzamy, czy ChatGPT jest dostępny i włączony
    if not chatgpt_state:
        return local_message  # Zwracamy lokalny komunikat, gdy ChatGPT jest wyłączony

    # Próba wywołania API OpenAI
    try:
        prompt = f"The result shows a matching percentage of {percentage_common_points}%. Please provide a motivational message. (below 5%. Please provide a motivational message, such as better luck next time between 5% and 10%. Please provide a message saying you're doing well, between 10% and 15%. Please provide an encouraging message like 'super wow'., 15% or more. Please provide a message saying 'perfect'."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Wyodrębnienie treści komunikatu z odpowiedzi
        message = response['choices'][0]['message']['content']
        return message

    except (openai.error.RateLimitError, openai.error.AuthenticationError, openai.error.APIError):
        # Obsługa błędu limitu zapytań lub błędu autoryzacji/klucza, zwracając lokalny komunikat
        return local_message




def visualize_matches(image0, image1, m_kpts0, m_kpts1, stop_layers):
    """Wizualizuje dopasowania między dwoma obrazami."""
    axes = viz2d.plot_images([image0, image1])
    viz2d.plot_matches(m_kpts0, m_kpts1, color='lime', lw=0.2)
    viz2d.add_text(0, f'Stop after {stop_layers} layers', fs=20)
    plt.show()

def visualize_keypoints(image0, image1, kpts0, kpts1, prune0, prune1):
    """Wizualizuje kluczowe punkty po odcięciu."""
    kpc0, kpc1 = viz2d.cm_prune(prune0), viz2d.cm_prune(prune1)
    viz2d.plot_images([image0, image1])
    viz2d.plot_keypoints([kpts0, kpts1], colors=[kpc0, kpc1], ps=10)
    plt.show()

def main():
    # Ustawienia
    load_api_key()
    images_path = Path(os.path.join(os.path.dirname(__file__), "assets"))
    device = set_device()
    
    # Inicjalizacja modeli
    extractor, matcher = initialize_models(device)
    
    # Ładowanie obrazów
    image0, image1 = load_images(images_path)
    
    # Ekstrakcja cech
    feats0, feats1 = extract_features(extractor, image0, image1, device)
    
    # Dopasowanie cech
    feats0, feats1, matches01 = match_features(matcher, feats0, feats1)
    
    # Pobranie kluczowych punktów i dopasowań
    kpts0, kpts1, matches = feats0['keypoints'], feats1['keypoints'], matches01['matches']
    m_kpts0, m_kpts1 = kpts0[matches[..., 0]], kpts1[matches[..., 1]]
    
    # Obliczanie wspólnych punktów
    num_common_points, percentage_common_points = calculate_common_points(matches01, kpts0, kpts1)
    print(f"Number of common points: {num_common_points}")
    print(f"Percentage of common points: {percentage_common_points:.2f}%")
    
    # Wywołanie funkcji get_chatgpt_message i wyświetlenie komunikatu
    message = get_chatgpt_message(percentage_common_points, False)
    print(message)
    
    # Wizualizacja dopasowań
    visualize_matches(image0, image1, m_kpts0, m_kpts1, matches01["stop"])
    
    # Wizualizacja kluczowych punktów po odcięciu
    visualize_keypoints(image0, image1, kpts0, kpts1, matches01['prune0'], matches01['prune1'])

# Uruchomienie głównej funkcji
if __name__ == "__main__":
    main()
