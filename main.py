from tkinter import *
import requests
from requests.exceptions import RequestException
import re
import execjs
from urllib.parse import quote


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def gettkk(text):
    goolgeTransBaseUrl = "https://translate.google.cn/"
    baseResultHtml = get_one_page(goolgeTransBaseUrl)

    pattern = re.compile('(?<=tkk:\')(.*?)(?=\')', re.S)
    item = re.findall(pattern, baseResultHtml)

    jsstr = get_js()
    ctx = execjs.compile(jsstr)
    resultstr = ctx.call('tk', text, item[0])
    print(item[0])
    print(resultstr)

    fromLanguage = 'en'
    toLanguage = 'zh-CN'
    transurl = 'https://translate.google.cn/translate_a/single?client=t&sl=' \
               + fromLanguage + \
               '&tl=' \
               + toLanguage + \
               '&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&' \
               'ie=UTF-8&oe=UTF-8&source=btn&ssel=0&tsel=0&kc=0&tk='\
               + resultstr + '&q='\
               + quote(text)
    transresult = get_one_page(transurl)

    reslut = re.search('\[\[\["(.*?)"', transresult, re.S)

    text2.delete('1.0', 'end')
    text2.insert(INSERT, reslut.group(1))


def get_js():
# f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("gettk.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

def GoogleTranslate():
    gettkk(text.get(0.0, END))


root = Tk()
root.title('translate')

root.geometry('550x210+300+279')

Label(root, text='请输入翻译内容:').grid()

# Entry是可输入文本框
# url_input = Entry(root, font=("微软雅黑", 15), width=50)
# url_input.grid(row=0, column=1)

# 列表控件
text = Text(root, font=('微软雅黑', 15), width=20, height=5)
# columnspan 组件所跨越的列数
text.grid(row=1, columnspan=1)

# 设置按钮 sticky对齐方式，N S W E
button = Button(root, text='翻译', font=("微软雅黑", 15), command=GoogleTranslate).grid(row=1, column=1, sticky=W)

text2 = Text(root, font=('微软雅黑', 15), width=20, height=5)
# columnspan 组件所跨越的列数
text2.grid(row=1, column=2)

button = Button(root, text='退出', font=("微软雅黑", 15), command=root.quit).grid(row=2, column=1, sticky=E)

root.mainloop()
