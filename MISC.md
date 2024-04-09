# MISC

![image](https://hackmd.io/_uploads/rJTzTd-Pp.png)

## Prog1: Max

![image](https://hackmd.io/_uploads/r1Gxw5fwa.png)



```python
#!/usr/bin/python3.7
from pwn import *

# Kết nối tới máy chủ
io = remote('103.162.14.116', 14002)
def find_maximum_value(arr):
    if not arr:
        return None  # Trả về None nếu mảng rỗng

    max_value = arr[0]  # Gán giá trị đầu tiên làm giá trị lớn nhất ban đầu

    for num in arr:
        if num > max_value:
            max_value = num  # Nếu phần tử hiện tại lớn hơn giá trị lớn nhất, cập nhật giá trị lớn nhất

    return max_value
while (1):
    io.recvuntil(b'arr = ')
    arr = io.recvline()
    arr = arr.decode('utf8')
    arr = arr.replace('[', '').replace(']', '')
    arr = arr.split(', ')
    list_num = [int(num) for num in arr]
    max_value = find_maximum_value(list_num)
    io.sendline(str(max_value).encode())

io.interactive()
```
![image](https://hackmd.io/_uploads/BkWABczPa.png)
## Prog2: True Parenthses

![image](https://hackmd.io/_uploads/HkTAD9fwT.png)



```python
#!/usr/bin/python3.7
from pwn import *

# Địa chỉ IP và cổng của máy chủ
host = '103.162.14.116'
port = 14003
# Kết nối tới máy chủ
io = remote(host, port)

# Hàm xử lý yêu cầu
def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            # Ignoring non-bracket characters
            pass

    return not stack

for i in range(1, 101):
    io.recvuntil(f'ROUND {i}: ')
    data = io.recvline()
    data = data.decode('utf-8')
    if (is_valid_parentheses(data)):
        io.sendline('yes')
    else:
        io.sendline('no')

io.interactive()
```
![image](https://hackmd.io/_uploads/rkRyKcfDa.png)

## Prog3: nth Num

![image](https://hackmd.io/_uploads/S1LBccfP6.png)

```python
#!/usr/bin/python3
from pwn import *

# Kết nối tới máy chủ
io = remote('103.162.14.116', 14004)

# Hàm xử lý yêu cầu
def find_nth_digit(n):
    # Bắt đầu với một số có một chữ số
    num_digits = 1
    start = 1

    while True:
        # Tính số lượng chữ số của nhóm hiện tại
        group_size = 9 * num_digits * 10 ** (num_digits - 1)

        # Kiểm tra xem n có nằm trong nhóm hiện tại hay không
        if n <= group_size:
            # Tính toán số cần tìm trong nhóm
            num_in_group = start + (n - 1) // num_digits

            # Tìm chữ số cụ thể trong số
            digit_position = (n - 1) % num_digits
            result_digit = int(str(num_in_group)[digit_position])

            return result_digit
        else:
            # Nếu không nằm trong nhóm hiện tại, giảm n và tăng số chữ số
            n -= group_size
            num_digits += 1
            start *= 10
i = 1
while (1):
    if (i == 1):
        io.sendlineafter(b'>> ',b'1')
        i = i + 1
    i = i + 1
    io.recvuntil(b'n = ')
    value = io.recvline()
    value = int(value.decode('utf-8'))
    result = find_nth_digit(value)
    io.sendline(str(result).encode())
    

# Đóng kết nối khi không cần sử dụng nữa
io.interactive()
```

![image](https://hackmd.io/_uploads/r1UXiqfPa.png)

## Prog4: Requiem

![image](https://hackmd.io/_uploads/HkoPs5Mv6.png)

```python
#!/usr/bin/python3.7
from pwn import *

# Kết nối tới máy chủ
io = remote('103.162.14.116', 14005)

def recursive_sequence(n):
    if n == 0:
        return 1
    elif n % 2 == 0:
        return n * recursive_sequence(n - 1)
    else:
        return n + recursive_sequence(n - 1)

while (1):
    io.recvuntil(b'n = ')
    data = io.recvline()            
    print ('data1: ',data)
    data = int(data.decode('utf-8').strip())
    # In dữ liệu nhận được
    print("Received data:", data)
    value = recursive_sequence(data)
    value = str(value).encode()
    print(value)
    io.sendline(value)

# Đóng kết nối khi không cần sử dụng nữa
io.interactive()

```    
![image](https://hackmd.io/_uploads/B113icMv6.png)


## dumbkernel_jail

Trong hàm cat thì điều quan tâm nhất là input chúng ta cần có các kí tự '+', '-'... ở đoạn if any(...).
Nếu có thì hàm sẽ thực thi eval(file_name), 

- eval() python injection. 

https://vk9-sec.com/exploiting-python-eval-code-injection/

Bước thử payload thì mình nghĩ là nên dùng dấu ```+``` cho input để thoả mã điều kiện.
Sau khi mò payload thì mình đã lấy được flag

![image](https://hackmd.io/_uploads/BkizK6Mva.png)
