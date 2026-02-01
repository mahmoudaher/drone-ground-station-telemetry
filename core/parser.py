import json

def parse_line(line: str):
    try:
        data = json.loads(line)
        return data
    except json.JSONDecodeError:
        print("Bad JSON:", line)
        return None
