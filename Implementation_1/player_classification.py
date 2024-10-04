import cv2
import numpy as np
from skimage.feature import hog
from sklearn.cluster import KMeans
import os

# LAB segmentation thresholds (still used for initial segmentation, but updated with additional thresholding)
lower_lab = np.array([0, 115, 115])  # Lower the minimum for a broader range
upper_lab = np.array([255, 200, 200])  # Raise the maximum for a broader range

# Feature extraction functions remain the same
def extract_color_histogram(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    hist_l = cv2.calcHist([lab], [0], None, [256], [0, 256])
    hist_a = cv2.calcHist([lab], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([lab], [2], None, [256], [0, 256])
    hist_l = cv2.normalize(hist_l, hist_l).flatten()
    hist_a = cv2.normalize(hist_a, hist_a).flatten()
    hist_b = cv2.normalize(hist_b, hist_b).flatten()
    return np.hstack([hist_l, hist_a, hist_b])

def extract_hog_features(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, (128, 128))
    hog_features, _ = hog(resized_image, orientations=9, pixels_per_cell=(8, 8),
                          cells_per_block=(2, 2), visualize=True)
    return hog_features

# Function to process and segment players with added adaptive and Otsu's thresholding
def segment_and_process_images(folder):
    feature_list = []
    image_files = os.listdir(folder)

    for image_file in image_files:
        image_path = os.path.join(folder, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Warning: Could not read image {image_file}")
            continue

        # Convert image to LAB color space for initial segmentation
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        mask_lab = cv2.inRange(lab_image, lower_lab, upper_lab)

        # Convert image to grayscale for further thresholding
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Otsu's thresholding to get a binary mask
        _, mask_otsu = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply Adaptive Thresholding to get a more localized mask
        mask_adaptive = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 11, 2)

        # Combine masks in a less restrictive way
        # Instead of AND, we will use OR to allow for more pixels to be included in the mask
        combined_mask = cv2.bitwise_or(mask_lab, mask_otsu)
        combined_mask = cv2.bitwise_or(combined_mask, mask_adaptive)

        # Apply morphological operations for further refinement
        kernel = np.ones((5, 5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)

        # Segment player from background using the final combined mask
        result = cv2.bitwise_and(image, image, mask=combined_mask)

        # Check if the result is mostly black (i.e., no player was segmented)
        non_black_pixels = cv2.countNonZero(cv2.cvtColor(result, cv2.COLOR_BGR2GRAY))
        if non_black_pixels < 1000:  # Arbitrary threshold to check if segmentation is effective
            print(f"Warning: Insufficient segmentation for {image_file}")
            continue

        # Extract features (color histograms + HOG)
        color_features = extract_color_histogram(result)
        hog_features = extract_hog_features(result)
        combined_features = np.hstack([color_features, hog_features])
        feature_list.append(combined_features)

        # Save the processed segmented images
        processed_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(processed_image_path, result)

    return np.array(feature_list), image_files

# Perform clustering (same as before)
def perform_clustering(features, k=4):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features)
    return kmeans.labels_

# Create output directories (same as before)
output_folder = '/Users/kshitijchaturvedi/Downloads/Implementation_1/output'
os.makedirs(output_folder, exist_ok=True)
for i in range(4):
    os.makedirs(os.path.join(output_folder, f'player{i}'), exist_ok=True)

# Directories (adjust paths)
top_folder = '/Users/kshitijchaturvedi/Downloads/Level1_screening/two_players_top'
bot_folder = '/Users/kshitijchaturvedi/Downloads/Level1_screening/two_players_bot'

# Process images and extract features from both folders
top_features, top_images = segment_and_process_images(top_folder)
bot_features, bot_images = segment_and_process_images(bot_folder)

# Combine features and images for clustering
combined_features = np.vstack((top_features, bot_features))
combined_images = top_images + bot_images

# Perform k-means clustering for all players
combined_labels = perform_clustering(combined_features, k=4)

# Classify players based on clustering results (same as before)
def assign_player_classes(cluster_labels, image_files):
    class_mapping = {}
    for label in np.unique(cluster_labels):
        indices = np.where(cluster_labels == label)[0]
        for index in indices:
            if label not in class_mapping:
                class_mapping[label] = []
            class_mapping[label].append(image_files[index])
    return class_mapping

# Classify players across both folders
player_classification = assign_player_classes(combined_labels, combined_images)

# Save images to corresponding player subfolders (same as before)
for player_class, images in player_classification.items():
    for image_name in images:
        original_folder = top_folder if image_name in top_images else bot_folder
        original_image_path = os.path.join(original_folder, image_name)
        player_output_path = os.path.join(output_folder, f'player{player_class}', image_name)
        image = cv2.imread(original_image_path)
        cv2.imwrite(player_output_path, image)

# Print classification results
print("Player Classification:")
for player_class, images in player_classification.items():
    print(f"Class {player_class}: {images}")
