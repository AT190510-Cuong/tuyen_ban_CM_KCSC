# Task 2

## JWT là gì

JSON web tokens (JWT)
Một trong những tình huống ứng dụng JWT thường gặp, đó là:

- Authentication: Tình huống thường gặp nhất, khi user logged in, mỗi request tiếp đó đều kèm theo chuỗi token JWT, cho phép người dùng có thể truy cập đường dẫn, dịch vụ và tài nguyên được phép ứng với token đó

![image](https://hackmd.io/_uploads/SJgHYDilyx.png)

- token có thể xuất hiện tại các vị trí sau trong http request

![image](https://hackmd.io/_uploads/S1v_tPolyl.png)

- token khác gì so với các kiểu xác thực khác

| Đặc điểm    | Basic                            | Session-based                                     | Token-based                                              |
| ----------- | -------------------------------- | ------------------------------------------------- | -------------------------------------------------------- |
| Dấu hiệu    | Authorization Header             | Header (cookie) / URL / Body (form)               | Header (Auth, custom) / URL / Body                       |
| Lưu Server  | Không lưu (vì chính là UserDB)   | Có lưu Session Data (memory, database, file,...)  | Không lưu (vì token chứa đủ thông tin rồi)               |
| Lưu Client  | Browser tự lưu (username + pass) | Cookie (Session ID)                               | Local storage, Cookie, session storage (browser)         |
| Cách verify | So sánh với UserDB               | Dùng Session ID để tìm data trong session storage | Kiểm tra tính toàn vẹn của token qua signature của token |
| Phù hợp cho | Hệ thống internal                | Monolithic website                                | Web API của hệ thống phân tán, đa nền tảng,...           |

## các thành phần chính của JWT

- https://www.youtube.com/watch?v=dZaFTf3iZME
- JWT là là một đối tượng JSON được định nghĩa trong RFC 7519 như một đoạn mã an toàn để trình bày một tập hợp thông tin giữa hai bên. Đoạn mã token bao gồm header, payload và signature.

![image](https://hackmd.io/_uploads/HJZzR3dgyx.png)

- thành phần Header: sẽ lưu thông tin thuật toán mã hóa và kiểu token là JWT
  - “typ” (type) chỉ ra rằng đối tượng là một JWT
  - “alg” (algorithm) xác định thuật toán mã hóa cho chuỗi là HS256
- thành phần Payload: sẽ lưu thông tin để định danh về chủ thể đang đăng nhập như UUID
- thành phần signature: sẽ là chữ ký được tạo ra từ header và payload kèm theo khóa đặc biệt qua khiểu mã hóa được đề cập trên header. Cụ thể, quá trình tạo signature trong JWT sử dụng thuật toán mã hóa hash như HMAC (Hash-based Message Authentication Code) hoặc RSA (Rivest-Shamir-Adleman) để tạo ra một chuỗi ký tự đại diện cho signature, được gắn vào cuối của JWT. Thuật toán HMAC sử dụng một khóa bí mật chung được biết đến bởi cả người tạo JWT và người xác thực JWT để tạo ra signature, trong khi thuật toán RSA sử dụng cặp khóa công khai và khóa riêng tư để thực hiện quá trình tạo signature.

## cách thức hoạt động của JWT

- JWT token sẽ lưu chính dữ liệu ở trên token mà token này do phía client nắm giữ không giống như cơ chế lưu trữ dữ liệu trên server của cookie

- khi đăng nhập vào website với credential hợp lệ server sẽ trả về cho client 1 JWT token
- và nhưng lần request sau đó client sẽ gửi kèm JWT token vừa được cấp này

![image](https://hackmd.io/_uploads/H1IzFpOxJe.png)

- tại server chuỗi JWT có cấu trúc H.P.S được Client gửi lên. Application Server trước khi thực hiện lệnh được gọi từ phía User, sẽ verify JWT gửi lên S tương tự như sau:
  - Set S1 = S
  - Set S2 = HMAC(H.P) vỡi secret key của hệ thống)
  - So sánh S1 == S2 ? . Nếu S1 và S2 khớp nhau, tức là chữ ký hợp lệ, hệ thống mới tiếp decode payload và tục kiểm tra các data trong payload và thực hiện lệnh được gọi.

## Phân tích các phương pháp tấn công JWT và biện pháp ngăn chặn

![image](https://hackmd.io/_uploads/Sk15KU2xke.png)

- mục tiêu này là bỏ qua xác thực và kiểm soát truy cập bằng cách mạo danh người dùng khác đã được xác thực.

Lưu ý: thư viện jsonwebtoken của Node.js chứa các hàm verify() và decode() thực hiện chức năng xác thực và giải mã thông tin. Tuy nhiên, nếu trong quá trình xây dựng ứng dụng, lập trình viên trực tiếp sử dụng hàm decode() mà thiếu đi bước kiểm tra xác thực, thì chương trình vẫn trả về các thông tin được lưu trữ trong payload của JWT, kể cả JWT token đã hết hạn!

### None Algorithm Attack với JWT

![image](https://hackmd.io/_uploads/HyGPBL3xkl.png)

- Tất cả JSON Web Token phải chứa tham số tiêu đề "alg", chỉ định thuật toán mà máy chủ nên sử dụng để xác minh chữ ký của token. Ngoài các thuật toán mạnh về mặt mật mã, đặc tả JWT cũng định nghĩa thuật toán "none", có thể được sử dụng với JWT "không an toàn" (không có chữ ký). Khi thuật toán này được hỗ trợ trên máy chủ, nó có thể chấp nhận các token không có chữ ký nào cả.
- JWT hỗ trợ giá trị “none” trong trường alg cho mục đích gỡ lỗi. Nếu trường này được đặt thành “none”, bất kỳ mã thông báo nào cũng sẽ được coi là hợp lệ, miễn là chữ ký phải trống. Điều này cho phép kẻ tấn công làm giả mã thông báo và đặt giá trị trường theo yêu cầu của chúng.

#### Khai thác

- Vì tiêu đề JWT có thể bị thay đổi ở phía máy khách, nên người dùng có ý đồ xấu có thể thay đổi tiêu đề "alg" thành "none", sau đó xóa chữ ký và kiểm tra xem máy chủ có còn chấp nhận mã thông báo hay không.

- Nếu có, họ có thể khai thác lỗ hổng này bằng cách cung cấp một yêu cầu tùy ý trong payload JWT để nâng cao đặc quyền của họ hoặc mạo danh người dùng khác. Ví dụ, nếu mã thông báo chứa yêu cầu "username": "guest", họ có thể thay đổi thành "username": "admin".

ví dụ bài lab sau : https://hackmd.io/@4w350m3/rkwxbwyaa#2-Lab-JWT-authentication-bypass-via-flawed-signature-verification

#### Khắc phục

- Đảm bảo rằng JWT không an toàn bị máy chủ từ chối và chỉ các thuật toán mạnh về mặt mật mã mới được chấp nhận và xác minh. Ngay cả khi ứng dụng không trực tiếp sử dụng JWT không an toàn, điều quan trọng là phải đảm bảo rằng tham số tiêu đề "alg": "none" bị hạn chế bởi thư viện phân tích cú pháp JWT cơ bản.

### Weak Signature Key với JWT

![image](https://hackmd.io/_uploads/Hk0XLL3lyl.png)

- chạy cuộc tấn công brute-force/dictionary/hybrid cổ điển. Một lần lặp lại yêu cầu tính toán hai hàm băm SHA256 (đây là cách HMAC-SHA256 hoạt động) và cũng có những công cụ tự động hóa toàn bộ hoạt động, chẳng hạn như hashcat triển khai việc bẻ khóa khóa JWT bằng GPU. Với một vài GPU tốc độ cao, bạn có thể đạt tốc độ hơn một tỷ lần kiểm tra mỗi giây. Hơn nữa, toàn bộ hoạt động có thể được thực hiện ngoại tuyến mà không cần bất kỳ tương tác nào với API
- khi secret key dùng để tạo Signature bị lộ do không đủ phức tạp dẫn đến dễ đoán và crack sẽ dẫn đến hậu quả nghiêm trọng, kẻ tấn công có thể tùy ý thay đổi các giá trị tham số quan trọng, từ đó mạo danh người dùng bất kỳ, nâng cấp quyền hạn tài khoản.

ví dụ bài lab sau: https://hackmd.io/@4w350m3/rkwxbwyaa#3-Lab-JWT-authentication-bypass-via-weak-signing-key

JWK (JSON Web Key) là một định dạng dữ liệu dùng để biểu diễn khóa mật mã, thường được sử dụng để ký hoặc mã hóa dữ liệu trong các ứng dụng web. Với JSON Web Token (JWT), thuật toán thường gặp là RS256 (RSA-SHA256), tức là sử dụng RSA để ký dữ liệu với hàm băm SHA-256. Điều này có nghĩa là, khi dùng RS256, quá trình xác thực JWT sẽ kiểm tra chữ ký để đảm bảo tính toàn vẹn của token và xác nhận nguồn gốc hợp lệ của nó.

- **jwk (JSON Web Key)**: Được sử dụng để nhúng một đối tượng JSON biểu diễn một khóa vào trong JWT headers. jwk chứa thông tin về khóa công khai được sử dụng để xác minh chữ ký của JWT (Thông thường là một cặp khóa public/private được tạo ra từ các thuật toán mã hóa RSA, ECDSA hoặc HMAC). Ví dụ:

```javascript!
    "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
    "typ": "JWT",
    "alg": "RS256",
    "jwk": {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
        "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m"
    }
}
```

- với máy chủ hỗ trợ jwk tham số trong tiêu đề JWT. Điều này đôi khi được sử dụng để nhúng khóa xác minh chính xác trực tiếp vào mã thông báo. Tuy nhiên, nó không kiểm tra được liệu khóa được cung cấp có đến từ một nguồn đáng tin cậy hay không, điều này đẫn đến nếu attacker có thể embedded JWK vào header thì server sẽ sử dụng nó như public key để verify cookie đã sign bằng private key mà attacker định trước

ví dụ lab: https://hackmd.io/@4w350m3/rkwxbwyaa#4-Lab-JWT-authentication-bypass-via-jwk-header-injection

- **jku (JWK Set URL)**: Chỉ định URL chứa tập hợp các khóa công khai trong định dạng JSON Web Key (JWK), người tạo JWT có thể cung cấp một URL trỏ đến tập hợp khóa công khai được sử dụng để xác minh chữ ký của JWT, thường có đường dẫn là /.well-known/jwks.json. Việc sử dụng public key được nhúng trong jwt có thể chứa nhiều rủi ro, bởi vậy một số ứng dụng sử dụng tham số jku nhằm xác định một URL tham chiếu tới một bộ khóa công khai được đặt ở server.Tuy nhiên, việc triển khai không đúng cách có thể tạo ra lỗ hổng bảo mật nghiêm trọng. Một cuộc tấn công tham số jku trong self-signed JWTs thường xảy ra một kẻ tấn công giả mạo JWT bằng cách thay đổi giá trị của jku để trỏ đến một URL mà kẻ tấn công kiểm soát. Khi truy cập tới URL này, ứng dụng sẽ lấy và sử dụng các public keys do kẻ tấn công tạo ra.

```javascript!
{
    "alg": "RS256",
    "jku": "https://example.com/.well-known/jwks.json"
}
```

- **kid (Key ID)**: Được sử dụng để xác định một ID cho khóa công khai được sử dụng để xác minh chữ ký của JWT. Tham số kid (Key ID) được sử dụng để xác định khóa công khai (public key) hoặc khóa bí mật (private key) trong xác minh chữ ký của JWT. kid giúp định danh và tìm kiếm khóa phù hợp trong trường hợp có nhiều khóa khác nhau được sử dụng, đồng thời cho phép hệ thống dễ dàng quản lý nhiều khóa khác nhau khi cần thiết.

nếu jku được chấp nhận ứng dụng sẽ xác thực danh tính người dùng bằng cách truy cập tới một URL chứa danh sách các public keys, kiểm tra ánh xạ qua giá trị tham số kid trong JWT. Tuy nhiên, khi tham số jku tồn tại trong JWT, giá trị URL này được ghi đè, dẫn đến ứng dụng sẽ truy cập tới jku trong JWT.
Do sự cài đặt sai sót này, chúng ta có thể tự dựng một trang web chứa danh sách các public keys, từ đó giả mạo tham số jku để ứng dụng truy cập tới trang web giả mạo đó.

ví dụ lab: https://hackmd.io/@4w350m3/rkwxbwyaa#5-Lab-JWT-authentication-bypass-via-jku-header-injection

### Algorithm Confusion Attack

- xảy ra khi kẻ tấn công có thể buộc máy chủ xác minh chữ ký của mã thông báo web JSON ( JWT ) bằng một thuật toán khác với thuật toán mà các nhà phát triển trang web dự định. Nếu trường hợp này không được xử lý đúng cách, điều này có thể cho phép kẻ tấn công làm giả JWT hợp lệ chứa các giá trị tùy ý mà không cần biết khóa ký bí mật của máy chủ.

Thuật toán đối xứng (Symmetric algorithms) sử dụng cùng một khóa (secret key) cho cả quá trình ký (sign) và xác minh (verify) JWT. Một ví dụ tiêu biểu là HS256 (HMAC-SHA256), trong đó HMAC (Hash-based Message Authentication Code) được sử dụng để ký và xác minh chữ ký. Với thuật toán đối xứng, cả server và client đều biết khóa bí mật.

![image](https://hackmd.io/_uploads/H15iDTsekg.png)

Mặt khác, thuật toán bất đối xứng (Asymmetric algorithms) sử dụng một cặp khóa gồm khóa riêng tư (private key) và khóa công khai (public key) để thực hiện quá trình ký và xác minh JWT. Khi server tạo JWT, nó sẽ sử dụng khóa riêng tư để ký chữ ký. Sau đó, client sử dụng khóa công khai tương ứng để xác minh chữ ký. Ví dụ về thuật toán bất đối xứng RS256 (RSA-SHA256):

![image](https://hackmd.io/_uploads/SyT0v6jeJl.png)

JWT cho phép các thuật toán khác nhau được sử dụng để ký và xác minh chữ ký. Tuy nhiên, khi không kiểm tra hoặc kiểm tra không chính xác thuật toán được chỉ định trong phần header của JWT, người tấn công có thể thay đổi thuật toán để tận dụng các lỗ hổng liên quan đến việc triển khai hoặc xử lý JWT.

làm giả mã thông báo JWT bằng cách nào?

- attacker có được một khóa công khai (tên của nó cho thấy rằng nó có thể được công khai). Đôi khi, nó được truyền trong chính JWT.
- Gửi mã thông báo (với tải trọng đã thay đổi) với thuật toán HS256 được đặt trong tiêu đề (tức là HMAC, không phải RSA) và ký mã thông báo bằng khóa RSA công khai. Đúng vậy, không có lỗi nào ở đây – chúng tôi sử dụng khóa RSA công khai (mà chúng tôi cung cấp dưới dạng chuỗi) làm khóa đối xứng cho HMAC.
- Máy chủ nhận được mã thông báo, kiểm tra thuật toán nào được sử dụng cho chữ ký (HS256). Khóa xác minh được đặt trong cấu hình là khóa RSA công khai, vì vậy…:
- Chữ ký được xác thực (vì chính xác cùng một khóa xác minh được sử dụng để tạo chữ ký và kẻ tấn công đã đặt thuật toán chữ ký thành HS256).

![image](https://hackmd.io/_uploads/rJGOOI3gkx.png)

Nếu máy chủ đang mong đợi RSA nhưng được gửi HMAC-SHA với khóa công khai của RSA, máy chủ sẽ nghĩ rằng khóa công khai thực sự là khóa riêng HMAC. Điều này có thể được sử dụng để làm giả bất kỳ dữ liệu nào mà kẻ tấn công muốn.

#### Khai thác

Một cuộc tấn công Algorithm Confusionthường bao gồm các bước cấp cao sau đây:

1. Lấy khóa công khai của máy chủ
   - Trong trường hợp khóa công khai không có sẵn, bạn vẫn có thể kiểm tra sự nhầm lẫn của thuật toán bằng cách lấy khóa từ một cặp JWT hiện có. Quá trình này tương đối đơn giản khi sử dụng các công cụ như jwt_forgery.py. Bạn có thể tìm thấy công cụ này cùng với một số tập lệnh hữu ích khác trên rsa_sign2n
   - hoặc dùng bản docker đơn giản hơn của công cụ trên `docker run --rm -it portswigger/sig2n <token1> <token2>`
2. Chuyển đổi khóa công khai sang định dạng phù hợp
3. Tạo JWT độc hại với tải trọng đã sửa đổi và algtiêu đề được đặt thành HS256.
4. Ký mã thông báo bằng HS256 , sử dụng khóa công khai làm bí mật.

- ví dụ lab sau: https://hackmd.io/@4w350m3/rkwxbwyaa#8-Lab-JWT-authentication-bypass-via-algorithm-confusion-with-no-exposed-key

#### Khắc phục

- Có thể dễ dàng ngăn chặn phương thức tấn công này bằng cách chỉ cho phép sử dụng một loại thuật toán mã hóa duy nhất, đồng thời tăng độ phức tạp của secret key.
- Nâng cấp ==jsonwebtoken== lên phiên bản 9.0.0 hoặc cao hơn.

### Directory traversal và SQLi

KID là một tiêu đề tùy chọn trong JWT, cho phép các nhà phát triển chỉ định khóa nào sẽ được sử dụng để xác minh mã thông báo. Đây là cách tham số KID trông như thế nào trong JWT:

```
{
 "alg" : "HS256",
 "typ" : "JWT",
 "kid" : "123"
}
```

Directory traversal

- KID cung cấp vị trí của tệp khóa trên hệ thống tệp, việc vệ sinh không đúng cách trước khi sử dụng có thể dẫn đến các cuộc tấn công duyệt thư mục. Khi đó, kẻ tấn công sẽ có thể chỉ định bất kỳ tệp nào trong hệ thống tệp làm khóa để sử dụng để xác minh mã thông báo. Trong trường hợp xấu nhất, kẻ tấn công sẽ có thể sử dụng bất kỳ khóa nào trong hệ thống tệp để xác minh mã thông báo.

SQLi

- Vì trường KID có thể được cung cấp bởi người dùng, nó mở đường cho một số cuộc tấn công tiêm mã. Nó có thể dẫn đến tiêm mã SQL nếu KID đang được lấy từ cơ sở dữ liệu. Kẻ tấn công có thể sử dụng tải trọng sau:
- “kid”: "invalid-key' UNION SELECT 'attackers-key';--".
- Vì cơ sở dữ liệu không chứa invalid-key, nên mã thông báo sẽ được xác minh bằng cách sử dụng attackers-key

### JWT Timing Attack

- Sử dụng thời gian phản hồi từ server để suy ra các thông tin trong JWT. Kẻ tấn công có thể sử dụng kỹ thuật này để suy ra chữ ký hoặc mã hóa của JWT và tạo ra một JWT mới.
- Nếu chữ ký từ JWS được kiểm tra từng byte một với chữ ký chính xác (do bên chấp nhận JWS tạo ra) và nếu quá trình xác minh hoàn tất trên byte đầu tiên không nhất quán , chúng ta có thể dễ bị tấn công theo thời gian.
- Lưu ý rằng trong trường hợp này, chúng ta có càng nhiều byte khớp nhau thì càng cần nhiều phép so sánh và do đó thời gian cần thiết để phản hồi càng lâu.

## LAB task 2

### Phân tích

![image](https://hackmd.io/_uploads/SJVNoHjekg.png)

- thấy web có dùng =="jsonwebtoken": "^8.5.1"==
- jsonwebtoken là một triển khai JSON Web Token (đối xứng và bất đối xứng)

với phiên bản 8.5.1 này

- Các phiên bản bị ảnh hưởng của gói này dễ bị xác thực không đúng, do đó việc thiếu định nghĩa thuật toán trong hàm jwt.verify() có thể dẫn đến việc bỏ qua xác thực chữ ký do mặc định không có thuật toán nào để xác minh chữ ký.

- Các phiên bản bị ảnh hưởng của gói này dễ bị hạn chế không đúng cách trong việc gán mã thông báo bảo mật thông qua đối số secretOrPublicKey do cấu hình sai của hàm truy xuất khóa jwt.verify(). Việc khai thác lỗ hổng này có thể dẫn đến việc xác minh không chính xác các mã thông báo giả mạo khi mã thông báo được ký bằng khóa chung không đối xứng có thể được xác minh bằng thuật toán HS256 đối xứng.
- Lưu ý: Lỗ hổng này ảnh hưởng đến ứng dụng của bạn nếu nó hỗ trợ sử dụng cả khóa đối xứng và bất đối xứng khi triển khai jwt.verify() với cùng chức năng truy xuất khóa.

- ở source code backend
- lúc tạo token web chỉ dùng RS256 để tạo và dùng private key trên server để ký

![image](https://hackmd.io/_uploads/rJglCSslJl.png)

- nhưng khi verify thì có thể dùng kiểm tra chữ ký với public key trên server qua các thuật toán RS256, HS256, ES256

![image](https://hackmd.io/_uploads/Sy--AHsgyl.png)

Chương trình trên chấp nhận xác thực JWT do người dùng cung cấp trong cả hai trường hợp token sử dụng thuật toán RS256 (bất đối xứng) và HS256 (đối xứng). Khi đó, nếu ứng dụng bị lộ RSA public key, kẻ tấn công có thể chuyển thể sang dạng PEM, mã hóa Base64 và sử dụng như secret key của thuật toán đối xứng

Trong trường hợp này, nếu máy chủ nhận được mã thông báo được ký bằng thuật toán đối xứng như HS256, verify()phương pháp chung của thư viện sẽ coi khóa công khai là bí mật HMAC. Điều này có nghĩa là kẻ tấn công có thể ký mã thông báo bằng HS256 và khóa công khai, và máy chủ sẽ sử dụng cùng khóa công khai để xác minh chữ ký.

- và chỉ cần trường username trong payload có giá trị là admin thì có thể giả mạo credential cảu admin và vào endpoint /admin lấy flag

![image](https://hackmd.io/_uploads/Bk_YCAolJg.png)

![image](https://hackmd.io/_uploads/SyRzyk3e1e.png)

### Khai thác

- bước đầu tiên cần lấy được public key của thuật toán RSA
- em đăng nhập lần đầu và lấy được token 1:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiaWF0IjoxNzMwMDA0NTk5LCJleHAiOjE3MzAwMDgxOTl9.fM9ohTeKy4wUQIBiS2c-jFPbVt1LUxCrF3fjNfB_WHm21yxFjdTWFkxig_Oloaq4Gqaq28Gd9D-TQp-ilCjyqwNt_N055uVBWD9lpMCxQWxdv9kKqnI8-jTgctSaCaZhF9Qhxmd-sJhnkCcKfmNmI9FRFJLZBTAt2QhV3qz5cUr7m_ryc8azReGbIT8gb-0wR1FWyYEYMUto9IJYoIzwdWFlxfiG1vyAdwD_CCD5ilg1Q5WqG_auOmkEvF2zCOQhuN5YATk6AWqK3h59E4oBE602JpU738uir_bwAb0S2bh0vwqFK-0Ij0v-idtxabP7iiTtEDK_lzFTUeRY4yoWAA
```

- logout và sau đó login lại em được token 2:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiaWF0IjoxNzMwMDA0NjYyLCJleHAiOjE3MzAwMDgyNjJ9.LH9f6GKTKx8wAOFop8xvsUmQpMuHfv_qocI6UejvfwV3nW2INiYHKh-ATJ3TghZwvgBE4LlJmPiAc4jg1whk3Y9fyzHFe4_-k4jf7BVX5wWu8-eIB8z4tNsTGm8iZ65av12--dgt94r484g0uGSMXy_cD8svbehJll8eBbI7kn3Nh8742mcjk2L82HopgMibacjja-kwLZnqPAaukSUzVeFGmU_lWuZs1-VcYa4LF3xWAS3GE8jH1SjgqOUIbD23N9NWhQoc-coTVmbh2uUvPxG77s5bvJ9pNKk4xsRfZVi_jld43zR5qARulTzWx3shBuwa82HX8Md91rHZB-dsiQ
```

- em chạy chạy tooll mà portswigger cung cấp để tìm khóa công khai RSA

```
docker run --rm -it portswigger/sig2n eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiaWF0IjoxNzMwMDA0NTk5LCJleHAiOjE3MzAwMDgxOTl9.fM9ohTeKy4wUQIBiS2c-jFPbVt1LUxCrF3fjNfB_WHm21yxFjdTWFkxig_Oloaq4Gqaq28Gd9D-TQp-ilCjyqwNt_N055uVBWD9lpMCxQWxdv9kKqnI8-jTgctSaCaZhF9Qhxmd-sJhnkCcKfmNmI9FRFJLZBTAt2QhV3qz5cUr7m_ryc8azReGbIT8gb-0wR1FWyYEYMUto9IJYoIzwdWFlxfiG1vyAdwD_CCD5ilg1Q5WqG_auOmkEvF2zCOQhuN5YATk6AWqK3h59E4oBE602JpU738uir_bwAb0S2bh0vwqFK-0Ij0v-idtxabP7iiTtEDK_lzFTUeRY4yoWAA eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiaWF0IjoxNzMwMDA0NjYyLCJleHAiOjE3MzAwMDgyNjJ9.LH9f6GKTKx8wAOFop8xvsUmQpMuHfv_qocI6UejvfwV3nW2INiYHKh-ATJ3TghZwvgBE4LlJmPiAc4jg1whk3Y9fyzHFe4_-k4jf7BVX5wWu8-eIB8z4tNsTGm8iZ65av12--dgt94r484g0uGSMXy_cD8svbehJll8eBbI7kn3Nh8742mcjk2L82HopgMibacjja-kwLZnqPAaukSUzVeFGmU_lWuZs1-VcYa4LF3xWAS3GE8jH1SjgqOUIbD23N9NWhQoc-coTVmbh2uUvPxG77s5bvJ9pNKk4xsRfZVi_jld43zR5qARulTzWx3shBuwa82HX8Md91rHZB-dsiQ
```

- và em được kết quả là

![image](https://hackmd.io/_uploads/Sy3xOrolyx.png)

- thấy có 2 kết quả token trả về nên em thử lần lượt và thấy token đầu tiên vào được trang chính

![image](https://hackmd.io/_uploads/HyeS_Bsgyx.png)

- vậy em lấy được public key RSA của server là:

```
Base64 encoded x509 key: LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUE1ZjdzZ2N0Y3lpY0RLVE9BeXJ6VwpPZStUcUVXVDhpN2paaHFvT2c4aU4vS3NtOVpKWUtSS3F6WFAzYWcvSUswTXhwMXpLTHRicVVWeVJMZjk1L21yClowLzZTSnBwQkg0SWhPY045bnVwYmtxaWtQM2FYdGw4dWh2bVBEbGozeVdvT2p3VVQyNFVodnhEZ1VOaElLUEYKZ3JJWTZHcldndFlPQ3RBdzRwWHBDSUFvVUhBTDBWWUk2eGlEY3pRcS9CRCtaaG4yN21JWnR4YVhyNFdtZDY5TQpidFNCU2p3aS9QaXZ1bi91eENtcGZYTUxPMkg0S3Z2OE9vZjNEUGozUlhkRlp3Yjh2Z2poMlNYL05GYXJOQTBYCkg3cTFtSk5JeitSSi9zeGxDdHp6K05nZnQyZDVZaUc4QVFvNVJwWk91MDRRY0ZCTXc1OHdzU2FkeG5aRjNVNTEKWXdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==
    Tampered JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ICJndWVzdCIsICJpYXQiOiAxNzMwMDA0NTk5LCAiZXhwIjogMTczMDA5MTM2MH0.oOfQjpZ3-oNWNtgBYKgiNPlZLcgTvuBPU1VHWJTG5kw
```

- tiếp theo em tạo 1 new sysmetric key với x509 key tương ứng của token hợp lệ

![image](https://hackmd.io/_uploads/rJAa9HilJe.png)

- sửa trường username thành admin và ký lại token với HSA256 key em vừa tạo

![image](https://hackmd.io/_uploads/Sk6ctrigJe.png)

- sau đó gửi request đến /admin và em có được flag

![image](https://hackmd.io/_uploads/S15-trigJe.png)
