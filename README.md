# Caidao-AES-Version
用AES算法透明加密菜刀的http数据流

## 功能介绍
Caidao.exe与服务器的http交互是明文，容易被分析和拦截。
偶然看到《“冰蝎”动态二进制加密网站管理客户端》https://github.com/rebeyond/Behinder, 这个套路不错哈；

习惯了用菜刀, 于是决定给菜刀做一个Burp的Python AES加密插件，自动加解密caidao.exe与服务器端交互的http数据流，
进而达到过WAF的目的。


## 使用方式

1. git clone https://github.com/ekgg/Caidao-AES-Version.git
2. 下载安装Burp Suite Community Edition v1.7.36 https://portswigger.net/burp/communitydownload (其它版本未测试，应该问题不大)
3. 下载Jython 2.7.0 - Standalone Jar http://www.jython.org/downloads.html
4. 启动Burp，配置Extender的选项，添加python运行环境
![image](https://github.com/ekgg/Caidao-AES-Version/blob/master/Pic/20190113135843.png)	
5. 在Burp Extensions中，添加并启用Caidao Crypto(AES)的python脚本
	.\Caidao-AES-Version\BurpSuite-Caidao-Extender\CaidaoExt.py
![image](https://github.com/ekgg/Caidao-AES-Version/blob/master/Pic/20190113135844.png)	
6. 在Intenet选项中，设置系统代理为Burp监听的 127.0.0.1:8080
7. 将修改过的\Caidao-AES-Version\Caidao-AES-PHP\cdaes.php上传到服务器端
8. 启动caidao.exe，找开服务器端的cdaes.php地址，可在Wireshark中观察是否已经加密了http数据流
![image](https://github.com/ekgg/Caidao-AES-Version/blob/master/Pic/20190113141221-aes.png)	
9. 在Burp中，可以查看自动加解密http post的数据流
![image](https://github.com/ekgg/Caidao-AES-Version/blob/master/Pic/20190113141745-cd2.png)	

## 注意事项
1.PHP连接有问题？

因为采用了aes加密，请确认PHP是否开启了OpenSSL扩展，可通过echo var_dump(function_exists("openssl_encrypt"));是否为true来判断。

2.有Java, .Net版本的webshell吗？
暂时还没有空写。

3.我怎么运行不起来？
请将你的测试环境提交到isues, 上面列出的软件(caidao,burp,jython),我没有测试完所有有的版本。
推荐你用我列出的版本来测试:

```txt
caidao-20141213
Burp Suite Community Edition v1.7.36
jython-standalone-2.7.0.jar
```

## AES默认的加密key
在python和php脚本用的是一个简单的密码，请自行修改

```php
$mykey = "0123456789012345";
$myiv = "9876543210987654";
$mymethod = 'AES-128-CFB';
```

## 参考与感谢
```txt
http://www.4hou.com/technology/15501.html
https://github.com/raddyfiy/caidao-official-version  
https://github.com/rebeyond/Behinder
https://github.com/PortSwigger/example-custom-editor-tab/.
https://github.com/securityMB/burp-exceptions
https://github.com/PortSwigger/example-traffic-redirector/tree/master/python
https://github.com/parsiya/Parsia-Code/tree/master/python-burp-crypto
```
