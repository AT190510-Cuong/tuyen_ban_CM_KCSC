# Nguyễn Hùng Cường-AT190510-MB 
# TTV KCSC (16/12/2023-17/12/2023)
## Warmup
mình vào discord lấy flag

## web
### -Pokemon Hof Panel Level 1

đầu tiên mình bật intercept trên burp suit rồi vào web và chọn như bình thường và submit
![image](https://hackmd.io/_uploads/Byd1VJ3I6.png)

kết quả hiển thị là : mình không phải champion
![image](https://hackmd.io/_uploads/HJfFEynL6.png)

và gói tin mình chặn là:
![image](https://hackmd.io/_uploads/Hy4S8knUa.png)
ở đây có trường cookie mình đem ra decode để xem giá trị
![image](https://hackmd.io/_uploads/SygTL12IT.png)
lần lượt là url và base64
![image](https://hackmd.io/_uploads/SyT1wyn8a.png)

thấy trường isChampion có kiểu boolean và giá trị 0 nên mình chuyển lại thành 1 và encode 
![image](https://hackmd.io/_uploads/S1RZ_J28T.png)
rồi mình gửi lại gói tin đã sửa `Cookie: trainer_data` ở Repeater

và được flag
![image](https://hackmd.io/_uploads/SJDu_1n8T.png)

### -Mi Tom Thanh Long

mình đi xung quanh trang web thì không nhận được gì ngoài **"lần đầu tiên trái thanh long có trong mì tôm"**

có trường để nhập vào nhưng không send được:
![image](https://hackmd.io/_uploads/rJ9z913La.png)

mình nghĩ đây chỉ là phần fontend và không có manh mối gì nên thử dùng dirsearch để quét xem có thư mục hay tệp nào ẩn mà trang web không muốn hiện ra không 
`dirsearch -u http://103.162.14.116:10002/`
và tìm được file flag :+1: 
![image](https://hackmd.io/_uploads/r1iyj1h8T.png)

mình chuyển hướng đến đọc file này và được flag
![image](https://hackmd.io/_uploads/HkD4oy286.png)

### -Apply To KCSC


mình up 1 file thường lên và success
![image](https://hackmd.io/_uploads/B1zrlx2U6.png)

mình kiểm tra trang web thì thấy viết bằng php
![image](https://hackmd.io/_uploads/S1ZsZxhU6.png)


sau đó mình vào Burp Suite và send package vừa gửi sang repeater rồi thay đổi file phần mở rộng của file là `shell.php` và tạo nội dung bên trong một web shell là:

**<?php echo exec('whoami > /images/output.txt'); ?>**

sau đó mình gửi và vẫn thành công
gửi được rồi vậy đọc thì thế nào đây?
mình thử tìm file ảnh có logo của clb KCSC rồi thay đổi đường dẫn đến file mình vừa tạo **/images/output.txt**  nhưng không đọc được kết quả gì
sau một hồi mình thử shell khác cho phép tương tác trên url
**<?php system($_GET['cmd']); ?>** để tạo parameter **cmd** cho mình tương tác với hệ thống qua hàm system
sau đó mình gửi và vẫn thành công


![image](https://hackmd.io/_uploads/ryKfMxnI6.png)
và mình thử dùng dirsearch để tìm ra thư mục ẩn được thưu mục uploads:


![image](https://hackmd.io/_uploads/Hye04x3L6.png)

và mình lên đường link url thực hiện khai thác vào hệ thống
![image](https://hackmd.io/_uploads/S1az8x386.png)
mình vào từng thư mục cha của thư mục mình đang đứng ![image](https://hackmd.io/_uploads/ryoTLghIp.png)

và được flag  ![image](https://hackmd.io/_uploads/SJPVPg3U6.png)

![image](https://hackmd.io/_uploads/rJGbwx3Ua.png)



## PWN
### -A gift for pwners
mình dùng IDA để reverse và đi tìm xung quanh các hàm rồi nhận được flag
![image](https://hackmd.io/_uploads/BytxyN2Ip.png)
part1: KCSC{A_gift_
![image](https://hackmd.io/_uploads/BkXfk42La.png)
part2: for_the_
sau đó mình dùng lệnh `strings gift` để đọc được các đoạn text của chương trình và được part3
![image](https://hackmd.io/_uploads/r10ylV3Ip.png)
part3: pwners_0xdeadbeef}


### -strstr 
mình vào IDA để reverse
![image](https://hackmd.io/_uploads/HJD-ol3Ua.png)
mình thấy buf khai báo 48 byte mà hàm read lại cho nhập đến 0x40(64 byte) nên ở đây có lỗi buffer overflow
mình thấy đã có sẵn hàm win có chứa shell
![image](https://hackmd.io/_uploads/rkuw0gnI6.png)
nên mục tiêu của mình là ghi đè địa chỉ của win vào save rip trên stack để thực thi hàm này khi chương trình kết thúc 
![image](https://hackmd.io/_uploads/r1Dbs4nLp.png)
và mình debug động gặp lỗi xmm0
![image](https://hackmd.io/_uploads/HJZ69Vh8p.png)

do ở đây địa chỉ stack không chia hết cho 16 
![image](https://hackmd.io/_uploads/HyRoi42Ip.png)
nên mình nhảy vào vị trí `win + 1` và mình đã nhận được flag
![image](https://hackmd.io/_uploads/rJNTAJ28p.png)

### -linux command
![image](https://hackmd.io/_uploads/H1NKsmnI6.png)
mình có part1: KCSC{Linux_
mình dùng IDA để reverse và được 
![image](https://hackmd.io/_uploads/HyMOD-3Ua.png)
thấy có hàm system thực thi biến command ngay đầu vào của mình nhập và nó sẽ chép 22 byte đầu vậy từ 23 đến 32 byte sau thì sao?
![image](https://hackmd.io/_uploads/HyDM4-3Lp.png)

mình đã tận dụng mấy byte cuối bị thừa này đề thực thi shell
![image](https://hackmd.io/_uploads/rk7Ep7hLT.png)
ban đầu mình dùng ls và ra được các file và mình nghĩ đã có shell để thực thi rồi và cat các file nhưng không được vì có vẻ như bị chặn khoảng trắng và mình cố gắng tìm những lệnh linux để đọc file mà không cần  khoảng trắng. Nhưng đã quá muộn để nhận ra mình chỉ cần thêm /bin/sh và làm bất cứ điều gì mình muốn   
![image](https://hackmd.io/_uploads/SyxSM-3Up.png)
mình được part2: Commands_

![image](https://hackmd.io/_uploads/r1LvMZh8a.png)

mình được part3: You_MUST_Know_

![image](https://hackmd.io/_uploads/rybjG-38T.png)
mình được part4: bc6680c1a0d13d77_

![image](https://hackmd.io/_uploads/SkofQbnIa.png)

mình được part5: 8d73c59185b1e412}
![image](https://hackmd.io/_uploads/ry__m-2I6.png)

ghép lại được flag là **KCSC{Linux_Commands_You_MUST_Know_bc6680c1a0d13d77_8d73c59185b1e412}**

## RE
### -Real Warmup

mình dùng Ghidra và vào hàm main được:
![image](https://hackmd.io/_uploads/By9h1W2LT.png)


mình thấy chỉ khi biến local_108=**local_108,S0NTQ3tDaDQwYF9NfF98bjlgX0QzTidfVjAxJ183N1wvX0tDU0N9** thì chương trình mới thoát ra và in Great!!! có vẻ đó chính là flag
![image](https://hackmd.io/_uploads/rypkg-3LT.png)

mình lên Cyberchef giải mã đoạn trên và được flag: 
![image](https://hackmd.io/_uploads/rJj0lZ28p.png)





### -hide and seek

tìm loại file với lệnh file trên linux mình thấy đây là file PE32 của window
chạy file mình được 

![image](https://hackmd.io/_uploads/SkPPtgnUp.png)

trong dòng màu blue mình copy và paste ra được 1 đường dẫn thư mục chỉ đến thư mục rác của máy
**C:\Users\HP\AppData\Local\Temp**

![image](https://hackmd.io/_uploads/S1u7YgnUT.png)
chạy file này và mình được flag
![image](https://hackmd.io/_uploads/r1gMKl3IT.png)

## crypto

bài này dùng  mật mã caesar sẽ dịch chuyển các chữ cái so với ban đầu độ dài là key vì mình cần biết key để dịch lại nhưng chúng ta cũng có thể brute force để tìm ra flag
![image](https://hackmd.io/_uploads/SJsMT42I6.png)


![image](https://hackmd.io/_uploads/S13yTNnIp.png)


## Sister Location
mình làm bài này đầu tiên và mất rất nhiều thời gian vẫn không ra 
bài cho mình 1 file pdf có pass và 1 hình ảnh
![image](https://hackmd.io/_uploads/r14X1B3IT.png)

mình dùng john the rip thử crack mật khẩu file pdf nhưng không được

tiếp theo phân tích hình ảnh thấy có dòng chữ mờ góc trên bên trái 
![image](https://hackmd.io/_uploads/rJ6uJrh8p.png)
nên mình nghĩ có thể là stegano che dấu điều gì trong bức ảnh này nên mình dùng stegsolve ra 
![image](https://hackmd.io/_uploads/B1IQeHnIp.png)
red coordinates
![image](https://hackmd.io/_uploads/H11LeS386.png)
green coordinates
![image](https://hackmd.io/_uploads/BkwDeHhIp.png)
blue coordinates
![image](https://hackmd.io/_uploads/rkcueS38p.png)

ALPHA COORDINATES:
(1664:413)
(38:535)
(1173:683)
(1564:1075)
(983:113)
(196:430)

RED COORDINATES:
(523:731)
(751:127)
(1890:261)
(1776:279)

GREEN COORDINATES:
(352:91)
(241:777)
(1876:690)
(882:889)
(1815:144)
(177:625)
(1850:884)
(389:178)

BLUE COORDINATES:
(1267 :765)
(1849:78)
(1452:100)

mình thử biểu diễn ra tọa độ nhưng không được 
![image](https://hackmd.io/_uploads/S14nmrh86.png)
sang dạng nhị phân cũng không được 
![image](https://hackmd.io/_uploads/S1kxNr3LT.png)
và thử sang bit xem có ghép được thành chữ gì không

![image](https://hackmd.io/_uploads/BJ_rVS2UT.png)
và cũng không ra được gì
