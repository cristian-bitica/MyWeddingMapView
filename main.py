import pandas as pd
import sqlite3
from src.map_generator import MapGenerator

# === INPUT PARAMETERS ===
db_path = '/Users/cristian.bitica/Repositories/PythonProjects/DjangoNuptialWedding/nuptial_wedding/db.sqlite3'
output = '/Users/cristian.bitica/Repositories/PythonProjects/DjangoNuptialWedding/nuptial_wedding/templates/wedding_map.html'
wedding_id = 1
cols = ['name', 'latitude', 'longitude', 'timestamp']


# === VARIABLES ===
query = f"""
    SELECT {', '.join(cols)}
    FROM home_location hl 
    LEFT JOIN home_wedding hw
    ON hw.townhall_id = hl.id OR hw.church_id = hl.id OR hw.restaurant_id = hl.id
    WHERE hw.id = {wedding_id}
    """
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(query)
result = cursor.fetchall()

df = pd.DataFrame(
    columns=cols,
    data=result
    )

map = MapGenerator(input_df=df)

with open(output, 'w') as out:
    out.write(map.make_map(full_html=True))
    out.close()