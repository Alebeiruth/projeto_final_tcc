import os
import shutil
from pathlib import Path

def organize_jaffe_dataset(source_dir, output_dir):
    """
    Organize JAFFE dataset images into emotion folders based on filename codes.
    
    The filename format follows pattern like 'KM-HA1.tiff' where:
    - 'KM' is the poser ID
    - 'HA' is the emotion code:
        - NE: neutral
        - HA: happy
        - SA: sadness
        - SU: surprise
        - AN: anger
        - DI: disgust
        - FE: fear
    - '1' is the pose number
    """
    # Create emotion directories if they don't exist
    emotion_dirs = {
        'NE': 'neutral',
        'HA': 'happy', 
        'SA': 'sadness',
        'SU': 'surprise',
        'AN': 'anger',
        'DI': 'disgust',
        'FE': 'fear'
    }
    
    # Create output directories
    for emotion_name in emotion_dirs.values():
        os.makedirs(os.path.join(output_dir, emotion_name), exist_ok=True)
    
    # Process each file in the source directory
    for filename in os.listdir(source_dir):
        # Check if it's a valid image file (.tiff format according to README)
        if filename.lower().endswith('.tiff'):
            # Extract emotion code (positions 4-5 in the filename as per README)
            if len(filename) >= 5:
                emotion_code = filename[3:5]
                
                if emotion_code in emotion_dirs:
                    # Create source and destination paths
                    src_path = os.path.join(source_dir, filename)
                    dst_dir = os.path.join(output_dir, emotion_dirs[emotion_code])
                    dst_path = os.path.join(dst_dir, filename)
                    
                    # Copy the file to the appropriate emotion directory
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied {filename} to {emotion_dirs[emotion_code]} folder")
                else:
                    print(f"Unknown emotion code in {filename}, skipping")
            else:
                print(f"Filename {filename} too short to extract emotion code, skipping")

if __name__ == "__main__":
    # Set your source and output directories here
    source_directory = f'jaffe'  # Replace with your source directory
    output_directory = f'Jaffe Organizado'  # Replace with your output directory
    
    organize_jaffe_dataset(source_directory, output_directory)
    print("Organization complete!")