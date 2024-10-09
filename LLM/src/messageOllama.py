import subprocess
import random


def send_message_to_ollama(message):
    process = subprocess.Popen(
        ["docker", "exec", "-i", "ollama", "ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # This will handle strings instead of bytes
    )

    output, error = process.communicate(
        input=f'Optimise these descriptions and format them with markdown. Do not includeany headers like "Here is the optimised product description:" or "Optimised Product Description"\n\n{message}')

    if error:
        print(f"Error: {error}")
    return output


def get_random_description(df):
    row_number = random.randint(0, len(df) - 1)
    return df.iloc[row_number].about_product
