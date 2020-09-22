import requests
import csv

if __name__ == "__main__":
    print("Start API Test!")
    url = "http://127.0.0.1:8000/api/"
    with open('test_codes.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            try:
                code = "".join(line)
                params = {'code': code}
                res = requests.get(url, params=params)
                assert(res.status_code == 200)
            except AssertionError:
                print("API test failed ...")
                exit()
    print("API test finished")
