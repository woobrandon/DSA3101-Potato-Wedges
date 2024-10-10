import random


def get_random_description(df):
    row_number = random.randint(0, len(df) - 1)
    return df.iloc[row_number].about_product
