import os
import logging
import threading
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
            self.text_widget.yview(tk.END) # التمرير التلقائي للأسفل
        # استخدام after لضمان تحديث الواجهة بأمان من مسار (Thread) آخر
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
        # توليد المفاتيح تلقائياً إذا لم تكن موجودة لمنع انهيار التطبيق
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
        self.root.geometry("600x500")
        self.root.configure(padx=20, pady=20)
        
        # تصميم الواجهة
        self.setup_ui()
        self.setup_logging()

    def setup_ui(self):
        # العنوان
        title_label = ttk.Label(self.root, text="🚀 أداة تسريع الشاومي ستيك و Android TV", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 15))

        # حقل إدخال الـ IP
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="أدخل الـ IP الخاص بالجهاز:", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)
        
        self.ip_entry = ttk.Entry(input_frame, font=("Helvetica", 12), width=15)
        self.ip_entry.insert(0, "192.168.100.45") # القيمة الافتراضية
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        # زر التشغيل
        self.start_btn = ttk.Button(input_frame, text="⚡ بدء التحسين (Optimize)", command=self.start_optimization)
        self.start_btn.pack(side=tk.RIGHT, padx=5)

        # شاشة العرض (Console)
        console_frame = ttk.LabelFrame(self.root, text=" شاشة العمليات (Console) ")
        console_frame.pack(fill=tk.BOTH, expand=True, pady=15)

        self.console_text = tk.Text(console_frame, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10), state='disabled', wrap='word')
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_logging(self):
        # توجيه السجلات إلى الـ Text Widget
        self.logger = logging.getLogger("AndroidTV_Optimizer")
        self.logger.setLevel(logging.INFO)
        
        # منع تكرار الـ Handlers إذا تم تشغيل الكود عدة مرات
        if not self.logger.handlers:
            text_handler = TextHandler(self.console_text)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%H:%M:%S")
            text_handler.setFormatter(formatter)
            self.logger.addHandler(text_handler)

    def run_optimization_task(self, target_ip):
        """هذه الدالة تعمل في مسار (Thread) منفصل لكي لا تتجمد الواجهة"""
        
        UI_TWEAKS = [
            "settings put global window_animation_scale 0",
            "settings put global transition_animation_scale 0",
            "settings put global animator_duration_scale 0",
            "setprop persist.sys.ui.hw 1",
            "setprop debug.hwui.renderer opengl"
        ]
        RAM_TWEAKS = [
            "settings put global activity_manager_max_running_operations 1",
            "setprop dalvik.vm.heapsize 128m",
            "setprop dalvik.vm.heapgrowthlimit 64m",
        ]
        NETWORK_TWEAKS = [
            "setprop net.tcp.buffersize.default 4096,87380,256960,4096,16384,256960",
            "setprop net.tcp.buffersize.wifi 4096,87380,256960,4096,16384,256960"
        ]
        BLOATWARE_DISABLE = [
            "pm disable-user --user 0 com.miui.tv.analytics",
            "pm disable-user --user 0 com.xiaomi.mitv.advertise",
            "pm disable-user --user 0 com.xiaomi.mitv.tvpush.tvpushservice",
            "pm disable-user --user 0 com.google.android.katniss" 
        ]
        MAINTENANCE = [
            "pm trim-caches 4096M"
        ]

        optimizer = XiaomiOptimizer(ip_address=target_ip)

        try:
            optimizer.connect()
            optimizer.execute_commands(UI_TWEAKS, "تسريع واجهة المستخدم والرسوميات")
            optimizer.execute_commands(RAM_TWEAKS, "تحسين إدارة الذاكرة (RAM)")
            optimizer.execute_commands(NETWORK_TWEAKS, "تحسين حزم الشبكة لتسريع البث")
            optimizer.execute_commands(BLOATWARE_DISABLE, "إيقاف خدمات التتبع والخدمات الثقيلة")
            optimizer.execute_commands(MAINTENANCE, "تنظيف الذاكرة المؤقتة العميقة")
            self.logger.info("🔥 تمت العملية بنجاح! الجهاز الآن في وضع الأداء الخارق.")
            
        except Exception as e:
            self.logger.error("❌ توقف البرنامج بسبب خطأ في الاتصال.")
        finally:
            optimizer.disconnect()
            # إعادة تفعيل الزر بعد الانتهاء
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))

    def start_optimization(self):
        target_ip = self.ip_entry.get().strip()
        if not target_ip:
            messagebox.showerror("خطأ", "الرجاء إدخال عنوان IP صحيح.")
            return

        # تنظيف الشاشة السابقة وتعطيل الزر لمنع الضغط المتكرر
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')
        self.start_btn.config(state=tk.DISABLED)

        # تشغيل العملية في مسار منفصل (Background Thread)
        task_thread = threading.Thread(target=self.run_optimization_task, args=(target_ip,))
        task_thread.daemon = True # لضمان إغلاق المسار عند إغلاق التطبيق
        task_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizerApp(root)
    root.mainloop()
