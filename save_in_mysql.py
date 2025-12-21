import pandas as pd
from sqlalchemy import create_engine

# Load cleaned CSV
df = pd.read_csv("C:/Users/VARSHA/Documents/Python/py_venv/eq_clean.csv")

# Create MySQL connection
engine = create_engine("mysql+pymysql://root:Vinvj%405050@localhost/earthquake_db")

# Save DataFrame to MySQL
df.to_sql("earthquakes", con=engine, if_exists="append", index=False)

print("Data successfully saved to MySQL!")
