import requests
import openpyxl
import json
import prettytable as pt
import time
import os

# 自动切换工作路径，使得直接用python命令行执行.py文件时，能正确查找到xlsx文件
current_path = os.path.dirname(__file__)
os.chdir(current_path)

data_xlsx = openpyxl.load_workbook('dnsSearch.xlsx')
sheet = data_xlsx['Sheet1']


def get_dns(domain_name):
    min = 10000
    dict = {}
    for i in range(10):
        # 提取请求头
        url_index = 'F' + repr(i + 2)
        url = sheet[url_index].value
        # 构造post体，Form_data内容
        process_index = 'D' + repr(i + 2)
        right_index = 'E' + repr(i + 2)
        Form_data = {
            'host': domain_name,
            'type': '1',
            'total': '10',
            'process': sheet[process_index].value,
            'right': sheet[right_index].value
        }
        # post发送请求
        response = requests.post(url, data=Form_data)
        dns_index = 'B' + repr(i + 2)
        print("尝试连接DNS所在地：\t" + sheet[dns_index].value, "\t返回值：" + response.text)

        string = response.text
        if string[10] == '1':
            str = json.loads(string[1: len(string) - 1])
            if str['list']:
                current = int(str['list'][0]['ttl'])
                if current < min:
                    min = current
                    dict['DNS所在地'] = sheet[dns_index].value
                    dict['result'] = str['list'][0]['result']
                    dict['ipaddress'] = str['list'][0]['ipaddress']
                    dict['TTL值'] = str['list'][0]['ttl']
    print("\n当前最佳结果：")
    tb = pt.PrettyTable()
    tb.field_names = ["DNS所在地", "result", "ipaddress", "TTL值"]
    tb.add_row([dict['DNS所在地'], dict['result'], dict['ipaddress'], dict['TTL值']])
    print(tb)
    return dict


def mod_host(new_dns, domain_name):
    with open("C:\Windows\System32\drivers\etc\hosts", "r+", encoding='utf-8') as f:
        flist = f.readlines()
        flag = 0
    for i, content in enumerate(flist):
        # 可将文件中所有相同域名的行都变成同一个值
        if domain_name in content:
            flist[i] = new_dns + " " + domain_name + "\n"
            flag = 1
    # 去除21行以后的重复元素，相当于变相删除了原始host中多个重复值
    flist[20:] = sorted(set(flist[20:]), key=flist[20:].index)
    # 当之前的搜索未执行替换时，才添加新的域名
    if not flag:
        # 当最后一个元素不具有回车时，添加回车，否则会导致粘连，使得二次执行时直接删除第一次的最后一行
        if '\n' not in flist[-1]:
            flist[-1] += '\n'
        flist.append(new_dns + " " + domain_name + "\n")
    with open("C:\Windows\System32\drivers\etc\hosts", "w+", encoding='utf-8') as file:
        file.writelines(flist)


if __name__ == '__main__':
    start = time.time()
    domain_name = input('请输入域名：')
    # 获取当前最佳dns
    ip_dict = get_dns(domain_name)
    choose = input('\n是否修改host文件？[y/n]')
    if choose == ('y' or 'Y'):
        print('\nDNS所在地已迁移:' + ip_dict['DNS所在地'], '响应IP:' + ip_dict['result'] + '[' + ip_dict['ipaddress'] + ']')
        # 按照获得的dns和域名，修改host文件
        mod_host(ip_dict['result'], domain_name)
        # 刷新
        cmd = 'ipconfig/flushdns'
        os.system(cmd)
        cmd = 'ping github.com'
        os.system(cmd)
    elif choose == ('n' or 'N'):
        print("\n已终止操作")
    end = time.time()
    print("\n--------------------------------")
    print("Process exited after " + format((end - start), '.3f') + " seconds with return value 0")
    temps = input("请按任意键继续. . .")