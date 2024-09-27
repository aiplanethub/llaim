def load_text_file(file_path):
    with open(file_path, 'r') as file:
        text_data = file.read()
        print(text_data)