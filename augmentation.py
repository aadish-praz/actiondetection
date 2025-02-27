# import cv2
# import os
# import numpy as np
# def mirror_images_in_folder(input_folder, direction='horizontal'):
#     # Get the name of the input folder
#     input_folder_name = os.path.basename(input_folder)


#     c=int(input_folder_name )+50
#     # Create the output folder in the same location as the input folder
#     output_folder = os.path.join(os.path.dirname(input_folder), f'{c}')
    
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Get a list of all image files in the input folder
#     image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

#     # Mirror each image in the input folder
#     for image_file in image_files:
#         # Build the input and output paths
#         input_path = os.path.join(input_folder, image_file)
#         output_path = os.path.join(output_folder, f'{image_file}')

#         # Read the image
#         image = cv2.imread(input_path)

#         # Mirror the image horizontally or vertically
#         if direction == 'horizontal':
#             mirrored_image = cv2.flip(image, 1)
#         elif direction == 'vertical':
#             mirrored_image = cv2.flip(image, 0)
#         else:
#             print("Invalid direction. Please use 'horizontal' or 'vertical'.")
#             return

#         # Save the mirrored image
#         cv2.imwrite(output_path, mirrored_image)
#         print(f"Mirrored image saved to {output_path}")

# # Example usage: Mirror all images in the input folder horizontally and save in a new folder


# def extract_folder_paths(base_folder):
#     folder_paths = []
    
#     # Walk through the directory and get all folder paths
#     for folder_name, _, _ in os.walk(base_folder):
#         folder_paths.append(folder_name)
    
#     return folder_paths

# # Example usage: Extract all folder paths in a given folder
# base_folder = r'D:\Data collection\Frame_Collection\Nice To Meet You'

# all_folders = extract_folder_paths(base_folder)
# c=50
# # Print the extracted folder paths
# for folder_path in all_folders:
#     input_folder_name = os.path.basename(folder_path)
#     if input_folder_name.isdigit():
#         print(input_folder_name)
#         mirror_images_in_folder(folder_path, direction='horizontal')







# actions = np.array(['Aausadi', 'Ambulance', 'Bathroom', 'Be Careful', 'Bleeding', 'Call', 'Dhanebad', 'Doctor', 'dont understand',
#                     'eklopan', 'Emergency', 'firstaid', 'Good Morning', 'Happy', 'Heart_attack', 'hello', 'Help', 'Hospital', 'Name',
#                     'need', 'nice to meet you', 'oxygen', 'pain', 'Please', 'Police', 'Relax', 'sign', 'Slowly', 'sorry', 'What', 'yes', 'You'])

# # Example usage: Extract all folder paths in a given folder
# base_folder = r'D:\Data collection\Frame_Collection\actions'  # Define the base folder path outside the loop

# for action in actions:
#     folder_path = os.path.join(base_folder, action)
#     print(folder_path)  # Print the folder path for each action


import os
import numpy as np

def mirror_arrays_in_folder(input_folder, direction='horizontal'):
    # Get the name of the input folder
    input_folder_name = os.path.basename(input_folder)

    c = int(input_folder_name) + 50
    # Create the output folder in the same location as the input folder
    output_folder = os.path.join(os.path.dirname(input_folder), str(c))
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all .npy files in the input folder
    npy_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.npy')]

    # Mirror each .npy file in the input folder
    for npy_file in npy_files:
        # Build the input and output paths
        input_path = os.path.join(input_folder, npy_file)
        output_path = os.path.join(output_folder, npy_file)

        # Load the numpy array
        array = np.load(input_path)

        # Mirror the array horizontally or vertically
        if direction == 'horizontal':
            if len(array.shape) == 1:
                mirrored_array = np.flip(array)
            elif len(array.shape) == 2:
                mirrored_array = np.fliplr(array)
            else:
                print("Invalid array shape. Please use 1D or 2D arrays.")
                return
        elif direction == 'vertical':
            if len(array.shape) == 1:
                mirrored_array = np.flip(array)
            elif len(array.shape) == 2:
                mirrored_array = np.flipud(array)
            else:
                print("Invalid array shape. Please use 1D or 2D arrays.")
                return
        else:
            print("Invalid direction. Please use 'horizontal' or 'vertical'.")
            return

        # Save the mirrored array
        np.save(output_path, mirrored_array)
        print(f"Mirrored array saved to {output_path}")

def extract_folder_paths(base_folder):
    folder_paths = []
    
    # Walk through the directory and get all folder paths
    for folder_name, _, _ in os.walk(base_folder):
        folder_paths.append(folder_name)
    
    return folder_paths

# Example usage: Extract all folder paths in a given folder
base_folder = r'D:\Hand Gesture Recognition\Frame_Data\Aausadi'

all_folders = extract_folder_paths(base_folder)

# Mirror .npy files in each folder
for folder_path in all_folders:
    input_folder_name = os.path.basename(folder_path)
    if input_folder_name.isdigit():
        print(input_folder_name)
        mirror_arrays_in_folder(folder_path, direction='horizontal')
