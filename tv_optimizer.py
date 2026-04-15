import os
import socket
import logging
import threading
import concurrent.futures
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_cryptography import CryptographySigner
from adb_shell.auth.keygen import keygen

# ---------------------------------------------------------
# 1. إعداد نظام تحويل السجلات للواجهة الرسومية (GUI Logger)
# ---------------------------------------------------------
class TextHandler(logging.Handler):
    """محول مخصص لإرسال مخرجات الـ Logging إلى عنصر Text في Tkinter"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

# ---------------------------------------------------------
# 2. الفئة الرئيسية لأداة التحسين (Optimizer Class)
# ---------------------------------------------------------
class XiaomiOptimizer:
    def __init__(self, ip_address: str, port: int = 5555, key_path: str = 'adbkey'):
        self.ip_address = ip_address
        self.port = port
        self.key_path = key_path
        self.device = AdbDeviceTcp(self.ip_address, self.port)
        self.is_connected = False
        self.logger = logging.getLogger("AndroidTV_Optimizer")

    def _get_signer(self) -> CryptographySigner:
        if not os.path.exists(self.key_path):
            self.logger.info("🔑 جاري توليد مفاتيح مصادقة جديدة (RSA Keys)...")
            keygen(self.key_path)
        return CryptographySigner(self.key_path)

    def connect(self) -> None:
        self.logger.info(f"📡 جاري محاولة الاتصال بالجهاز: {self.ip_address}:{self.port}...")
        try:
            signer = self._get_signer()
            self.device.connect(rsa_keys=[signer], transport_timeout_s=15)
            self.is_connected = True
            self.logger.info("✅ تم الاتصال والمصادقة بنجاح!")
        except Exception as e:
            self.logger.error(f"❌ فشل الاتصال. تأكد من عمل الجهاز والشبكة.")
            raise

    def execute_commands(self, commands: List[str], description: str) -> None:
        if not self.is_connected:
            return
        self.logger.info(f"⚙️ بدء تنفيذ: {description}...")
        for cmd in commands:
            try:
                self.device.shell(cmd)
            except Exception as e:
                self.logger.warning(f"⚠️ فشل تنفيذ الأمر ({cmd})")

    def disconnect(self) -> None:
        if self.is_connected:
            self.device.close()
            self.logger.info("🔌 تم إغلاق الاتصال بالجهاز بأمان.")

# ---------------------------------------------------------
# 3. واجهة المستخدم الرسومية (GUI App)
# ---------------------------------------------------------
class OptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Android TV Ultimate Optimizer")
        self.root.geometry("750x750")
        self.root.configure(padx=20, pady=20)
        
        self.var_ui = tk.BooleanVar(value=True)
        self.var_ram = tk.BooleanVar(value=True)
        self.var_net = tk.BooleanVar(value=True)
        self.var_bloat = tk.BooleanVar(value=True)
        self.var_mic_disable = tk.BooleanVar(value=True)
        self.var_cache = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.setup_logging()

    def setup_ui(self):
        title_label = ttk.Label(self.root, text="🚀 أداة تسريع الشاومي ستيك و Android TV", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 15))

        # --- قسم الشبكة والـ IP ---
        network_frame = ttk.LabelFrame(self.root, text=" الاتصال والجهاز ")
        network_frame.pack(fill=tk.X, pady=5, ipadx=10, ipady=10)

        ttk.Label(network_frame, text="عنوان الـ IP:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5, pady=5)
        
        # تحويل الإدخال إلى Combobox ليدعم الكتابة اليدوية أو اختيار الأجهزة المكتشفة
        self.ip_combo = ttk.Combobox(network_frame, font=("Helvetica", 12), width=18)
        self.ip_combo.insert(0, "192.168.100.45")
        self.ip_combo.grid(row=0, column=1, padx=5, pady=5)

        self.scan_btn = ttk.Button(network_frame, text="🔍 اكتشاف الأجهزة في الشبكة", command=self.start_network_scan)
        self.scan_btn.grid(row=0, column=2, padx=10, pady=5)

        # --- قسم خيارات التحسين (Checkboxes) ---
        options_frame = ttk.LabelFrame(self.root, text=" حدد المميزات المراد تفعيلها (جميعها مفعلة افتراضياً) ")
        options_frame.pack(fill=tk.X, pady=10, ipadx=10, ipady=10)

        ttk.Checkbutton(options_frame, text="تسريع الواجهة والأنيميشن (لجعل التنقل بين القوائم أسرع وتقليل التقطيع)", variable=self.var_ui).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="تحسين إدارة الرام (الحد من العمليات في الخلفية لمنع تعليق الجهاز)", variable=self.var_ram).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="تسريع حزم الإنترنت (لتقليل التقطيع أثناء مشاهدة البث والمحتوى)", variable=self.var_net).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="إيقاف خدمات شاومي الثقيلة (إيقاف الإعلانات والتتبع التابع لشاومي فقط)", variable=self.var_bloat).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="إيقاف مساعد جوجل والبحث الصوتي - katniss (أزل الصح إذا أردت أن يعمل المايك)", variable=self.var_mic_disable).pack(anchor=tk.W, pady=3)
        ttk.Checkbutton(options_frame, text="تنظيف عميق للذاكرة المؤقتة (تفريغ الكاش لتوفير مساحة التخزين)", variable=self.var_cache).pack(anchor=tk.W, pady=3)

        # --- أزرار الإجراءات ---
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill=tk.X, pady=10)

        self.start_btn = ttk.Button(action_frame, text="⚡ بدء تنفيذ التحسينات", command=self.start_optimization)
        self.start_btn.pack(side=tk.RIGHT, padx=5, ipadx=10)

        self.reset_btn = ttk.Button(action_frame, text="🔄 استعادة ضبط المصنع (إلغاء التحسينات)", command=self.start_reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5, ipadx=10)

        # --- شاشة العرض ---
        console_frame = ttk.LabelFrame(self.root, text=" شاشة العمليات (Console) ")
        console_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.console_text = tk.Text(console_frame, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10), state='disabled', wrap='word')
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_logging(self):
        self.logger = logging.getLogger("AndroidTV_Optimizer")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            text_handler = TextHandler(self.console_text)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
            text_handler.setFormatter(formatter)
            self.logger.addHandler(text_handler)

    # --- دوال اكتشاف الأجهزة ---
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def scan_port(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((ip, 5555))
        sock.close()
        return result == 0

    def network_scan_task(self):
        self.logger.info("🔍 جاري فحص الشبكة المحلية للبحث عن أجهزة Android TV (المنفذ 5555)...")
        local_ip = self.get_local_ip()
        base_ip = local_ip.rsplit('.', 1)[0] + '.'
        ips_to_scan = [base_ip + str(i) for i in range(1, 255)]
        
        discovered_devices = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {executor.submit(self.scan_port, ip): ip for ip in ips_to_scan}
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                if future.result():
                    discovered_devices.append(ip)

        if discovered_devices:
            self.logger.info(f"🎯 تم العثور على أجهزة: {', '.join(discovered_devices)}")
            # تحديث القائمة المنسدلة
            self.root.after(0, lambda: self.ip_combo.config(values=discovered_devices))
            self.root.after(0, lambda: self.ip_combo.set(discovered_devices[0]))
        else:
            self.logger.warning("⚠️ لم يتم العثور على أجهزة تدعم ADB في الشبكة. تأكد من تفعيل وضع المطورين.")
        
        self.root.after(0, self.enable_buttons)

    def start_network_scan(self):
        self.clear_console()
        self.disable_buttons()
        threading.Thread(target=self.network_scan_task, daemon=True).start()

    # --- دوال التحسين والاستعادة ---
    def run_optimization_task(self, target_ip, selections):
        UI_TWEAKS = ["settings put global window_animation_scale 0", "settings put global transition_animation_scale 0", "settings put global animator_duration_scale 0", "setprop persist.sys.ui.hw 1", "setprop debug.hwui.renderer opengl"]
        RAM_TWEAKS = ["settings put global activity_manager_max_running_operations 1", "setprop dalvik.vm.heapsize 128m", "setprop dalvik.vm.heapgrowthlimit 64m"]
        NETWORK_TWEAKS = ["setprop net.tcp.buffersize.default 4096,87380,256960,4096,16384,256960", "setprop net.tcp.buffersize.wifi 4096,87380,256960,4096,16384,256960"]
        BLOATWARE_DISABLE = ["pm disable-user --user 0 com.miui.tv.analytics", "pm disable-user --user 0 com.xiaomi.mitv.advertise", "pm disable-user --user 0 com.xiaomi.mitv.tvpush.tvpushservice"]
        KATNISS_DISABLE = ["pm disable-user --user 0 com.google.android.katniss"]
        KATNISS_ENABLE = ["pm enable com.google.android.katniss"]
        MAINTENANCE = ["pm trim-caches 4096M"]

        optimizer = XiaomiOptimizer(ip_address=target_ip)
        try:
            optimizer.connect()
            if selections['ui']: optimizer.execute_commands(UI_TWEAKS, "تسريع واجهة المستخدم والرسوميات")
            if selections['ram']: optimizer.execute_commands(RAM_TWEAKS, "تحسين إدارة الذاكرة (RAM)")
            if selections['net']: optimizer.execute_commands(NETWORK_TWEAKS, "تحسين حزم الشبكة لتسريع البث")
            if selections['bloat']: optimizer.execute_commands(BLOATWARE_DISABLE, "إيقاف خدمات التتبع الخاصة بشاومي")
            if selections['mic_disable']: optimizer.execute_commands(KATNISS_DISABLE, "إيقاف المايك ومساعد جوجل (Katniss)")
            else: optimizer.execute_commands(KATNISS_ENABLE, "تفعيل المايك ومساعد جوجل")
            if selections['cache']: optimizer.execute_commands(MAINTENANCE, "تنظيف الذاكرة المؤقتة العميقة")
                
            self.logger.info("🔥 تمت العملية بنجاح! تم تطبيق الخيارات المحددة فقط.")
        except Exception as e:
            self.logger.error("❌ توقف البرنامج بسبب خطأ في الاتصال.")
        finally:
            optimizer.disconnect()
            self.root.after(0, self.enable_buttons)

    def run_reset_task(self, target_ip):
        REVERT_ALL = [
            "settings put global window_animation_scale 1",
            "settings put global transition_animation_scale 1",
            "settings put global animator_duration_scale 1",
            "setprop persist.sys.ui.hw 0",
            "settings delete global activity_manager_max_running_operations",
            "pm enable com.miui.tv.analytics",
            "pm enable com.xiaomi.mitv.advertise",
            "pm enable com.xiaomi.mitv.tvpush.tvpushservice",
            "pm enable com.google.android.katniss"
        ]
        
        optimizer = XiaomiOptimizer(ip_address=target_ip)
        try:
            optimizer.connect()
            optimizer.execute_commands(REVERT_ALL, "إلغاء جميع التحسينات والعودة لإعدادات المصنع الافتراضية")
            self.logger.info("✅ تم استعادة الجهاز لحالته الأصلية بنجاح! (يفضل إعادة تشغيل الجهاز لتطبيق كل شيء).")
        except Exception as e:
            self.logger.error("❌ توقف البرنامج بسبب خطأ في الاتصال.")
        finally:
            optimizer.disconnect()
            self.root.after(0, self.enable_buttons)

    def start_optimization(self):
        target_ip = self.ip_combo.get().strip()
        if not target_ip:
            messagebox.showerror("خطأ", "الرجاء إدخال عنوان IP أو البحث في الشبكة.")
            return

        selections = {
            'ui': self.var_ui.get(), 'ram': self.var_ram.get(), 'net': self.var_net.get(),
            'bloat': self.var_bloat.get(), 'mic_disable': self.var_mic_disable.get(), 'cache': self.var_cache.get()
        }

        self.clear_console()
        self.disable_buttons()
        threading.Thread(target=self.run_optimization_task, args=(target_ip, selections), daemon=True).start()

    def start_reset(self):
        target_ip = self.ip_combo.get().strip()
        if not target_ip:
            messagebox.showerror("خطأ", "الرجاء إدخال عنوان IP أو البحث في الشبكة.")
            return

        confirm = messagebox.askyesno("تأكيد", "هل أنت متأكد أنك تريد التراجع عن كل التغييرات وإرجاع إعدادات الجهاز الأصلية؟")
        if confirm:
            self.clear_console()
            self.disable_buttons()
            threading.Thread(target=self.run_reset_task, args=(target_ip,), daemon=True).start()

    # --- دوال مساعدة للواجهة ---
    def clear_console(self):
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')

    def disable_buttons(self):
        self.start_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.scan_btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.start_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)
        self.scan_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizerApp(root)
    root.mainloop()
