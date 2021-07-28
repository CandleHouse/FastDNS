# FastDNS

*Small demo for configuring local DNS domain name mapping*

## 一个配置本地DNS域名映射的简单样例

诸如Github国内登录缓慢，不方便配置梯子或者不稳定的情况下想要浏览网页很慢

一个简单的办法是配置本地的DNS域名，但是同样由于不稳定的原因，这种操作需要定期更新，由此fastDns应运而生

基本原理：从http://tool.chinaz.com/dns/ 中获取域名的DNS ip，选择ttl最低的连接，然后选择修改本机hosts文件，最后刷新dns并测试稳定性，全程一体化操作，执行完毕后即可愉快畅游

同时，该fastDns.py可以重复执行，达到刷新的目的

也可以自动增加原本没有的域名dns，如raw.githubusercontent.com，以浏览readme中的图片

- - -
#### 自动工作目录切换

<pre><code>current_path = os.path.dirname(__file__)
os.chdir(current_path)
</code></pre>

之后可以直接使用python命令行执行.py文件，如果是windows，您甚至可以编写shell指令在“任务计划程序”中按需要自动化执行

![Image text](https://raw.githubusercontent.com/CandleHouse/FastDNS/master/example.png)
