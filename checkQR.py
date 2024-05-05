import json
import main

def check_qr():
    with open('instance/check.txt', 'r') as f:
        id = f.read()
    if id != '':
        try:
            decoded_data = json.loads(id)
            abn_id = (decoded_data['subscription_number'])
            return abn_id
        except:
            f.close()
            clear()
            return None


def clear():
    with open('instance/check.txt', 'w') as f:
        f.write('')