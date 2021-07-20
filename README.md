# FastDNS
*Small demo for configuring local DNS domain name mapping*

## 一个配置本地DNS域名映射的简单样例

众所周知，Github国内登录缓慢，没钱买梯子或者不稳定的情况下想要浏览网页很是麻烦

一个简单的办法是配置本地的DNS域名，但是同样由于不稳定的原因，这种操作需要定期更新，很是麻烦，由此fastDns应运而生

基本原理：从http://tool.chinaz.com/dns/ 中获取域名的DNS ip，选择ttl最低的连接，然后选择修改本机hosts文件，最后刷新dns并测试稳定性，全程一体化操作，执行完毕后即可愉快畅游

同时，该fastDns.py可以重复执行，达到刷新的目的，也可以自动增加原本没有的域名dns，如raw.githubusercontent.com，以浏览readme中的图片

![Image text](https://github.com/CandleHouse/FastDNS/blob/master/example.png)
