import os

def rename_files_in_sequence(folder_path, prefix="file"):
    try:
        # List all files in the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Sort files for consistency
        files.sort()

        # Loop through the files and rename them
        for index, file in enumerate(files, start=1):
            old_path = os.path.join(folder_path, file)
            file_extension = os.path.splitext(file)[1]  # Get file extension
            new_name = f"{prefix}{index}{file_extension}"
            new_path = os.path.join(folder_path, new_name)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {file} -> {new_name}")

        print("All files have been renamed successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
folder_path = "data/train/labels"  # Replace with the folder path
rename_files_in_sequence(folder_path)
