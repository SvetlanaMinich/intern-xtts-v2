import os

# Define the folder path and the string to replace
folder_path = 'C:/intern/xtts-2/TTS/'
old_string = 'TTS.Trainer.TTS.Trainer.trainer.'
new_string = 'TTS.Trainer.trainer.'

# Loop through each file in the folder
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)

            # Open and read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = f.read()

            # Replace the old string with the new one
            new_data = file_data.replace(old_string, new_string)

            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_data)

print("Replacement completed.")
