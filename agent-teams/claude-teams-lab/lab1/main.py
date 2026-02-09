from utils import calculate_total, format_output
from config import settings

def process_data(items):
    total = calculate_total(items)
    return format_output(total, settings['currency'])

if __name__ == "__main__":
    data = [100, 200, 300]
    result = process_data(data)
    print(result)