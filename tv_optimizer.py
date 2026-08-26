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
# 1. قاموس اللغات (Translations)
# ---------------------------------------------------------
LANGUAGES = {
    'ar': {
        'title': "🚀 أداة تسريع الشاومي و Android TV",
        'network': " الاتصال والجهاز ",
        'ip_label': "عنوان الـ IP:",
        'scan_btn': "🔍 اكتشاف الأجهزة",
        'options': " المميزات المراد تفعيلها (جميعها مفعلة افتراضياً) ",
        'ui': "تسريع الواجهة والأنيميشن (لتقليل التقطيع وتسريع التنقل)",
        'ram': "تحسين إدارة الرام (الحد من العمليات في الخلفية)",
        'net': "تسريع حزم الإنترنت (لتقليل التقطيع أثناء البث)",
        'bloat': "إيقاف خدمات شاومي الثقيلة (إعلانات وتتبع)",
        'mic': "إيقاف مساعد جوجل - katniss (أزل الصح ليعمل المايك)",
        'cache': "تنظيف عميق للذاكرة المؤقتة (لتوفير المساحة)",
        'start_btn': "⚡ بدء تنفيذ التحسينات",
        'reset_btn': "🔄 استعادة ضبط المصنع",
        'console': " شاشة العمليات (Console) ",
        'lang_btn': "🌐 Switch to English",
        # سجلات العمليات (Logs)
        'log_gen_key': "🔑 جاري توليد مفاتيح مصادقة جديدة (RSA Keys)...",
        'log_conn': "📡 جاري محاولة الاتصال بالجهاز: {}...",
        'log_conn_ok': "✅ تم الاتصال والمصادقة بنجاح!",
        'log_conn_err': "❌ فشل الاتصال. تأكد من عمل الجهاز وتفعيل وضع المطورين.",
        'log_exec': "⚙️ بدء تنفيذ: {}...",
        'log_warn': "⚠️ تخطي: حزمة غير موجودة أو غير مدعومة بالنظام",
        'log_err': "⚠️ فشل تنفيذ الأمر",
        'log_disc': "🔌 تم إغلاق الاتصال بالجهاز بأمان.",
        'log_scan': "🔍 جاري فحص الشبكة المحلية (المنفذ 5555)...",
        'log_found': "🎯 تم العثور على أجهزة: {}",
        'log_not_found': "⚠️ لم يتم العثور على أجهزة تدعم ADB في الشبكة.",
        'log_done': "🔥 تمت العملية بنجاح! تم تطبيق الخيارات المحددة.",
        'log_reset_done': "✅ تم استعادة إعدادات المصنع بنجاح! (يفضل إعادة التشغيل).",
        'err_ip': "الرجاء إدخال عنوان IP أو البحث في الشبكة.",
        'confirm_reset': "هل أنت متأكد أنك تريد التراجع عن كل التغييرات؟",
        'opt_ui': "تسريع واجهة المستخدم",
        'opt_ram': "تحسين الذاكرة (RAM)",
        'opt_net': "تحسين الشبكة",
        'opt_bloat': "إيقاف خدمات شاومي",
        'opt_mic_off': "إيقاف مساعد جوجل",
        'opt_mic_on': "تفعيل مساعد جوجل",
        'opt_cache': "تنظيف الكاش",
        'opt_reset': "إلغاء جميع التحسينات"
    },
    'en': {
        'title': "🚀 Android TV & Xiaomi Optimizer",
        'network': " Connection & Device ",
        'ip_label': "IP Address:",
        'scan_btn': "🔍 Scan Network",
        'options': " Features to Enable (All enabled by default) ",
        'ui': "Speed up UI & Animations (Reduce menu lag)",
        'ram': "Optimize RAM Management (Prevent freezing)",
        'net': "Optimize Network Packets (Better streaming)",
        'bloat': "Disable Xiaomi Bloatware (Ads & Tracking)",
        'mic': "Disable Google Assistant (Uncheck to use Mic)",
        'cache': "Deep Cache Cleaning (Free up storage space)",
        'start_btn': "⚡ Start Optimization",
        'reset_btn': "🔄 Factory Reset Tweaks",
        'console': " Console Operations ",
        'lang_btn': "🌐 التبديل للعربية",
        # Logs
        'log_gen_key': "🔑 Generating new RSA keys...",
        'log_conn': "📡 Attempting to connect to: {}...",
        'log_conn_ok': "✅ Connected and authenticated successfully!",
        'log_conn_err': "❌ Connection failed. Check network and developer mode.",
        'log_exec': "⚙️ Executing: {}...",
        'log_warn': "⚠️ Skipped: Package not found or unsupported",
        'log_err': "⚠️ Failed to execute command",
        'log_disc': "🔌 Connection safely closed.",
        'log_scan': "🔍 Scanning local network (Port 5555)...",
        'log_found': "🎯 Found devices: {}",
        'log_not_found': "⚠️ No ADB-enabled devices found on the network.",
        'log_done': "🔥 Operation completed successfully!",
        'log_reset_done': "✅ Factory reset successful! (Reboot recommended).",
        'err_ip': "Please enter an IP address or scan the network.",
        'confirm_reset': "Are you sure you want to revert all changes?",
        'opt_ui': "Speed up UI",
        'opt_ram': "Optimize RAM",
        'opt_net': "Optimize Network",
        'opt_bloat': "Disable Xiaomi Services",
        'opt_mic_off': "Disable Google Assistant",
        'opt_mic_on': "Enable Google Assistant",
        'opt_cache': "Clear Cache",
        'opt_reset': "Revert optimizations"
    }
}

