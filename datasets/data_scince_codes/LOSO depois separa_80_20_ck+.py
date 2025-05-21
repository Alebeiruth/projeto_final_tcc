import os
import numpy as np
import re
import random
import shutil
from pathlib import Path
from collections import defaultdict

# Define paths
base_dir = 'datasets\ck+'  # Replace with your actual path to the CK+ dataset
output_dir = 'datasets\ck+_LOSO'  # Replace with your desired output directory

# Create output directories if they don't exist
os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'train'), exist_ok=True)

# Function to extract subject ID from CK+ filename
def extract_subject_id(filename):
    # CK+ typically has filenames like S005_001_00000001.png or similar
    match = re.match(r'S(\d+)_', filename)
    if match:
        return f"S{match.group(1)}"
    return None

def perform_single_loso_ck_plus(base_dir, output_dir):
    # Dictionary to store all subject IDs and their files by emotion
    subjects_data = {}
    
    # Track subjects per emotion for better distribution
    emotion_subjects = defaultdict(list)
    
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
                        # Add this subject to the emotion_subjects tracker
                        emotion_subjects[emotion_folder].append(subject_id)
                    
                    subjects_data[subject_id][emotion_folder].append(
                        (os.path.join(emotion_path, file), file)
                    )
    
    # Get all unique subject IDs
    all_subjects = list(subjects_data.keys())
    print(f"Found {len(all_subjects)} unique subjects")
    
    # Print statistics about emotions and subjects
    for emotion, subjects in emotion_subjects.items():
        print(f"Emotion: {emotion} - {len(subjects)} subjects")
    
    # Select one subject to leave out for LOSO
    # Choose a subject that appears in multiple emotions for better coverage
    subject_emotion_counts = {subject: len(subjects_data[subject]) for subject in all_subjects}
    subjects_sorted = sorted(subject_emotion_counts.items(), key=lambda x: x[1], reverse=True)
    left_out_subject = subjects_sorted[0][0]  # Subject with most emotions
    
    print(f"Selected left-out subject (LOSO): {left_out_subject} (appears in {subject_emotion_counts[left_out_subject]} emotions)")
    
    # Strategy: For each emotion, ensure there are at least 2 subjects in test set
    # First, gather subjects for test (including left-out subject)
    test_subjects = [left_out_subject]
    train_subjects = []
    
    # For each emotion, ensure we have at least 2 subjects in test
    for emotion, emotion_subject_list in emotion_subjects.items():
        # Check how many subjects already in test_subjects have this emotion
        test_subjects_with_emotion = [s for s in test_subjects if s in emotion_subject_list]
        
        # If fewer than 2 test subjects have this emotion, add more
        if len(test_subjects_with_emotion) < 7:
            # Find subjects not already in test_subjects that have this emotion
            available_subjects = [s for s in emotion_subject_list if s != left_out_subject and s not in test_subjects]
            
            # How many more do we need to reach at least 2?
            num_needed = 7 - len(test_subjects_with_emotion)
            
            if available_subjects and num_needed > 0:
                # Add as many as we can up to num_needed
                additional_subjects = random.sample(available_subjects, min(num_needed, len(available_subjects)))
                test_subjects.extend(additional_subjects)
    
    # Finalize the train set (everyone not in test)
    train_subjects = [s for s in all_subjects if s not in test_subjects]
    
    print(f"Test subjects: {len(test_subjects)} subjects")
    print(f"Train subjects: {len(train_subjects)} subjects")
    
    # Copy left-out subject + test subjects files to test directory
    for subject in test_subjects:
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
    
    # Count files per emotion for reporting
    print("\nDistribution of files:")
    print("EMOTION\t\tTEST\tTRAIN")
    print("-" * 30)
    total_test = 0
    total_train = 0
    
    for emotion in os.listdir(os.path.join(output_dir, 'test')):
        if os.path.isdir(os.path.join(output_dir, 'test', emotion)):
            test_count = len(os.listdir(os.path.join(output_dir, 'test', emotion)))
            train_count = len(os.listdir(os.path.join(output_dir, 'train', emotion)))
            print(f"{emotion:<15}{test_count:>5}\t{train_count:>5}")
            total_test += test_count
            total_train += train_count
    
    print("-" * 30)
    print(f"TOTAL\t\t{total_test:>5}\t{total_train:>5}")
    
    print("\nLOSO and subject-based train/test split completed")
    print(f"Overall split: {total_test/(total_test+total_train)*100:.1f}% test, {total_train/(total_test+total_train)*100:.1f}% train")

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    perform_single_loso_ck_plus(base_dir, output_dir)