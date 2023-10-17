import os
import shutil
import random

# Paths
ORIGINAL_DATASET_DIR = "dataset"
NEW_BASE_DIR = "dataset_split"

TRAIN_DIR = os.path.join(NEW_BASE_DIR, "train")
VALIDATION_DIR = os.path.join(NEW_BASE_DIR, "validation")

# Creating new directories for train and validation
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VALIDATION_DIR, exist_ok=True)

# Ratios
TRAIN_RATIO = 0.8  # 80% of data used for training
VALIDATION_RATIO = 0.2  # 20% of data used for validation

# List of categories
categories = ["cats", "dogs"]

# Splitting data into training and validation sets
for cat in categories:
    os.makedirs(os.path.join(TRAIN_DIR, cat), exist_ok=True)
    os.makedirs(os.path.join(VALIDATION_DIR, cat), exist_ok=True)

    # Listing all files in the category
    all_files = os.listdir(os.path.join(ORIGINAL_DATASET_DIR, cat))
    all_files = [
        f
        for f in all_files
        if os.path.isfile(os.path.join(ORIGINAL_DATASET_DIR, cat, f))
    ]

    # Shuffling to randomize data
    random.shuffle(all_files)

    # Splitting files
    train_files = all_files[: int(len(all_files) * TRAIN_RATIO)]
    validation_files = all_files[int(len(all_files) * TRAIN_RATIO) :]

    # Copying files into new directory structure
    for file in train_files:
        shutil.copy(
            os.path.join(ORIGINAL_DATASET_DIR, cat, file),
            os.path.join(TRAIN_DIR, cat, file),
        )
    for file in validation_files:
        shutil.copy(
            os.path.join(ORIGINAL_DATASET_DIR, cat, file),
            os.path.join(VALIDATION_DIR, cat, file),
        )
