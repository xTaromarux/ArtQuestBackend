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
    Loads an image from binary data (blob) and converts it to Torch Tensor format.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Load image and convert to RGB
        transform = transforms.Compose([
            transforms.ToTensor(),  # Convert to tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalization
        ])
        return transform(image)
    except Exception as e:
        raise ValueError(f"Image loading error: {e}")

def load_api_key():
     # Load environment variables from the .env file
    load_dotenv()

    # Read API key from loaded variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if openai.api_key:
        print("The API key has been loaded.")
    else:
        print("API key missing. Make sure the .env file is correct.")

def set_device():
    """Uputs the computing device (GPU if available)."""
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def initialize_models(device):
    """Initializes the feature extractor and LightGlue matcher."""
    extractor = SuperPoint(max_num_keypoints=2048).eval().to(device)
    matcher = LightGlue(features='superpoint').eval().to(device)
    return extractor, matcher

def process_images(image1_bytes, image2_bytes):
    """
    The main function that processes images in binary format.
    
    Args:
        image1_bytes: The contents of the first image in binary format.
        image2_bytes: The contents of the second image in binary format.

    Returns:
        message: the message generated from the image comparison.
    """
    device = set_device()
    extractor, matcher = initialize_models(device)

    try:
        # Load images from binary data
        image1 = load_image_from_bytes(image1_bytes)
        image2 = load_image_from_bytes(image2_bytes)

        # Feature extraction
        feats1 = extractor.extract(image1.to(device))
        feats2 = extractor.extract(image2.to(device))

        # Matching features
        matches01 = matcher({'image0': feats1, 'image1': feats2})
        feats1, feats2, matches01 = [rbd(x) for x in [feats1, feats2, matches01]]

        # Calculating common points
        kpts1, kpts2 = feats1['keypoints'], feats2['keypoints']
        matches = matches01['matches']
        num_common_points = len(matches)
        total_keypoints = (len(kpts1) + len(kpts2)) / 2
        percentage_common_points = (num_common_points / total_keypoints) * 100

        # Log the result
        print(f"Number of common points: {num_common_points}")
        print(f"Percentage of common points: {percentage_common_points:.2f}%")

    
        message = generate_message(percentage_common_points, chatgpt_enabled=False)
        return message

    except Exception as e:
        raise ValueError(f"Error during image processing: {e}")

def generate_message(percentage_common_points, chatgpt_enabled):
    """
    Generates a message based on the percentage of matches.

    Args:
        percentage_common_points: Percentage of match.
        chatgpt_enabled: Whether to use ChatGPT to generate the message.

    Returns:
        message: message.
    """
    percentage_common_points = round(percentage_common_points, 1)
    if percentage_common_points < 30:
        local_message = "Next time will be better. You have " + str(percentage_common_points) + "%"
    elif 30 <= percentage_common_points < 60:
        local_message = "You're doing good. You have " + str(percentage_common_points) + "%"
    elif 60 <= percentage_common_points < 90:
        local_message = "Super wow. You have " + str(percentage_common_points) + "%"
    else:
        local_message = "Ideal. You have " + str(percentage_common_points) + "%"

    if not chatgpt_enabled:
        return local_message
    
    # Using ChatGPT (optional)
    try:
        load_api_key()
        prompt = f"The result shows a matching percentage of {percentage_common_points}. Please provide a motivational message. (below 30%. Please provide a motivational message, such as better luck next time between 30% and 60%. Please provide a message saying you're doing well, between 60% and 90%. Please provide an encouraging message like 'super wow'., 90% or more. Please provide a message saying 'perfect'. Return also number of percentage points with % mark"
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
