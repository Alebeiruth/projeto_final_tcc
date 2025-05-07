import os
import numpy as np
import re
import random
import shutil
from pathlib import Path

# Define paths
base_dir = 'ck+'  # Replace with your actual path to the CK+ dataset
output_dir = 'ck+_LOSO'  # Replace with your desired output directory

# Create output directories if they don't exist
os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'train'), exist_ok=True)

# Function to extract subject ID from CK+ filename
def extract_subject_id(filename):
    # CK+ typically has filenames like S005_001_00000001.png or similar
    # The first part usually represents the subject ID
    match = re.match(r'S(\d+)_', filename)
    if match:
        return f"S{match.group(1)}"
    return None

def perform_single_loso_ck_plus(base_dir, output_dir):
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
    print(f"Found {len(all_subjects)} unique subjects: {', '.join(all_subjects[:10])}...")
    
    # Select one subject to leave out for LOSO
    left_out_subject = random.choice(all_subjects)
    
    # Get remaining subjects (excluding the left-out subject)
    remaining_subjects = [s for s in all_subjects if s != left_out_subject]
    
    # Randomly select 20% of remaining subjects for testing 
    num_test_subjects = max(2, int(0.2 * len(all_subjects)))
    test_subjects = random.sample(remaining_subjects, num_test_subjects)
    
    # The rest go to training
    train_subjects = [s for s in remaining_subjects if s not in test_subjects]
    
    print(f"Left-out subject (LOSO): {left_out_subject}")
    print(f"Additional test subjects: {', '.join(test_subjects[:5])}...")
    print(f"Train subjects: {', '.join(train_subjects[:5])}...")
    
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
    
    # Count files for reporting
    test_files = sum(len(os.listdir(os.path.join(output_dir, 'test', emotion))) 
                     for emotion in os.listdir(os.path.join(output_dir, 'test')))
    train_files = sum(len(os.listdir(os.path.join(output_dir, 'train', emotion))) 
                      for emotion in os.listdir(os.path.join(output_dir, 'train')))
    
    print("LOSO and subject-based train/test split completed")
    print(f"Test set: {len(test_subjects_all)} subjects with {test_files} files")
    print(f"Train set: {len(train_subjects)} subjects with {train_files} files")

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    perform_single_loso_ck_plus(base_dir, output_dir)