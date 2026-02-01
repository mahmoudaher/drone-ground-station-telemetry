import csv
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

filename = datetime.now().strftime("logs/session_%Y%m%d_%H%M%S.csv")

file = open(filename, "w", newline="")
writer = csv.writer(file)

writer.writerow(["ts", "src", "ch", "name", "unit", "val"])

def log_row(d):
    writer.writerow([
        d["ts"],
        d["src"],
        d["ch"],
        d["name"],
        d["unit"],
        d["val"],
    ])
    file.flush()
