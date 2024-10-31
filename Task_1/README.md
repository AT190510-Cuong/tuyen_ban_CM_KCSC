# Task 1

![image](https://hackmd.io/_uploads/Skqx7KQ1kl.png)

## Khái niệm

- GraphQL là một ngôn ngữ truy vấn API được thiết kế để tạo sự giao tiếp hiệu quả giữa client và server. Nó cho phép người dùng chỉ định chính xác dữ liệu mà họ muốn nhận trong phản hồi, giúp tránh việc trả về quá nhiều dữ liệu thừa của đối tượng và nhiều truy vấn như thường thấy trong REST API.

### Cách thức hoạt động của GraphQL

- Dữ liệu mà schema GraphQL mô tả có thể được xử lý bằng ba loại hoạt động:
  - Truy vấn (Queries): Lấy dữ liệu.
  - Thay đổi (Mutations): Thêm, thay đổi hoặc xóa dữ liệu.
  - Đăng ký (Subscriptions): Tạo một kết nối vĩnh viễn giữa máy chủ và khách hàng, cho phép máy chủ đẩy dữ liệu thời gian thực đến khách hàng trong định dạng đã chỉ định.

Tất cả các hoạt động GraphQL đều sử dụng cùng một điểm cuối và thường được gửi dưới dạng POST request

Với GraphQL, type và name của operation xác định cách xử lý truy vấn, thay vì endpoint mà truy vấn được gửi đến hoặc HTTP method được sử dụng.

### GraphQL vs REST API

![image](https://hackmd.io/_uploads/HJ-TmoLJkx.png)

- Tất cả các toán tử (operations) GraphQL sử dụng cùng một endpoint, thường được gửi dưới dạng yêu cầu POST. Điều này khác biệt đáng kể so với REST API, nơi mà các hoạt động được gửi đến các endpoint cụ thể dựa trên các phương thức HTTP khác nhau

- https://www.youtube.com/watch?v=PWbsH2q8g3c

| **GraphQL**                                                                                 | **REST**                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nó chỉ là 1 ngôn ngữ truy vấn APIs.                                                         | Là 1 khái niệm, 1 loại kiến trúc phần mềm mà định nghĩa 1 số ràng buộc, quy tắc cần tuân theo khi thiết kế web services.                                                      |
| Chỉ deploy 1 endpoint duy nhất và client có thể quyết định lấy những dữ liệu nào cần thiết. | Deploy nhiều endpoints và mỗi endpoint thông thường sẽ trả về 1 resource duy nhất (VD như /api/v1/users sẽ trả về danh sách users, còn /books sẽ trả về danh sách books,...). |
| Sử dụng kiến trúc hướng tới phía client.                                                    | Sử dụng kiến trúc hướng tới phía server.                                                                                                                                      |
| Không có cơ chế caching được tích hợp sẵn mà phải sử dụng các thư viện bên ngoài.           | Có tính năng caching mặc định.                                                                                                                                                |
| Không hỗ trợ API versioning.                                                                | Hỗ trợ API versioning.                                                                                                                                                        |
| Dữ liệu trả về chỉ có JSON.                                                                 | Dữ liệu trả về có thể XML, JSON, và YAML.                                                                                                                                     |
| Có hệ thống định nghĩa kiểu dữ liệu rõ ràng và documents sẽ được tạo tự động.               | Không có.                                                                                                                                                                     |

vấn đề của REST API:

- `Over fetching`: trả về dữ liệu dư thừa VD khi ta chỉ cần dữ liệu của 2 trường title và prize thì trong response lại trả ra toàn bộ thông tin sản phẩm ![image](https://hackmd.io/_uploads/H18GtimJJg.png)
- `Under fetching` khi mà trong 1 endpoint không chứa đủ thông tin phía client cần để hiển thị ==> cần query thêm 1 endpoint khác

==> grahpql giải quyết được vấn đề này ==> chỉ lấy những dữ liệu cần thiết thôi

### GraphQL schema

- Nó định nghĩa hình dạng của dữ liệu, kiểu dữ liệu, và các truy vấn (queries) hay thao tác (mutations) mà máy chủ GraphQL có thể xử lý

VD:

```javascript
type User {
  id: ID!
  name: String!
  email: String!
}

type Query {
  getUser(id: ID!): User
}

type Mutation {
  createUser(name: String!, email: String!): User
}
```

- Schema này định nghĩa một User, một truy vấn getUser để lấy thông tin của người dùng dựa trên ID, và một mutation createUser để tạo mới một người dùng.

### GraphQL queries

- Truy vấn GraphQL lấy dữ liệu từ kho dữ liệu. Chúng tương đương với các yêu cầu GET trong REST API.
- Các truy vấn thường có các thành phần chính sau:
  - loại operation: query
  - Tên query: tên truy vấn là tùy chọn, nhưng được khuyến khích vì nó có thể giúp gỡ lỗi
  - Cấu trúc dữ liệu. Đây là dữ liệu mà truy vấn sẽ trả về
  - Tùy chọn, một hoặc nhiều đối số. Chúng được sử dụng để tạo các truy vấn trả về thông tin chi tiết của một đối tượng cụ thể

VD: truy vấn này yêu cầu lấy thông tin về một sản phẩm cụ thể có id = 123, với thông tin bao gồm tên và mô tả của sản phẩm

```javascript
    #Example query

    query myGetProductQuery {
        getProduct(id: 123) {
            name
            description
        }
    }
```

với ví dụ trên:

- `query`: Đây là từ khóa để định nghĩa một truy vấn GraphQL.
- `myGetProductQuery`: Tên của truy vấn này
- `getProduct`: Tên của một trường hoặc resolver, thường là một phương thức trên server để lấy thông tin về sản phẩm (product).
- `(id: 123)`: Đây là đối số (argument) của trường getProduct
- `name` và `description`: Đây là các trường con (subfields) của đối tượng trả về từ getProduct. Truy vấn chỉ yêu cầu server trả về tên (name) và mô tả (description) của sản phẩm.

### GraphQL mutations

- Mutations thay đổi dữ liệu theo một cách nào đó, có thể là thêm, xóa hoặc chỉnh sửa dữ liệu. Chúng tương đương với các phương thức POST, PUT và DELETE của REST API.

Ví dụ bên dưới cho thấy một mutations để tạo ra một sản phẩm mới và phản hồi liên quan của nó. Trong trường hợp này, dịch vụ được cấu hình để tự động gán ID cho các sản phẩm mới, đã được trả về theo yêu cầu.

```javascript
    #Example mutation request

    mutation {
        createProduct(name: "Flamin' Cocktail Glasses", listed: "yes") {
            id
            name
            listed
        }
    }
```

```javascript
#Example mutation response

    {
        "data": {
            "createProduct": {
                "id": 123,
                "name": "Flamin' Cocktail Glasses",
                "listed": "yes"
            }
        }
    }
```

## Introspection

- Introspection là một hàm GraphQL tích hợp cho phép bạn truy vấn máy chủ để biết thông tin về schema bao gồm các kiểu dữ liệu, truy vấn, và mutations có sẵn
- Để sử dụng introspection để khám phá thông tin schema hãy truy vấn trường `__schema`. Trường này có sẵn trên root type của tất cả các query
- Giống như các query thông thường, bạn có thể chỉ định các trường và cấu trúc của phản hồi mà bạn muốn trả về khi chạy introspection query.
- Bạn có thể thăm dò introspection bằng cách sử dụng query đơn giản sau. Nếu introspection được bật, phản hồi sẽ trả về tên của tất cả các truy vấn khả dụng.

```javascript
#Introspection probe request

    {
        "query": "{__schema{queryType{name}}}"
    }
```

- Tính năng này rất hữu ích trong quá trình phát triển và gỡ lỗi, nhưng nếu không được bảo vệ, nó có thể tạo ra các lỗ hổng bảo mật.

1. Tiết lộ thông tin nhạy cảm
   - kẻ tấn công có thể gửi một truy vấn để khám phá toàn bộ schema của GraphQL server.
   - Xác định các truy vấn, mutations, và subscriptions có sẵn
   - Tìm các endpoint nhạy cảm, chẳng hạn như những endpoint quản lý dữ liệu người dùng, xác thực, hoặc thao tác dữ liệu mà đáng lẽ ra không nên để lộ.
   - Tiếp cận các trường dữ liệu nhạy cảm như thông tin cá nhân, mật khẩu hoặc token API.
2. Tấn công dựa trên kiến trúc ứng dụng
   - Việc lộ ra cấu trúc chi tiết của schema có thể giúp kẻ tấn công xây dựng một kế hoạch tấn công chính xác hơn. Ví dụ, họ có thể tìm cách khai thác những điểm yếu trong các mutations có thể dẫn đến SQL Injection, NoSQL Injection hoặc tấn công DoS (Denial of Service)

## Broken Authentication & Authorization

đối tượng GrapQL không thể chứa nhiều thuộc tính với tên giống nhau. Thường thì, trong GraphQL, các đối tượng không thể chứa nhiều thuộc tính có cùng tên. Các aliases cho phép chúng ta bypass cơ chế giới hạn này bằng cách chỉ định tên cho các thuộc tính mà bạn muốn API trả về. Ở đây chúng ta có thể sử dụng nhiều alias để trả về nhiều nhiều dữ liệu của cùng loại đối tượng trong một yêu cầu HTTP.
Ví dụ để trả về dữ liệu cho 2 product sử dụng getProduct chúng ta không thể sử dụng như sau:

```javascript

#Invalid query

    query getProductDetails {
        getProduct(id: 1) {
            id
            name
        }
        getProduct(id: 2) {
            id
            name
        }
    }

```

Mà thay vào đó, để trả về dữ liệu của 2 product khác nhau thông qua getProduct với 2 alias khác nhau:

```javascript
    #Valid query using aliases

    query getProductDetails {
        product1: getProduct(id: "1") {
            id
            name
        }
        product2: getProduct(id: "2") {
            id
            name
        }
    }

```

Mặc dù alias được thiết kế để giới hạn số lần gọi API mà bạn cần thực hiện, nhưng chúng cũng có thể được sử dụng để thực hiện tấn công brute force vào một endpoints GraphQL.

Nhiều endpoints sẽ giới hạn số request HTTP được gọi tới để ngăn chặn các cuộc tấn công brute force. Nhưng với cách sử dụng alias này, chúng ta có thể chỉ cần gửi 1 request HTTP nhưng có thể lấy được nhiều dữ liệu như ở ví dụ nêu trên.

- Cách tiếp cận này sẽ đánh lừa các ứng dụng giám sát rate monitoring nghĩ rằng mọi thứ đều ổn và không có bot brute force nào cố gắng đoán mật khẩu.

## Làm sao để tìm được GraphQL Enpoint?

![image](https://hackmd.io/_uploads/BJykLjIyJx.png)

Trước khi có thể kiểm thử API GraphQL, ta cần tìm ra endpoint của nó.

Vì các API GraphQL sử dụng cùng một endpoint cho tất cả các request nên đây là thông tin quan trọng.

=> Burp Scanner có thể tự động phát hiện ra endpoint GraphQL và phát sinh sự cố GraphQL endpoint found.

## Prevent

- Nếu API không public thì tốt nhất là nên tắt introspection giải lộ thông tin nhạy cảm
- Nếu API này là public thì cần phải bật introspection. Nên xem xét lại scheme để nó không lộ lọt những trường không mong muốn.
- Nên vô hiệu hóa suggestions ngăn việc sử dụng Clairvoyance để suy luận ra thông tin lược đồ
- API không nên hiển thị bất kì trường user private nào như email, userid
- Ngăn chặn alias brute force
  - Giới hạn độ sâu truy vấn của API. Độ sâu truy vấn chính là số lượng truy vấn lồng nhau trong một query.
  - Định cấu hình số lượng byte tối đa mà một truy vấn có thể chứa
  - Nên phân tích chi phí trên API. Xác định lượng tài nguyên cần để chạy truy vấn , nếu quá phức tạp về tính toán để chạy thì loại bỏ luôn.
- Ngăn chặn CSRF
  - APi chỉ chấp nhận các query POST
  - API có cơ chế mã thông báo CSRF an toàn
  - khớp với Content-type được cung cấp Content-type: application/json

## 1. Lab: Accessing private GraphQL posts

link: https://portswigger.net/web-security/graphql/lab-graphql-reading-private-posts

### Đề bài

![image](https://hackmd.io/_uploads/r1XvMoL1Jl.png)

### Phân tích

- Bài lab cho chúng ta một danh sách các bài post. Yêu cầu của bài lab là truy cập được vào một bài viết bí mật và lấy ra được password.

- trang web chứa các bài blog và phía client sẽ gọi query `getBlogSummaries` tại trang chính nơi chứa tất cả các trang blog có id từ 1 đến 5 nhưng bị thiếu mất id 3 ==> đây có thể là bài blog ẩn cần tìm

![image](https://hackmd.io/_uploads/SJK-2381Jx.png)

- vào từng bài blog chúng ta thấy được query `getBlogPost`

![image](https://hackmd.io/_uploads/H1yGp28yyg.png)

nhiệm vụ của chúng ta là lấy được `password` nhưng trong bài blog có id 3 này không không thấy chứa giá trị password mà chúng ta cần tìm ==> có thể còn các field khác mà trong query chưa dùng đến ==> cần biết thông tin về schema

- kiểm tra xem introspection có được bật không

![image](https://hackmd.io/_uploads/SJKVNLDJJl.png)

- send request thấy kết quả trả về chứa thông tin schema

### Khai thác

- em dùng extension InQL để quét các field ẩn thấy có chứa `postPassword` mà chúng ta cần tìm

![image](https://hackmd.io/_uploads/H1nDXUPyJe.png)

- em query với field này và lấy được thông tin của password cần tìm

![image](https://hackmd.io/_uploads/HyqBBLPyJg.png)

- em đem đi submit và solve được bài lab này

![image](https://hackmd.io/_uploads/B1qDrIwkkg.png)

## 2. Lab: Accidental exposure of private GraphQL fields

link: https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure

### Đề bài

![image](https://hackmd.io/_uploads/BytcULPkkl.png)

### Phân tích

- Bài lab yêu cầu login được tài khoản admin và xóa user carlos
- tương tự bài trước em kiểm tra xem web có bật introspection không

![image](https://hackmd.io/_uploads/SJvaYIwkke.png)

- em thấy có bật introspection và xem schema

![image](https://hackmd.io/_uploads/Hkg7cIwkkx.png)

- thấy được có query getUser theo id
- và thấy trong blog các id tuyến tính có kiểu dữ liệu int bắt đầu từ 1

### Khai thác

- em gửi đi query getUser và thay id = 1 và nhận được thông tin của admin

![image](https://hackmd.io/_uploads/BJuK5LPJkl.png)

- đăng nhập tài khoản admin và xóa user carlos khi đó bài lab được giải quyết

![image](https://hackmd.io/_uploads/SkPviUvJ1e.png)

## 3. Lab: Finding a hidden GraphQL endpoint

link: https://portswigger.net/web-security/graphql/lab-graphql-find-the-endpoint

### Đề bài

![image](https://hackmd.io/_uploads/Skys5Dv1yl.png)

### Phân tích

- Bài lab yêu cầu tìm đến enpoints ẩn để xóa user carlos

- em dùng burp scan và ra được enpoint /api

![image](https://hackmd.io/_uploads/SkoERww1kx.png)

![image](https://hackmd.io/_uploads/HyDp0vDkJx.png)

- Tiếp tục em gửi request để kiểm tra introspection và được kết quả GraphQL introspection is not allowed

![image](https://hackmd.io/_uploads/HJGB1uwkJx.png)

- theo như đề bài thì đã có cơ chế bảo vệ introspection và em cần bypass nó

### Khai thác

- em thêm ký tự new line %0a vào sau \_\_schema và gửi request. Kết quả có thể lấy được dữ liệu

![image](https://hackmd.io/_uploads/S14Ql_D1yx.png)

- em copy toàn bộ respone trả về vào file json rồi đưa vào InQL phân tích

![image](https://hackmd.io/_uploads/rkPKWdv1kg.png)

- thấy được quey deleteOrganizationUser

- và em biết được user carlos có id là 3

![image](https://hackmd.io/_uploads/SkNhGuvyJg.png)

- tiếp đến xóa user này và em solve được lab

![image](https://hackmd.io/_uploads/BkUym_vJJg.png)

![image](https://hackmd.io/_uploads/S1HgXuwkkl.png)

## 4. Lab: Bypassing GraphQL brute force protections

link: https://portswigger.net/web-security/graphql/lab-graphql-brute-force-protection-bypass

### Đề bài

![image](https://hackmd.io/_uploads/Bk1-N_wyye.png)

### Phân tích

- Bài lab yêu cầu bypass cơ chế ngăn chặn brute force để log in vào tài khoản carlos
- Login với tài khoản carlos và mật khẩu bất kì

![image](https://hackmd.io/_uploads/HJJwDuvJJl.png)

- thấy trong response trả về trang thái và token

- khi em tiếp tục gửi request đăng nhập nhiều lần thì xuất hiện thông báo đăng nhập sai nhiều lần ==> cơ chế chống limit login của website

![image](https://hackmd.io/_uploads/SJ7cv_Dkkg.png)

- và chúng ta biết trang web này dùng graphql nó có cơ chế alias để trả về nhiều phiên bản của cùng một loại đối tượng trong một yêu cầu. Điều này giúp giảm số lượng cuộc gọi API cần thiết.

### Khai thác

Sử dụng code javascript để tạo ra nhiều alias khác nhau với list mật khẩu sử dụng

![image](https://hackmd.io/_uploads/HJagK_Py1e.png)

![image](https://hackmd.io/_uploads/Bkwq5_wkJe.png)

- kết quả có tài khoản đăng nhập thành công là `carlos:thunder`

![image](https://hackmd.io/_uploads/r1wjFODyJl.png)

## 5. Lab: Performing CSRF exploits over GraphQL

link: https://portswigger.net/web-security/graphql/lab-graphql-csrf-via-graphql-api

### Đề bài

![image](https://hackmd.io/_uploads/By9i3ODJke.png)

### Phân tích

- bài lab cho biết endpoint chấp nhận các yêu cầu có loại nội dung là `x-www-form-urlencoded` và do đó dễ bị tấn công CSRF, yêu cầu chúng ta tạo mã HTML sử dụng tấn công CSRF để thay đổi địa chỉ email của người xem
- đăng nhập bằng tài khoản wiener:peter và thực hiện đổi email với x-www-form-urlencoded

![image](https://hackmd.io/_uploads/B1ix-FDykl.png)

- thấy reponse trả về đổi email thành công

### Khai thác

- em tạo csrf poc

![image](https://hackmd.io/_uploads/r1CwWFwk1g.png)

```htmlembedded
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
    <form action="https://0af0005d0387f1d481400cb800430089.web-security-academy.net/graphql/v1" method="POST">
      <input type="hidden" name="query" value="mutation&#32;changeEmail&#40;&#36;input&#58;ChangeEmailInput&#33;&#41;&#123;changeEmail&#40;input&#58;&#36;input&#41;&#123;email&#125;&#125;" />
      <input type="hidden" name="operationName" value="changeEmail" />
      <input type="hidden" name="variables" value="&#123;&quot;input&quot;&#58;&#123;&quot;email&quot;&#58;&quot;abcd&#64;gmail&#46;com&quot;&#125;&#125;" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```

![image](https://hackmd.io/_uploads/rJoJvYw1ye.png)

- store và delivery exploit to victim và em solve được lab

![image](https://hackmd.io/_uploads/rJV3LYwk1g.png)
