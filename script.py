items = [
    ("ahmed","12", "06xxxx"),
    ("noor","18", "07xxxx"),
    ]


for item in items:
    print("new: row")
    for col_id, col_info in enumerate(item):
        print(f"col_id {col_id}, col_info {col_info}")
    