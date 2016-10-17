# coding: utf-8

# bot.py - A Simple Telegram Bot
# Using python3 for Unicode support

# Version: 0.9.2
# Final Check: 2016.10.17 15:11:00
# Update Log:
# 1. Bug Fixed in Moe
# 2. Timer allow inputs like '13:02'

import telepot
import requests
import time
from threading import Thread
from base64 import b64encode, b64decode
from urllib.parse import quote, unquote
from pyquery import PyQuery as pq

# bot 的配置信息

token = '***** PUT YOUR TOKEN HERE *****'
admin = 123456789
username = '@your_bot'

bot = telepot.Bot(token)

# bot 信息处理流程

def handle(msg):
    content_type, chat_type, chat_id, date, msg_id = telepot.glance(msg,'chat',True)
    chat_id = int(chat_id)
    print(content_type, chat_type, chat_id, date, msg_id)
    # 文本信息处理
    if content_type == 'text':
        cmd = msg['text']
        if cmd.startswith('/'): 
            # 基础命令
            if cmd.startswith('/start'): 
                bot_welcome(chat_id)
            elif cmd.startswith('/help'):
                bot_help(chat_id)
            elif cmd.startswith('/about'):
                bot_about(chat_id)
            # 功能命令
            elif cmd.startswith('/baidu'):
                baidu(cmd, chat_id)
            elif cmd.startswith('/b64en'):
                b64en(cmd, chat_id)
            elif cmd.startswith('/b64de'):
                b64de(cmd, chat_id)
            elif cmd.startswith('/math'):
                math(cmd, chat_id)
            elif cmd.startswith('/moe'):
                moe(cmd, chat_id)
            elif cmd.startswith('/panc'):
                panc(cmd, chat_id)
            elif cmd.startswith('/qrcode'):
                qrcode(cmd, chat_id)
            elif cmd.startswith('/stack'):
                stack(cmd, chat_id)
            elif cmd.startswith('/timer'):
                # 使用子进程实现计时器
                t1 = Thread(target=timer, args=(cmd, chat_id))
                t1.start()
            elif cmd.startswith('/urlen'):
                urlen(cmd, chat_id)
            elif cmd.startswith('/urlde'):
                urlde(cmd, chat_id)
            elif cmd.startswith('/wikien'):
                wiki('en', cmd, chat_id)
            elif cmd.startswith('/wikizh'):
                wiki('zh', cmd, chat_id)
            # Admin 命令
            elif chat_id == admin:
                if cmd.startswith('/get'):
                    get_msg(cmd)
                elif cmd.startswith('/reply'):
                    reply_msg(cmd)
                elif cmd.startswith('/send'):
                    send_msg(cmd)
            # 命令无法识别，返回错误信息
            else:
                bot_error(chat_id)
        # 纯文本
        else:     
            if chat_id != admin:
                bot.forwardMessage(admin,chat_id,msg_id)
                bot.sendMessage(admin, chat_id)
    # 其他类型信息
    else: 
        bot.sendMessage(admin, '%s,%d %s'%(content_type, chat_id, msg_id))
        if content_type == 'sticker' and chat_id != admin:
            bot.forwardMessage(admin,chat_id,msg_id)

# Bot 基本信息输出

# 欢迎语

def bot_welcome(chat_id):
    welcome_msg = '欢迎光临三只熊漫画书店！'
    bot.sendMessage(chat_id, welcome_msg)

# 帮助信息

def bot_help(chat_id):
    help_msg = '''熊骑士命令帮助：\n
    /baidu    使用百度搜索
    /b64en    Base64 编码
    /b64de    Base64 解码
    /math     简单的数学计算
    /moe      萌娘百科搜索（测试中）
    /panc     胖次网盘搜索（测试中）
    /qrcode   生成二维码
    /stack    Stack Overflow 搜索
    /timer    计时器（输入整分钟，测试中）
    /urlen    URL 编码
    /urlde    URL 解码
    /wikien   搜索英文维基百科
    /wikizh   搜索中文维基百科\n
    还有什么需要熊骑士帮忙的吗？
    '''
    bot.sendMessage(chat_id, help_msg)

# 关于

def bot_about(chat_id):
    about_msg = '版本：0.9.2 ，<a href="https://github.com/kurubot/kuuma_bot">查看源码</a> 。'
    bot.sendMessage(chat_id, about_msg, parse_mode='HTML')

# 错误信息

def bot_error(chat_id):
    error_msg = '熊骑士好像不明白……'
    bot.sendMessage(chat_id, error_msg)

# 命令预处理

def parse_cmd(cmd, func):
    return cmd.lstrip(func).lstrip(username).strip(' ').replace('\n','')

# Bot 功能命令

# 百度搜索
# 由于 Markdown 模式输出可能出现语法冲突，全部改为 HTML 模式

