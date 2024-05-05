import json


data_str = ' {"name": "\u0420\u0443\u0441\u043b\u0430\u043d ", "phone_number": "8-800-555-35-35", "date_signing": "01.05.2024", "activate_date": "02.05.2024-02.06.24", "freezing": "10.0", "subscription_number": "1623"} '


decoded_data = json.loads(data_str)

print(decoded_data)
