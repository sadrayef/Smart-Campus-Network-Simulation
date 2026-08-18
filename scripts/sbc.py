

from tcp import *
from http import *
from time import *

RUN_MODE = "scan"      # "scan" یا "pick"
PICK_ID = 1             # شماره‌ی سرویسی که در حالت "pick" بررسی می‌شود

TCP_GRACE = 2           # ثانیه‌های انتظار برای پایدار شدن handshake ناهمگام TCP
NAME_GRACE = 5          # ثانیه‌های انتظار برای پاسخ Name Resolution

# هر سطر شامل: برچسب، نوع، آدرس، پورت
#   نوع "port" -> بررسی دسترسی خام TCP به host:port
#   نوع "name" -> تایید Resolve شدن DNS از طریق یک درخواست HTTP
CATALOG = [
    ("سرور وب (HTTP/80)",                          "port", "10.10.4.13", 80),
    ("سرور ایمیل SMTP (25)",                        "port", "10.10.4.12", 25),
    ("سرور فایل FTP (21)",                          "port", "10.10.4.14", 21),
    ("جستجوی نام / سلامت DNS (www.university.edu)", "name", "http://www.university.edu", 0),
]

# وضعیت مشترک با callback ناهمگام HTTP
_reply_in = False
_reply_ok = False


def _http_reply(status, data):
    global _reply_in, _reply_ok
    _reply_in = True
    _reply_ok = (status == 200)


def probe_name(url):
    global _reply_in, _reply_ok
    _reply_in = False
    _reply_ok = False

    agent = HTTPClient()
    agent.onDone(_http_reply)
    try:
        agent.open(url)
    except:
        return False

    spent = 0
    while (not _reply_in) and (spent < NAME_GRACE):
        sleep(0.5)
        spent = spent + 0.5

    try:
        agent.stop()
    except:
        pass

    return _reply_ok


def probe_port(host, port):
    sock = TCPClient()
    alive = False
    try:
        sock.connect(host, port)
        sleep(TCP_GRACE)  # connect() ناهمگام است: صبر کن، بعد وضعیت را بخوان
        alive = sock.connected()
    except:
        alive = False
    try:
        sock.close()
    except:
        pass
    return alive


def evaluate(row):
    label, kind, address, port = row
    if kind == "name":
        return probe_name(address)
    return probe_port(address, port)


LINE_WIDTH = 46
LABEL_WIDTH = 34


def _line(ch="─"):
    print(ch * LINE_WIDTH)


def render(label, alive):
    dots = LABEL_WIDTH - len(label)
    if dots < 1:
        dots = 1
    padded = label + (" " + "." * dots)
    if alive:
        print("  " + padded + " متصل   ✓")
    else:
        print("  " + padded + " قطع    ✗")


def banner():
    print("╔" + "═" * LINE_WIDTH + "╗")
    title = "پایش وضعیت سرور های مرکز داده دانشگاه"
    pad = LINE_WIDTH - len(title)
    left = pad // 2
    right = pad - left
    print("║" + (" " * left) + title + (" " * right) + "║")
    print("╚" + "═" * LINE_WIDTH + "╝")


def scan_all():
    banner()
    print()
    live = 0
    for row in CATALOG:
        ok = evaluate(row)
        if ok:
            live = live + 1
        render(row[0], ok)

    total = len(CATALOG)
    percent = int((live * 100) / total)

    print()
    _line()
    print("  جمع‌بندی : " + str(live) + " از " + str(total) + " سرویس فعال (" + str(percent) + "٪)")

    if live == total:
        print("  وضعیت    : 🟢 سالم — همه‌ی سرویس‌ها در دسترس‌اند")
    elif live == 0:
        print("  وضعیت    : 🔴 بحرانی — مرکز داده کاملاً از دسترس خارج شده")
    else:
        print("  وضعیت    : 🟡 هشدار — قطعی جزئی در برخی سرویس‌ها")
    _line("═")


def scan_one(idx):
    if idx < 1 or idx > len(CATALOG):
        print("⚠  مقدار PICK_ID خارج از محدوده‌ی کاتالوگ است.")
        return
    banner()
    print()
    row = CATALOG[idx - 1]
    render(row[0], evaluate(row))
    _line("═")


# ---- نقطه‌ی شروع اجرا -----------------------------------------
if RUN_MODE == "scan":
    scan_all()
elif RUN_MODE == "pick":
    scan_one(PICK_ID)
else:
    print('⚠  مقدار RUN_MODE باید "scan" یا "pick" باشد.')