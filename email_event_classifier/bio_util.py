import os

def save_bio_to_file(tokens, labels, bio_file):
    """
    Save tokens and labels in BIO format to a .bio file.
    Creates the file if it doesn't exist, appends to it if it exists.
    """
    if len(tokens) != len(labels):
        raise ValueError("Tokens and labels must have the same length.")

    file_exists = os.path.isfile(bio_file)

    with open(bio_file, mode='a', encoding='utf-8') as file:
        if not file_exists:
            print(f"Creating new BIO file: {bio_file}")
        else:
            print(f"Appending to existing BIO file: {bio_file}")

        for token, label in zip(tokens, labels):
            file.write(f"{token}\t{label}\n")
        file.write("\n")  # Add a blank line to separate sentences
    print(f"BIO data saved to {bio_file}")