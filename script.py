import requests
import concurrent.futures


BOOKING_URL = 'http://127.0.0.1:8000/api/book/'
# ID of the train that should have only one available seat
TRAIN_NO = 12456

# Replace these with your actual user tokens from the login endpoint
TOKEN_USER_1 = '70e6ab60288157eb2e23dc76ef1eec2ef007e715'
TOKEN_USER_2 = 'b7f8a69b8019399273e47dfdbb04a910ca19bd68'

def attempt_booking(token):
    """
    Attempts to book a seat for the given user token.
    """
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    payload = {'train_no': TRAIN_NO}
    response = requests.post(BOOKING_URL, json=payload, headers=headers)
    try :
        return response.status_code, response.json()
    except Exception as e:
        print(f'some exception error occure {e}')
        print(f'respone {response.__dict__}')
        return  response.status_code, "response"

def main():
    # Use a ThreadPoolExecutor to simulate two requests happening concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(attempt_booking, TOKEN_USER_1),
            executor.submit(attempt_booking, TOKEN_USER_2)
        ]
        # Print the results as they complete
        for future in concurrent.futures.as_completed(futures):
            status_code, response_data = future.result()
            print(f"Status Code: {status_code}, Response: {response_data}")

if __name__ == '__main__':
    main()
