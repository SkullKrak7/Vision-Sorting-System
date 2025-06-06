import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

def load_dataset(data_dir, img_size=(64, 64)):
    X, y = [], []
    label_map = {}

    for i, folder in enumerate(sorted(os.listdir(data_dir))):
        folder_path = os.path.join(data_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        label_map[i] = folder
        for file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, img_size)
                X.append(img)
                y.append(i)
            else:
                print(f"Warning: Could not read {img_path}")

    X = np.array(X, dtype=np.float32) / 255.0
    y = np.array(y)

    class_counts = {label_map[i]: y.tolist().count(i) for i in label_map}
    if len(label_map) < 2:
        print("Warning: Only one class found. Classification requires at least two classes.")

    for label, count in class_counts.items():
        if count < 10:
            print(f"Warning: Class '{label}' has only {count} samples. Consider adding more for better results.")

    return train_test_split(X, y, test_size=0.2, random_state=42), label_map

