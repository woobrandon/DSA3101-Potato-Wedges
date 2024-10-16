import sqlite3
import numpy as np

def get_features(id):
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT features FROM features WHERE id=?', (id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        features_blob = result[0]
        features = np.frombuffer(features_blob, dtype=np.float32)
        return features
    else:
        return None