def baidu(cmd, chat_id):
    query = parse_cmd(cmd, '/baidu')
    # 判断内容是否为空
    if query:
        query = quote(query)
        link = 'http://www.baidu.com/s?wd=%s&pn=0&rn=5&tn=json' % query
        try:
            result = requests.get(link).json()
            data_list = result['feed']['entry']
            num = len(data_list)
            if num > 5:
                num = 5
            message = '搜索结果：\n\n'    
            for i in range(num):
                message += '%d. <a href="%s">%s</a>\n' % (i+1, data_list[i]['url'], data_list[i]['title'])
                message += '%s\n\n' % data_list[i]['abs']
            bot.sendMessage(chat_id, message, parse_mode='HTML')
        except:
            bot.sendMessage(chat_id, '搜索失败。')
    else:
        bot_error(chat_id)

# Base64 编码
# 注意 b64encode, b64decode 操作对象和输出对象都是编码后的二进制字符串（而不是 Unicode 字符串），所以使用前请先 encode，使用后要 decode

def b64en(cmd, chat_id):
    command = parse_cmd(cmd, '/b64en')
    if command:
        command = command.encode('utf-8')
        try:
            result = b64encode(command).decode('utf-8')
            bot.sendMessage(chat_id, 'Base64 编码结果：%s' % result)
        except:
            bot.sendMessage(chat_id, 'Base64 编码失败。')
    else:
        bot_error(chat_id)

# Base64 解码
# 虽然这里不 encode 也能得到正确的结果 = =

def b64de(cmd, chat_id):
    command = parse_cmd(cmd, '/b64de')
    if command:
        # 等号补全（比如 shadowsocks-android ）
        missing = len(command) % 4
        if missing:
            command += '=' * (4 - missing)
        try:
            result = b64decode(command.encode('utf-8')).decode('utf-8')
            bot.sendMessage(chat_id, 'Base64 解码结果: %s' % result)
        except:
            bot.sendMessage(chat_id, 'Base64 解码失败。')
    else:
        bot_error(chat_id)

# Mathjs

def math(cmd, chat_id):
    command = parse_cmd(cmd, '/math')
    if command:
        command = quote(command)
        try:
            result = requests.get('http://api.mathjs.org/v1/?expr=%s' % command)
            bot.sendMessage(chat_id, result.text)
        except:
            bot.sendMessage(chat_id, '计算失败。')
    else:
        bot_error(chat_id)

# 萌娘百科搜索（测试）

def moe(cmd, chat_id):
    command = parse_cmd(cmd, '/moe')
    if command:
        command = quote(command)
        link = 'https://zh.moegirl.org/index.php?search=%s&fulltext=Search' % command
        try:
            req = pq(url=link)
            # 结果抓取
            search_result = req.find('.mw-search-results')
            links = search_result.find('.mw-search-result-heading>a')
            abs = search_result.find('.searchresult')
            # 格式化输出
            titles = [i.text().replace(' ','') for i in links.items()]
            urls = ['https://zh.moegirl.org'+i.attr('href') for i in links.items()]
            preview = [i.text()+'...' for i in abs.items()]
            message = '搜索结果：\n\n'
            num = len(urls)
            if num > 5:
                num = 5
            for i in range(num):
                message += '%d. <a href="%s">%s</a>\n' % (i+1, urls[i], titles[i])
                message += '%s\n\n' % preview[i]
            bot.sendMessage(chat_id, message, parse_mode='HTML')
        except:
            bot.sendMessage(chat_id, '搜索失败。')
    else:
        bot_error(chat_id)

# 胖次网盘搜索（测试）

def panc(cmd, chat_id):
    command = parse_cmd(cmd, '/panc')
    if command:
        command = quote(command)
        link = 'https://www.panc.cc/s/%s/' % command
        try:
            req = pq(url=link)
            search_result = req.find('#search_result')
            # 查找标题
            titles = search_result.find('.b_title')
            titles_text = [i.text().replace(' ','') for i in titles.items()] 
            # 查找链接
            urls = search_result.find('.a_url')
            urls_href = [i.attr('href') for i in urls.items()]
            # 输出结果
            num = len(urls_href)
            message = '搜索结果：\n\n'
            for i in range(num):
                message += '%d. <a href="%s">%s</a>\n\n' % (i+1, urls_href[i], titles_text[i])
            bot.sendMessage(chat_id, message, parse_mode='HTML')
        except:
            bot.sendMessage(chat_id, '搜索失败。')
    else:
        bot_error(chat_id)

# 二维码

def qrcode(cmd, chat_id):
    command = parse_cmd(cmd, '/qrcode')
    if command:
        command = quote(command)
        bot.sendMessage(chat_id, 'https://zxing.org/w/chart?cht=qr&chs=350x350&chld=L&choe=UTF-8&chl=%s' % command)
    else:
        bot_error(chat_id)

# Stack Overflow 搜索

