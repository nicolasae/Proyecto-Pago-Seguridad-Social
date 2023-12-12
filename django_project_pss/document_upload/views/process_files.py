import os

def create_folder_if_not_exists(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        try:
            # Create the folder if it doesn't exist
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        except OSError as e:
            print(f"Error: Failed to create folder '{folder_path}'. Reason: {e}")
    else:
        print(f"Folder '{folder_path}' already exists.")

def save_uploaded_file(uploaded_file, path):
    # Open the destination file in binary write mode.
    with open(path, 'wb') as destination:
        # Iterate through the chunks of the uploaded file and write them to the destination file.
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return path
