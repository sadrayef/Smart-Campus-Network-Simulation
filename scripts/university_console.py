"""
University Network Management Console  (No-Input / Edit-and-Run version)
"""

import time

# ---------------------------------------------------------------------
# اطلاعات سرویس‌ها: (نام نمایشی، آدرس IP)
# ---------------------------------------------------------------------
SERVICES = {
    "1": ("DNS Server",         "10.10.4.11"),
    "2": ("Web Server",         "10.10.4.13"),
    "3": ("Mail Server (SMTP)", "10.10.4.12"),
    "4": ("File Server (FTP)",  "10.10.4.14"),
}

# ---------------------------------------------------------------------
# نتیجه‌ی تست دستی هر سرویس را همین‌جا وارد کنید:
# True  = سرویس پاسخ داد (پینگ موفق بود / صفحه باز شد / ...)
# False = سرویس پاسخ نداد (Timeout / خطا)
#
# مثال: اگر با ping 10.10.4.13 پاسخ گرفتید، مقدار "2" را True بگذارید.
# ---------------------------------------------------------------------
SERVICE_STATUS = {
    "1": True,    # DNS Server
    "2": True,    # Web Server
    "3": True,    # Mail Server
    "4": True,    # File Server
}


def print_menu():
    print("=" * 60)
    print("     University Network Management Console")
    print("=" * 60)
    for key in sorted(SERVICES.keys()):
        name, ip = SERVICES[key]
        print("  {}) {}   ({})".format(key, name, ip))
    print("=" * 60)


def check_service(key):
    if key not in SERVICES:
        print("[خطا] سرویسی با شماره‌ی {} تعریف نشده است.".format(key))
        return False, None, None, None

    name, ip = SERVICES[key]

    if key not in SERVICE_STATUS:
        status, message = "Unknown", "وضعیت این سرویس در SERVICE_STATUS ثبت نشده."
        return False, name, ip, (status, message)

    is_online = SERVICE_STATUS[key]
    if is_online:
        status, message = "Online", "Success - سرویس در دسترس است."
    else:
        status, message = "Offline", "Failed - سرویس در دسترس نیست یا Timeout داد."

    return True, name, ip, (status, message)


def check_all_services():
    print("\n===== بررسی وضعیت همه‌ی سرویس‌ها =====\n")
    results = []

    for key in sorted(SERVICES.keys()):
        ok, name, ip, result = check_service(key)
        if not ok or result is None:
            continue
        status, message = result
        results.append((name, ip, status, message))
        print("{:<22} {:<14} -> {:<8} ({})".format(name, ip, status, message))
        time.sleep(0.2)

    return results


def print_summary_report(results):
    print("\n" + "=" * 60)
    print("            گزارش کلی وضعیت سرویس‌های شبکه دانشگاه")
    print("=" * 60)

    total = len(results)
    online_count = 0
    for name, ip, status, message in results:
        if status == "Online":
            online_count += 1

    print("تعداد سرویس‌های Online: {} از {}".format(online_count, total))

    if total == 0:
        overall = "نامشخص - هیچ سرویسی بررسی نشد."
    elif online_count == total:
        overall = "SUCCESS - همه‌ی سرویس‌ها فعال هستند."
    elif online_count == 0:
        overall = "FAILED - هیچ سرویسی در دسترس نیست!"
    else:
        overall = "WARNING - برخی سرویس‌ها در دسترس نیستند."

    print("وضعیت کلی شبکه: {}".format(overall))
    print("=" * 60)


def main():
    print("در حال بارگذاری کنسول مدیریت شبکه دانشگاه ...")
    time.sleep(1)

    print_menu()
    results = check_all_services()
    print_summary_report(results)

    print("\n[راهنما] برای تست دوباره با وضعیت جدید، مقادیر دیکشنری")
    print("SERVICE_STATUS در ابتدای فایل را تغییر دهید و دوباره Run بزنید.")
    print("(مثلاً برای شبیه‌سازی خرابی Web Server، مقدار \"2\" را False کنید.)")


main()