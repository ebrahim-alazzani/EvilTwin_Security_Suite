#!/usr/bin/env python3
"""
=============================================================================
 EvilTwin Security Suite - Main Interactive CLI Entry Point
 Developed for Educational Research, Wireless Threat Analysis & Evil Twin Defense.
 Consolidated and upgraded from historical student project versions.
=============================================================================
"""

import sys
import os
import time
import socket
import platform

# Ensure local core package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.attacker import EvilTwinServer, get_banner
from core.detector import EvilTwinDetector

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_header():
    print(get_banner())
    print("=" * 75)
    print("  EvilTwin Security Suite | حزمة محاكاة واكتشاف هجمات التوأم الشرير")
    print("  مخصصة لأغراض التعليم والبحث الأمني وفحص شبكات الواي فاي")
    print("=" * 75)

def option_attacker():
    clear_screen()
    print("\n--- [1] تشغيل محاكي هجوم التوأم الشرير (Attacker Server) ---")
    port_input = input("أدخل رقم المنفذ (افتراضي 22222): ").strip()
    port = int(port_input) if port_input.isdigit() else 22222
    server = EvilTwinServer(port=port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
    input("\nاضغط Enter للعودة إلى القائمة الرئيسية...")

def option_detector():
    clear_screen()
    print("\n--- [2] تشغيل كاشف ومدافع الشبكات (Evil Twin Detector) ---")
    host_input = input("أدخل عنوان خادم المحاكاة (افتراضي 127.0.0.1): ").strip()
    port_input = input("أدخل رقم المنفذ (افتراضي 22222): ").strip()
    
    host = host_input if host_input else '127.0.0.1'
    port = int(port_input) if port_input.isdigit() else 22222
    
    detector = EvilTwinDetector(target_host=host, target_port=port)
    detector.run_scan_and_inspect()
    input("\nاضغط Enter للعودة إلى القائمة الرئيسية...")

def option_network_audit():
    clear_screen()
    print("\n--- [3] فحص وتحليل بطاقات ومحولات الشبكة الحالية ---")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"

    print(f"[*] اسم الجهاز (Hostname): {hostname}")
    print(f"[*] عنوان IP المحلي الرئيسي: {local_ip}")
    print(f"[*] نظام التشغيل: {platform.system()} {platform.release()}")

    try:
        import psutil
        print("\n[+] محولات وبطاقات الشبكة المكتشفة:")
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for iface, addr_list in addrs.items():
            stat = stats.get(iface)
            status_str = "متصل ✅" if (stat and stat.isup) else "غير متصل ❌"
            print(f"\n  • البطاقة: {iface} [{status_str}]")
            for a in addr_list:
                family = "IPv4" if a.family == socket.AF_INET else ("MAC" if hasattr(psutil, 'AF_LINK') and a.family == psutil.AF_LINK else str(a.family))
                print(f"    - {family}: {a.address}")
    except ImportError:
        print("[!] مكتبة psutil غير مثبتة للحصول على تفاصيل البطاقات كاملة.")

    input("\nاضغط Enter للعودة إلى القائمة الرئيسية...")

def option_view_logs():
    clear_screen()
    print("\n--- [4] استعراض سجلات جلسات الاتصال الملتقطة (Captured Logs) ---")
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_dir) or not os.listdir(log_dir):
        print("[-] لا توجد سجلات جلسات محفوظة حالياً.")
    else:
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log') or f.endswith('.txt')]
        print(f"[+] تم العثور على {len(log_files)} ملف سجل:\n")
        for idx, lf in enumerate(log_files, 1):
            fp = os.path.join(log_dir, lf)
            print(f"  {idx}. {lf} ({os.path.getsize(fp)} bytes)")
        
        choice = input("\nاختر رقم السجل لقراءته (أو Enter للعودة): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(log_files):
            chosen = log_files[int(choice) - 1]
            print(f"\n=== محتوى السجل: {chosen} ===")
            with open(os.path.join(log_dir, chosen), 'r', encoding='utf-8', errors='ignore') as f:
                print(f.read())
            print("=" * 45)

    input("\nاضغط Enter للعودة إلى القائمة الرئيسية...")

def option_docs():
    clear_screen()
    print("\n--- [5] الدليل والشرح الأكاديمي لمفهوم هجوم التوأم الشرير ---")
    print("""
1. ما هو هجوم التوأم الشرير (Evil Twin Attack)؟
   هو هجوم إلكتروني لاسلكي يقوم فيه المهاجم بإنشاء نقطة وصول واي فاي (Access Point) وهمية
   تحمل نفس الاسم (SSID) الخاص بشبكة شرعية موثوقة (مثل شبكة الشركة أو الفندق أو المقهى).

2. كيف يتم خداع الضحايا؟
   تقوم أجهزة المستخدمين بالاتصال تلقائياً بنقطة الوصول ذات الإشارة الأقوى أو الأقرب.
   بمجرد اتصال الضحية بنقطة الوصول المزيفة، يتمكن المهاجم من اعتراض وتفتيش البيانات
   غير المشفرة (Man-in-the-Middle) وسرقة بيانات الدخول.

3. كيف يعمل كاشف التوأم الشرير (Detection Mechanism)؟
   - فحص عناوين BSSID (عنوان MAC الفعلي للروتر).
   - إذا تم اكتشاف شبكتين أو أكثر لهما نفس الـ SSID ولكن بعناوين MAC مختلفة وبقوة إشارة غير متطابقة،
     يتم إطلاق تنبيه أمني فوري للتحذير من الاتصال.

4. النسخ التاريخية المؤرشفة:
   تم حفظ وتحليل النسخ الـ 8 للمشروع داخل مجلد 'archive_versions/' مع توثيق الفروق.
""")
    input("\nاضغط Enter للعودة إلى القائمة الرئيسية...")

def main():
    while True:
        clear_screen()
        display_header()
        print("\n  القائمة الرئيسية:")
        print("  [1] 🚀 تشغيل سيرفر محاكاة هجوم التوأم الشرير (Attacker Server)")
        print("  [2] 🛡️ تشغيل فاحص وكاشف الشبكات الوهمية (Evil Twin Detector)")
        print("  [3] 🔍 فحص بطاقات الشبكة وتفاصيل الاتصال (Network Audit)")
        print("  [4] 📂 عرض سجلات جلسات الاتصال الملتقطة (Captured Logs)")
        print("  [5] 📚 الدليل والشرح الأكاديمي والتوثيق (Educational Guide)")
        print("  [6] ❌ خروج (Exit)")
        print("-" * 75)

        choice = input("اختر رقم الخيار [1-6]: ").strip()
        if choice == '1':
            option_attacker()
        elif choice == '2':
            option_detector()
        elif choice == '3':
            option_network_audit()
        elif choice == '4':
            option_view_logs()
        elif choice == '5':
            option_docs()
        elif choice == '6':
            clear_screen()
            print("\nشكراً لاستخدامك EvilTwin Security Suite. وداعاً!\n")
            sys.exit(0)
        else:
            print("خيار غير صالح، يرجى المحاولة مرة أخرى.")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nتم إنهاء البرنامج.")
        sys.exit(0)
