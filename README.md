# kuuma_bot

A simple Telegram bot, written in Python 3. 

[Try it](https://telegram.me/kuuma_bot)

Version: 0.9.8

## Warning

I just learnt Python a few hours and my code is awful...

## Update Log

### v0.9.8

Add `/music`. Thanks to [go-music](https://github.com/loadfield/go-music/)!

### v0.9.7 Happy New Year!

1. Add `/zhihu` (Experimental).
2. Add Unicode Conversion `/unien` and `unide`.

### v0.9.5

1. Add `/google` (Experimental).
2. Bug Fixed (HTML Escape).

### v0.9.4

1. Bug fixed.
2. Add `/server` for Admin. 

If no issues, `v0.9.4` will be the final version of kuuma_bot.

### v0.9.3

1. `/qrcode` modify for Shadowsocks-Android URLs.
2. `/timer` with memos.

### v0.9.2

1. Bug fixed in `/moe`.
2. `/timer` can set alarms, too!

## Dependency

```bash
pip3 install telepot
pip3 install requests
pip3 install pyquery
```

## Feature

* Base64 Encode / Decode
* URL Encode / Decode
* Search in Baidu
* Search in Wikipedia
* Search in Stack Overflow
* Generate QR Codes (Using Zxing Generator)
* Simple Math Cal Using http://api.mathjs.org
* Timer and Alarm
* ...

## Bug

Make a thread for timer, which takes much virtual memory.

## License

MIT
