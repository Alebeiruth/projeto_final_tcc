import pandas as pd
import numpy as np
from PIL import Image
import os

def convert_fer2013_to_png(csv_path, output_dir):
    """
    Converts FER2013 dataset from CSV format to PNG images
    
    Parameters:
    csv_path (str): Path to the FER2013 CSV file
    output_dir (str): Directory to save the PNG images
    """

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Read the CSV file
    print("Reading CSV file...")
    data = pd.read_csv(csv_path)
    
    # Process each row in the CSV
    total_rows = len(data)
    for i, row in enumerate(data.iterrows()):
        # Print progress
        if i % 100 == 0:
            print(f"Processing image {i}/{total_rows}...")
            
        row = row[1]  # Get the pandas series from the tuple
        
        # Get the emotion label and pixel values
        emotion = row['emotion']
        pixels = row['pixels'].split()
        
        # Convert to integer values
        pixels = [int(pixel) for pixel in pixels]
        
        # The original FER2013 images are 48x48 pixels
        image_array = np.array(pixels, dtype=np.uint8).reshape(48, 48)
        
        # Create a PIL Image
        image = Image.fromarray(image_array)
        
        # Map emotion numbers to names
        emotion_map = {
            0: "anger",
            1: "disgust", 
            2: "fear",
            3: "happy",
            4: "neutral",
            5: "sadness",
            6: "surprise"
        }
        
        # Get emotion name from the map
        emotion_name = emotion_map.get(emotion, str(emotion))
        
        # Create subdirectory for this emotion if it doesn't exist
        emotion_dir = os.path.join(output_dir, emotion_name)
        if not os.path.exists(emotion_dir):
            os.makedirs(emotion_dir)
        
        # Save the image
        # If there's an 'Usage' column, use it as part of the filename
        if 'Usage' in row:
            usage = row['Usage']
            filename = f"{usage}_{i}.png"
        else:
            filename = f"{i}.png"
        
        image_path = os.path.join(emotion_dir, filename)
        image.save(image_path)
    
    print(f"Conversion complete! {total_rows} images saved to {output_dir}")
    
if __name__ == "__main__":
    # Caminho fixo para o arquivo CSV e diretório de saída
    csv_path = 'fer2013.csv\\fer2013.csv'
    output_dir = 'fer2013'
    
    # Executar a conversão com os caminhos definidos
    convert_fer2013_to_png(csv_path, output_dir)