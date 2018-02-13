import os


def load_text_data(file_path):
    """ Load data-set  """
    input_file = os.path.join(file_path)
    with open(input_file, "r") as f:
        data = f.read()

    return data.split("\n")