# ---------------------------------------------------------
# 2. إعداد نظام تحويل السجلات (GUI Logger)
# ---------------------------------------------------------
class TextHandler(logging.Handler):
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
# 3. الفئة الرئيسية لأداة التحسين (Optimizer Class)
# ---------------------------------------------------------
class XiaomiOptimizer:
    def __init__(self, ip_address: str, lang: str, port: int = 5555, key_path: str = 'adbkey'):
        self.ip_address = ip_address
        self.port = port
        self.key_path = key_path
        self.lang = lang
        self.device = AdbDeviceTcp(self.ip_address, self.port)
        self.is_connected = False
        self.logger = logging.getLogger("AndroidTV_Optimizer")

    def t(self, key):
        return LANGUAGES[self.lang][key]

    def _get_signer(self) -> CryptographySigner:
        if not os.path.exists(self.key_path):
            self.logger.info(self.t('log_gen_key'))
            keygen(self.key_path)
        return CryptographySigner(self.key_path)

    def connect(self) -> None:
        self.logger.info(self.t('log_conn').format(f"{self.ip_address}:{self.port}"))
        try:
            signer = self._get_signer()
            self.device.connect(rsa_keys=[signer], transport_timeout_s=15)
            self.is_connected = True
            self.logger.info(self.t('log_conn_ok'))
        except Exception:
            self.logger.error(self.t('log_conn_err'))
            raise

    def execute_commands(self, commands: List[str], description: str) -> None:
        if not self.is_connected:
            return
        self.logger.info(self.t('log_exec').format(description))
        for cmd in commands:
            try:
                output = self.device.shell(cmd)
                # تخطي الأخطاء الصامتة للحزم غير الموجودة في الأجهزة المخصصة
                if output and ("Exception" in output or "Error" in output):
                    if "Unknown package" in output or "does not exist" in output:
                        self.logger.info(self.t('log_warn'))
                    else:
                        self.logger.warning(f"{self.t('log_err')} ({cmd})")
            except Exception:
                self.logger.warning(f"{self.t('log_err')} ({cmd})")

    def disconnect(self) -> None:
        if self.is_connected:
            self.device.close()
            self.logger.info(self.t('log_disc'))

