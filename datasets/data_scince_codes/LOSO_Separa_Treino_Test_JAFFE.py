import os
import numpy as np
import re
import random
import shutil
from pathlib import Path

# Define paths
base_dir = 'jaffe'  # Replace with your actual path to the JAFFE dataset
output_dir = 'Jaffe_LOSO'  # Replace with your desired output directory

# Create output directories if they don't exist
os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'train'), exist_ok=True)

# Function to extract subject ID from filename
def extract_subject_id(filename):
    # JAFFE filenames follow patterns like KA.AN1.39.png, KL.AN2.168.png, etc.
    match = re.match(r'([A-Z]{2})\.', filename)
    if match:
        return match.group(1)
    return None

def perform_single_loso(base_dir, output_dir):
    # Dictionary to store all subject IDs and their files by emotion
    subjects_data = {}
    
    # Collect all subjects and their files
    for emotion_folder in os.listdir(base_dir):
        emotion_path = os.path.join(base_dir, emotion_folder)
        if os.path.isdir(emotion_path):
            # Create output emotion folders
            os.makedirs(os.path.join(output_dir, 'test', emotion_folder), exist_ok=True)
            os.makedirs(os.path.join(output_dir, 'train', emotion_folder), exist_ok=True)
            
            for file in os.listdir(emotion_path):
                subject_id = extract_subject_id(file)
                if subject_id:
                    if subject_id not in subjects_data:
                        subjects_data[subject_id] = {}
                    
                    if emotion_folder not in subjects_data[subject_id]:
                        subjects_data[subject_id][emotion_folder] = []
                    
                    subjects_data[subject_id][emotion_folder].append(
                        (os.path.join(emotion_path, file), file)
                    )
    
    # Get all unique subject IDs
    all_subjects = list(subjects_data.keys())
    print(f"Found {len(all_subjects)} unique subjects: {', '.join(all_subjects)}")
    
    # Select one subject to leave out for LOSO
    left_out_subject = random.choice(all_subjects)
    
    # Get remaining subjects (excluding the left-out subject)
    remaining_subjects = [s for s in all_subjects if s != left_out_subject]
    
    # Randomly select 2 subjects from remaining for testing (20% of 10 subjects)
    test_subjects = random.sample(remaining_subjects, 2)
    
    # The rest go to training
    train_subjects = [s for s in remaining_subjects if s not in test_subjects]
    
    print(f"Left-out subject (LOSO): {left_out_subject}")
    print(f"Additional test subjects: {', '.join(test_subjects)}")
    print(f"Train subjects: {', '.join(train_subjects)}")
    
    # Copy left-out subject + test subjects files to test directory
    test_subjects_all = [left_out_subject] + test_subjects
    for subject in test_subjects_all:
        if subject in subjects_data:
            for emotion, files in subjects_data[subject].items():
                for file_path, filename in files:
                    dest_path = os.path.join(output_dir, 'test', emotion, filename)
                    shutil.copy2(file_path, dest_path)
    
    # Copy train subjects' files to train directory
    for subject in train_subjects:
        if subject in subjects_data:
            for emotion, files in subjects_data[subject].items():
                for file_path, filename in files:
                    dest_path = os.path.join(output_dir, 'train', emotion, filename)
                    shutil.copy2(file_path, dest_path)
    
    print("LOSO and subject-based train/test split completed")
    print(f"Test set: 3 subjects ({left_out_subject} and {', '.join(test_subjects)})")
    print(f"Train set: 7 subjects ({', '.join(train_subjects)})")

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    perform_single_loso(base_dir, output_dir)