def stack(cmd, chat_id):
    command = parse_cmd(cmd, '/stack')
    if command:
        command = quote(command)
        link = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=%s&accepted=True&site=stackoverflow&filter=!-MOiNm40F1YTH5WjEK.BGQ_jCyid6o_27' % command
        try:
            result = requests.get(link).json()
            data = result['items']
            num = len(data)
            if num > 5:
                num = 5
            message = '搜索结果：\n\n'
            for i in range(num):
                message += '%d. <a href="%s">%s</a>\n' % (i+1, data[i]['link'], data[i]['title'])
            bot.sendMessage(chat_id, message, parse_mode='HTML')
        except:
            bot.sendMessage(chat_id, '搜索失败。')
    else:
        bot_error(chat_id)

# Timer 计时器（测试中）

def timer(cmd, chat_id):
    command = parse_cmd(cmd, '/timer')
    if command:
        try:
            if ':' in command:
                [hours, minutes] = command.split(':')
                # 处理输入
                hours = int(hours)
                if not hours in range(0,24):
                    bot.sendMessage(chat_id, '请使用 24 小时时制~')
                    return
                minutes = int(minutes)
                if not minutes in range(0,60):
                    bot.sendMessage(chat_id, '分钟格式输入有误~')
                    return
                # 处理小时部分
                sys_hours = time.localtime(time.time()).tm_hour
                hours = hours - sys_hours
                if hours < 0:
                    hours += 24
                # 处理分钟部分
                sys_minutes = time.localtime(time.time()).tm_min
                minutes = minutes + hours * 60 - sys_minutes - 1
                seconds = 60 - time.localtime(time.time()).tm_sec
            else:
                minutes = int(command)
                seconds = 0
            if not minutes in range(0,720):
                bot.sendMessage(chat_id, '请输入 0 到 720 间的整数~')
                return
            if seconds:
                bot.sendMessage(chat_id, '闹钟设好啦~ 熊骑士会在 %s 提醒你的哦~' % command)
            else:
                bot.sendMessage(chat_id, '定时器设好啦~ %d 分钟后熊骑士会提醒你的哦~' %     minutes)
            time.sleep(minutes * 60 + seconds)
            bot.sendMessage(chat_id, '时间到啦！')
        except:
            bot.sendMessage(chat_id, '出错啦！')
    else:
        bot_error(chat_id)

# URL 编码

def urlen(cmd, chat_id):
    command = parse_cmd(cmd, '/urlen')
    if command:
        try:
            command = quote(command)
            bot.sendMessage(chat_id, 'URL 编码结果：%s' % command)
        except:
            bot.sendMessage(chat_id, 'URL 编码失败。')
    else:
        bot_error(chat_id)

# URL 解码

def urlde(cmd, chat_id):
    command = parse_cmd(cmd, '/urlde')
    if command:
        try:
            command = unquote(command)
            bot.sendMessage(chat_id, 'URL 解码结果：%s' % command)
        except:
            bot.sendMessage(chat_id, 'URL 解码失败。')
    else:
        bot_error(chat_id)

# 维基百科搜索

def wiki(lang, cmd, chat_id):
    command = parse_cmd(cmd, '/wiki%s' % lang)
    if command:
        command = quote(command)
        link = 'https://%s.wikipedia.org/w/api.php?action=opensearch&format=json&search=%s&namespace=0&limit=5' % (lang, command)
        try:
            result = requests.get(link).json()
            num = len(result[1])
            message = '搜索结果：\n\n'
            for i in range(num):
                message += '%d. <a href="%s">%s</a>\n' % (i+1, result[3][i], result[1][i])
                message += '%s\n\n' % result[2][i]
            bot.sendMessage(chat_id, message, parse_mode='HTML')
        except:
            bot.sendMessage(chat_id, '搜索失败。')
    else:
        bot_error(chat_id)

# Admin 命令：获取信息

def get_msg(cmd):
    try:
        from_chat_id, message_id = cmd.lstrip('/get').strip(' ').split(' ')
        from_chat_id = int(from_chat_id)
        message_id = int(message_id)
        bot.forwardMessage(admin, from_chat_id, message_id)
    except:
        bot.sendMessage(admin, '获取信息失败。')

# Admin 命令：回复信息

def reply_msg(cmd):
    try: 
        reply_id, message = cmd.lstrip('/reply').strip(' ').split(' ')
        reply_id = int(reply_id)
        bot.sendMessage(reply_id, message)
    except:
        bot.sendMessage(admin, '回复信息失败。')

# admin 命令：转发信息

def send_msg(cmd):
    try:
        reply_id, message_id = cmd.lstrip('/send').strip(' ').split(' ')
        reply_id = int(reply_id)
        message_id = int(message_id)
        bot.forwardMessage(reply_id, admin, message_id)
    except:
        bot.sendMessage(admin, '转发信息失败。')

# bot 开始运行

bot.message_loop(handle)

print('Listening...')

# Keep Running

while 1:
    time.sleep(10)