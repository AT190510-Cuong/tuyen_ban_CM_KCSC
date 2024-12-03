# Cài đặt môi trường debug deserialize
## Tải nhiều jdk trên kali linux

### tải file JDK 8u131

- https://planetone.online/downloads/java/jdk/


![image](https://hackmd.io/_uploads/rka92ZOXJx.png)


![image](https://hackmd.io/_uploads/rJdPhZOXye.png)
### 2. Cài đặt JDK 8u131
Sau khi tải xong, thực hiện các bước sau để cài đặt:

- Bước 2.1: Di chuyển tệp tải về
Giả sử tệp được tải về thư mục ~/Downloads, di chuyển tệp đến thư mục /opt:

```bash
Sao chép mã
sudo mv ~/Downloads/jdk-8u131-linux-x64.tar.gz /opt
```

- Bước 2.2: Giải nén tệp
Giải nén tệp JDK:

```bash
Sao chép mã
cd /opt
sudo tar -xvzf jdk-8u131-linux-x64.tar.gz
```


Thư mục jdk1.8.0_131 sẽ được tạo trong /opt.

### 3. Cấu hình JDK
Cập nhật biến môi trường để sử dụng JDK vừa cài.

- Bước 3.1: Cấu hình JAVA_HOME và PATH
Mở tệp ~/.bashrc:

```bash
Sao chép mã
nano ~/.bashrc
```

Thêm các dòng sau vào cuối tệp:

```bash
Sao chép mã
export JAVA_HOME=/opt/jdk1.8.0_131
export PATH=$JAVA_HOME/bin:$PATH
```


Lưu và tải lại tệp cấu hình:

```bash
Sao chép mã
source ~/.bashrc
Bước 3.2: Kiểm tra phiên bản Java
```

Kiểm tra xem JDK 8u131 đã được cài đặt thành công hay chưa:

```bash
Sao chép mã
java -version
```


Kết quả mong đợi:


```
java version "1.8.0_131"
Java(TM) SE Runtime Environment (build 1.8.0_131-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.131-b11, mixed mode)

```
### 4. Cấu hình thay đổi với update-alternatives (tùy chọn)
Nếu bạn muốn quản lý nhiều phiên bản Java cùng lúc, bạn có thể sử dụng update-alternatives:

Thêm JDK 8u131 vào danh sách:
```bash
Sao chép mã
sudo update-alternatives --install /usr/bin/java java /opt/jdk1.8.0_131/bin/java 1
sudo update-alternatives --install /usr/bin/javac javac /opt/jdk1.8.0_131/bin/javac 1
```


Chọn phiên bản mặc định:
```bash
Sao chép mã
sudo update-alternatives --config java
sudo update-alternatives --config javac
```

![image](https://hackmd.io/_uploads/Hkw8Ae2mke.png)



## Tải intelij trên kali linux 

```bash
wget https://download.jetbrains.com/idea/ideaIC-2022.3.tar.gz
## Sau khi tải xong, giải nén tệp:
tar -xvzf ideaIC-2022.3.tar.gz
## Di chuyển thư mục đã giải nén đến /opt để dễ quản lý:
sudo mv idea-IC-223.* /opt/intellij-idea
## Tạo một liên kết để có thể khởi chạy IntelliJ IDEA từ terminal:
sudo ln -s /opt/intellij-idea/bin/idea.sh /usr/local/bin/idea
## Chạy IntelliJ IDEA bằng lệnh:
idea
```

## tải source code để debug trên intelij

- ```File > Settings```


![image](https://hackmd.io/_uploads/S13KYes7kx.png)

- cửa sổ sua sẽ xuất hiện 


![image](https://hackmd.io/_uploads/HJS2KeiXye.png)

- chọn ```Build, Execution, Deployment > Build Tools > Maven > Import```
- ở phần Automatically download chọn ```Source, documentation, Annotations```
- chọn ```Apply > OK```


## debug 
![image](https://hackmd.io/_uploads/Byxgvx3QJx.png)

- ```Project File```: là cửa sổ show ra các source file java, khi chạy các file java trong IntellIJ sẽ lấy working directory tại đây luôn.
- ```Project ‘s Library```: hiển thị các library có trong classpath của project
- ```Stack Trace```: cửa sổ này hiển thị ra backtrace, hay còn được hiểu là show ra các method đã gọi tới method hiện tại.
- ```Local Variable```: đây là một điểm mạnh mà mình rất thích ở IntellIJ. Khi debug, IntellIJ sẽ cố gắng lấy hết giá trị các biến để show ra cửa sổ này, giúp cho việc debug được dễ dàng hơn, nhưng đôi khi nó lại gây ra những sai sót và hiểu lầm cho người dùng


## tài liệu tham khảo ysorial

- Commons-Collections1 : https://hackmd.io/@vanirxxx-java/BJYmd7hms

- Commons-Collections2 : https://hackmd.io/@vanirxxx-java/r1Oe0W7Ei?utm_source=preview-mode&utm_medium=rec