# ---------------------------------------------------------
# 4. واجهة المستخدم الرسومية (GUI App)
# ---------------------------------------------------------
class OptimizerApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'ar'
        
        self.root.geometry("800x820")
        self.root.configure(padx=20, pady=20)
        
        # المتغيرات
        self.var_ui = tk.BooleanVar(value=True)
        self.var_ram = tk.BooleanVar(value=True)
        self.var_net = tk.BooleanVar(value=True)
        self.var_bloat = tk.BooleanVar(value=True)
        self.var_mic_disable = tk.BooleanVar(value=True)
        self.var_cache = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.setup_logging()
        self.update_ui_text() # تطبيق اللغة الأولية

    def t(self, key):
        return LANGUAGES[self.current_lang][key]

    def toggle_language(self):
        self.current_lang = 'en' if self.current_lang == 'ar' else 'ar'
        self.update_ui_text()

    def update_ui_text(self):
        self.root.title(self.t('title'))
        self.title_label.config(text=self.t('title'))
        self.lang_btn.config(text=self.t('lang_btn'))
        
        self.network_frame.config(text=self.t('network'))
        self.ip_label.config(text=self.t('ip_label'))
        self.scan_btn.config(text=self.t('scan_btn'))
        
        self.options_frame.config(text=self.t('options'))
        self.chk_ui.config(text=self.t('ui'))
        self.chk_ram.config(text=self.t('ram'))
        self.chk_net.config(text=self.t('net'))
        self.chk_bloat.config(text=self.t('bloat'))
        self.chk_mic.config(text=self.t('mic'))
        self.chk_cache.config(text=self.t('cache'))
        
        self.start_btn.config(text=self.t('start_btn'))
        self.reset_btn.config(text=self.t('reset_btn'))
        self.console_frame.config(text=self.t('console'))

    def setup_ui(self):
        # الشريط العلوي (العنوان وزر اللغة)
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.title_label = ttk.Label(top_frame, font=("Helvetica", 16, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        self.lang_btn = ttk.Button(top_frame, command=self.toggle_language)
        self.lang_btn.pack(side=tk.RIGHT)

        # قسم الشبكة
        self.network_frame = ttk.LabelFrame(self.root)
        self.network_frame.pack(fill=tk.X, pady=5, ipadx=10, ipady=10)

        self.ip_label = ttk.Label(self.network_frame, font=("Helvetica", 10))
        self.ip_label.pack(side=tk.LEFT, padx=5)
        
        self.ip_combo = ttk.Combobox(self.network_frame, font=("Helvetica", 12), width=18)
        self.ip_combo.insert(0, "192.168.100.45")
        self.ip_combo.pack(side=tk.LEFT, padx=5)

        self.scan_btn = ttk.Button(self.network_frame, command=self.start_network_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=10)

        # قسم الخيارات
        self.options_frame = ttk.LabelFrame(self.root)
        self.options_frame.pack(fill=tk.X, pady=10, ipadx=10, ipady=10)

        self.chk_ui = ttk.Checkbutton(self.options_frame, variable=self.var_ui)
        self.chk_ui.pack(anchor=tk.W, pady=4)
        
        self.chk_ram = ttk.Checkbutton(self.options_frame, variable=self.var_ram)
        self.chk_ram.pack(anchor=tk.W, pady=4)
        
        self.chk_net = ttk.Checkbutton(self.options_frame, variable=self.var_net)
        self.chk_net.pack(anchor=tk.W, pady=4)
        
        self.chk_bloat = ttk.Checkbutton(self.options_frame, variable=self.var_bloat)
        self.chk_bloat.pack(anchor=tk.W, pady=4)
        
        self.chk_mic = ttk.Checkbutton(self.options_frame, variable=self.var_mic_disable)
        self.chk_mic.pack(anchor=tk.W, pady=4)
        
        self.chk_cache = ttk.Checkbutton(self.options_frame, variable=self.var_cache)
        self.chk_cache.pack(anchor=tk.W, pady=4)

        # أزرار التنفيذ
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill=tk.X, pady=10)

        self.start_btn = ttk.Button(action_frame, command=self.start_optimization)
        self.start_btn.pack(side=tk.RIGHT, padx=5, ipadx=10)

        self.reset_btn = ttk.Button(action_frame, command=self.start_reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5, ipadx=10)

        # شاشة الأوامر
        self.console_frame = ttk.LabelFrame(self.root)
        self.console_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.console_text = tk.Text(self.console_frame, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10), state='disabled', wrap='word')
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_logging(self):
        self.logger = logging.getLogger("AndroidTV_Optimizer")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            text_handler = TextHandler(self.console_text)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
            text_handler.setFormatter(formatter)
            self.logger.addHandler(text_handler)

    # --- دوال الشبكة ---
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
        self.logger.info(self.t('log_scan'))
        local_ip = self.get_local_ip()
        base_ip = local_ip.rsplit('.', 1)[0] + '.'
        ips_to_scan = [base_ip + str(i) for i in range(1, 255)]
        
        discovered_devices = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {executor.submit(self.scan_port, ip): ip for ip in ips_to_scan}
            for future in concurrent.futures.as_completed(future_to_ip):
                if future.result():
                    discovered_devices.append(future_to_ip[future])

        if discovered_devices:
            self.logger.info(self.t('log_found').format(', '.join(discovered_devices)))
            self.root.after(0, lambda: self.ip_combo.config(values=discovered_devices))
            self.root.after(0, lambda: self.ip_combo.set(discovered_devices[0]))
        else:
            self.logger.warning(self.t('log_not_found'))
        
        self.root.after(0, self.enable_buttons)

    def start_network_scan(self):
        self.clear_console()
        self.disable_buttons()
        threading.Thread(target=self.network_scan_task, daemon=True).start()

    # --- دوال العمليات (Threaded) ---
    def run_optimization_task(self, target_ip, selections, lang):
        UI_TWEAKS = ["settings put global window_animation_scale 0", "settings put global transition_animation_scale 0", "settings put global animator_duration_scale 0", "setprop persist.sys.ui.hw 1", "setprop debug.hwui.renderer opengl"]
        RAM_TWEAKS = ["settings put global activity_manager_max_running_operations 1", "setprop dalvik.vm.heapsize 128m", "setprop dalvik.vm.heapgrowthlimit 64m"]
        NETWORK_TWEAKS = ["setprop net.tcp.buffersize.default 4096,87380,256960,4096,16384,256960", "setprop net.tcp.buffersize.wifi 4096,87380,256960,4096,16384,256960"]
        BLOATWARE_DISABLE = ["pm disable-user --user 0 com.miui.tv.analytics", "pm disable-user --user 0 com.xiaomi.mitv.advertise", "pm disable-user --user 0 com.xiaomi.mitv.tvpush.tvpushservice"]
        KATNISS_DISABLE = ["pm disable-user --user 0 com.google.android.katniss"]
        KATNISS_ENABLE = ["pm enable com.google.android.katniss"]
        MAINTENANCE = ["pm trim-caches 4096M"]

        optimizer = XiaomiOptimizer(ip_address=target_ip, lang=lang)
        try:
            optimizer.connect()
            if selections['ui']: optimizer.execute_commands(UI_TWEAKS, self.t('opt_ui'))
            if selections['ram']: optimizer.execute_commands(RAM_TWEAKS, self.t('opt_ram'))
            if selections['net']: optimizer.execute_commands(NETWORK_TWEAKS, self.t('opt_net'))
            if selections['bloat']: optimizer.execute_commands(BLOATWARE_DISABLE, self.t('opt_bloat'))
            if selections['mic_disable']: optimizer.execute_commands(KATNISS_DISABLE, self.t('opt_mic_off'))
            else: optimizer.execute_commands(KATNISS_ENABLE, self.t('opt_mic_on'))
            if selections['cache']: optimizer.execute_commands(MAINTENANCE, self.t('opt_cache'))
                
            self.logger.info(self.t('log_done'))
        except Exception:
            pass # الخطأ تمت كتابته في الكونسول داخل الـ class
        finally:
            optimizer.disconnect()
            self.root.after(0, self.enable_buttons)

    def run_reset_task(self, target_ip, lang):
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
        
        optimizer = XiaomiOptimizer(ip_address=target_ip, lang=lang)
        try:
            optimizer.connect()
            optimizer.execute_commands(REVERT_ALL, self.t('opt_reset'))
            self.logger.info(self.t('log_reset_done'))
        except Exception:
            pass
        finally:
            optimizer.disconnect()
            self.root.after(0, self.enable_buttons)

    def start_optimization(self):
        target_ip = self.ip_combo.get().strip()
        if not target_ip:
            messagebox.showerror("Error / خطأ", self.t('err_ip'))
            return

        selections = {
            'ui': self.var_ui.get(), 'ram': self.var_ram.get(), 'net': self.var_net.get(),
            'bloat': self.var_bloat.get(), 'mic_disable': self.var_mic_disable.get(), 'cache': self.var_cache.get()
        }

        self.clear_console()
        self.disable_buttons()
        # نمرر اللغة الحالية للـ Thread لضمان اتساق السجلات
        threading.Thread(target=self.run_optimization_task, args=(target_ip, selections, self.current_lang), daemon=True).start()

    def start_reset(self):
        target_ip = self.ip_combo.get().strip()
        if not target_ip:
            messagebox.showerror("Error / خطأ", self.t('err_ip'))
            return

        confirm = messagebox.askyesno("Confirm / تأكيد", self.t('confirm_reset'))
        if confirm:
            self.clear_console()
            self.disable_buttons()
            threading.Thread(target=self.run_reset_task, args=(target_ip, self.current_lang), daemon=True).start()

    # --- دوال الواجهة المساعدة ---
    def clear_console(self):
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')

    def disable_buttons(self):
        self.start_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.scan_btn.config(state=tk.DISABLED)
        self.lang_btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.start_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)
        self.scan_btn.config(state=tk.NORMAL)
        self.lang_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    
    # تطبيق ثيم مرئي أفضل إذا كان مدعوماً
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
        
    app = OptimizerApp(root)
    root.mainloop()