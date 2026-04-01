# 🚀 Android TV Ultimate Optimizer (ADB Python)

🌍 **Read in other languages:** [🇬🇧 English](#-english-version) | [🇸🇦 العربية](#-النسخة-العربية)

---

## 🇬🇧 English Version

An advanced, object-oriented Python script designed to drastically improve the performance of low-end Android TV devices (such as Xiaomi TV Stick, Mi Box, and older Chromecast models). By utilizing ADB over Wi-Fi, this tool injects deep system tweaks to maximize hardware efficiency, manage RAM aggressively, and eliminate UI lag.

### ✨ Key Features

* **Zero UI Lag:** Disables all visual animations natively to ensure instantaneous remote response and zero CPU cycle waste.
* **Hardware Acceleration (GPU):** Forces the OS to utilize the GPU for UI rendering, offloading the CPU for heavy streaming tasks.
* **Aggressive RAM Management:** Limits background processes to an absolute minimum (1 process) and tunes the Dalvik VM heap size specifically for 1GB/2GB RAM environments.
* **Network Streaming Buffer Boost:** Expands TCP buffer sizes to prevent buffering and stuttering during high-bitrate streaming (IPTV, 4K content).
* **Bloatware & Telemetry Killer:** Safely disables resource-heavy tracking services and the Google Voice Search engine (`Katniss`), freeing up to 150MB+ of RAM.
* **Deep Cache Trimming:** Clears accumulated cache from the eMMC storage to prevent read/write bottlenecks.

### ⚙️ Compatibility
This script works seamlessly on almost all devices running **Android TV** or **Google TV**.
*(Note: Xiaomi-specific bloatware commands will safely be ignored if executed on non-Xiaomi devices like Nvidia Shield or Sony TVs without causing script failures, thanks to strict exception handling).*

### 🛠️ Prerequisites

1.  **Python 3.8+** installed on your machine.
2.  Install the required Python libraries:
    ```bash
    pip install adb-shell cryptography
    ```
3.  **Enable ADB on your TV:**
    * Go to `Settings` > `Device Preferences` > `About`.
    * Click on `Build` 7 times to unlock **Developer Options**.
    * Go back, open `Developer Options`, and enable **USB Debugging** (and **Wireless Debugging** if available).
4.  **Find your TV's IP Address:** `Settings` > `Network & Internet` > Select your connected Wi-Fi.

### 🚀 Installation & Usage

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Turki-Alshaikh/Android-TV-Optimizer.git](https://github.com/Turki-Alshaikh/Android-TV-Optimizer.git)
    cd Android-TV-Optimizer
    ```
2.  **Generate RSA Keys (First Time Only):**
    Before connecting, you need to generate authentication keys. You can do this via the `adb-shell` built-in keygen. Run this in your Python console:
    ```python
    from adb_shell.auth.keygen import keygen
    keygen('adbkey')
    ```
3.  Open `tv_optimizer.py` and change the `TARGET_IP` variable to match your TV's IP address:
    ```python
    TARGET_IP = '192.168.X.X'
    ```
4.  Run the script:
    ```bash
    python tv_optimizer.py
    ```
5.  **Crucial Step:** Look at your TV screen immediately. You will see an **"Allow USB Debugging?"** prompt. Check the *"Always allow from this computer"* box and click **OK**. (If the script times out, just run it again after allowing).

### 🧠 Under The Hood: Technical Details

Curious about what the script actually executes? Here is a technical breakdown of the injected shell commands:

| Target Category | Injected Command | Technical Purpose |
| :--- | :--- | :--- |
| **UI Speed** | `window_animation_scale 0` | Bypasses window rendering times, making menu navigation instantaneous. |
| **GPU Rendering** | `setprop persist.sys.ui.hw 1` | Forces Hardware Acceleration for the UI, relieving the CPU. |
| **RAM Tuning** | `dalvik.vm.heapsize 128m` | Prevents the Java Virtual Machine from allocating too much memory per app, avoiding out-of-memory crashes. |
| **Background Limits** | `activity_manager_max_running_operations 1` | Kills suspended apps aggressively to dedicate 100% RAM to the foreground streaming app. |
| **Network Buffers** | `net.tcp.buffersize.wifi` | Modifies the Kernel's TCP window sizes to allow larger packets, reducing network-related stuttering. |

### ⚠️ Caveats & Disclaimers
* **Voice Search Disabled:** The script disables `com.google.android.katniss` to save massive amounts of RAM. This means the microphone button on your remote will stop working. If you rely on voice search, comment out that specific line in the `BLOATWARE_DISABLE` list.
* **Persistence:** Some Android TV builds reset the `activity_manager` limit upon reboot. It is recommended to re-run the script if you restart your device completely (unplugging it from the wall).

---
---

## 🇸🇦 النسخة العربية

سكربت بايثون متقدم ومبني بنظام (OOP) مصمم لتحسين أداء الأجهزة الضعيفة التي تعمل بنظام Android TV بشكل جذري (مثل أجهزة شاومي ستيك، مي بوكس، وكروم كاست). من خلال استخدام بروتوكول ADB عبر الواي فاي، تقوم هذه الأداة بحقن تعديلات عميقة في نظام التشغيل لزيادة كفاءة العتاد، إدارة الذاكرة العشوائية (RAM) بشراسة، والقضاء على التقطيع في واجهة المستخدم.

### ✨ المميزات الرئيسية

* **استجابة فورية للواجهة (Zero Lag):** تعطيل كافة التأثيرات الحركية (Animations) من جذور النظام لضمان استجابة فورية للريموت دون إهدار طاقة المعالج.
* **تسريع العتاد (Hardware Acceleration):** إجبار النظام على استخدام معالج الرسوميات (GPU) لعرض الواجهة، مما يفرغ المعالج الرئيسي (CPU) لمهام البث وتشغيل الفيديو.
* **إدارة صارمة للرام:** تحديد العمليات في الخلفية لتكون عملية واحدة فقط، وتعديل حجم الذاكرة (Dalvik VM heap) ليتناسب خصيصاً مع الأجهزة ذات 1GB/2GB رام.
* **توسيع نوافذ الشبكة (TCP Buffers):** تعديل قيم شبكة TCP في الكيرنل لتسريع نقل البيانات ومنع التقطيع (Buffering) أثناء مشاهدة البث عالي الدقة (IPTV/4K).
* **إزالة تطبيقات النظام (Bloatware):** إيقاف خدمات التتبع الخاصة بشاومي ومحرك بحث جوجل الصوتي (`Katniss`) المليء بالاستهلاك، مما يحرر أكثر من 150 ميجابايت من الرام.
* **تنظيف الكاش العميق:** تفريغ الذاكرة المؤقتة من مساحة التخزين (eMMC) لمنع اختناق القراءة والكتابة.

### ⚙️ التوافق
يعمل هذا السكربت بسلاسة على أغلب الأجهزة التي تعمل بنظام **Android TV** أو **Google TV**.
*(ملاحظة: الأوامر المخصصة لتعطيل تطبيقات شاومي سيتم تجاهلها بأمان إذا تم تشغيل الكود على أجهزة أخرى مثل Nvidia Shield أو شاشات سوني، ولن تتسبب في توقف السكربت).*

### 🛠️ المتطلبات الأساسية

1.  تثبيت **Python 3.8** أو أحدث على جهازك.
2.  تثبيت المكتبات المطلوبة عبر سطر الأوامر:
    ```bash
    pip install adb-shell cryptography
    ```
3.  **تفعيل وضع المطور في التلفاز:**
    * اذهب إلى `الإعدادات` > `تفضيلات الجهاز` > `لمحة`.
    * اضغط على `رقم الإصدار (Build)` 7 مرات حتى يظهر لك إشعار تفعيل وضع المطور.
    * ارجع للخلف، وادخل إلى `خيارات المطور`، وقم بتفعيل **تصحيح أخطاء USB (USB Debugging)**.
4.  **معرفة الـ IP الخاص بالتلفاز:** من خلال `الإعدادات` > `الشبكة والإنترنت`.

### 🚀 طريقة التثبيت والاستخدام

1.  قم باستنساخ المستودع:
    ```bash
    git clone [https://github.com/Turki-Alshaikh/Android-TV-Optimizer.git](https://github.com/Turki-Alshaikh/Android-TV-Optimizer.git)
    cd Android-TV-Optimizer
    ```
2.  **توليد مفاتيح التشفير (للمرة الأولى فقط):**
    قبل الاتصال، يجب توليد مفاتيح للتوثيق. نفذ هذا الكود في بايثون:
    ```python
    from adb_shell.auth.keygen import keygen
    keygen('adbkey')
    ```
3.  افتح ملف `tv_optimizer.py` وقم بتعديل متغير `TARGET_IP` ليطابق عنوان التلفاز الخاص بك:
    ```python
    TARGET_IP = '192.168.X.X'
    ```
4.  قم بتشغيل السكربت:
    ```bash
    python tv_optimizer.py
    ```
5.  **خطوة حاسمة:** انظر إلى شاشة التلفاز فوراً. ستظهر رسالة **"السماح بتصحيح أخطاء USB؟"**. حدد خيار *"السماح دائماً من هذا الكمبيوتر"* واضغط **موافق**. (إذا انتهت مهلة السكربت، أعد تشغيله بعد الموافقة).

### 🧠 التفاصيل التقنية: ما تحت الغطاء

إذا كنت مهتماً بمعرفة ما يفعله الكود برمجياً، إليك جدول يوضح الأوامر التي يتم حقنها في النظام ووظيفتها التقنية:

| الفئة | الأمر البرمجي | الوظيفة التقنية |
| :--- | :--- | :--- |
| **سرعة الواجهة** | `window_animation_scale 0` | يلغي وقت تصيير النوافذ، مما يجعل التنقل بين القوائم لحظياً. |
| **الرسوميات** | `setprop persist.sys.ui.hw 1` | يجبر النظام على استخدام تسريع العتاد للواجهة، لتخفيف العبء عن المعالج. |
| **إدارة الرام** | `dalvik.vm.heapsize 128m` | يمنع الآلة الافتراضية (JVM) من حجز ذاكرة مبالغ فيها لكل تطبيق، مما يمنع الانهيار المفاجئ. |
| **الخلفية** | `activity_manager_max_running_operations 1` | يقتل التطبيقات المعلقة بشراسة لتوجيه 100% من الرام للتطبيق الذي يعمل حالياً. |
| **نطاق الشبكة** | `net.tcp.buffersize.wifi` | يعدل أحجام نوافذ TCP في الكيرنل للسماح بحزم بيانات أكبر، مما يقلل التقطيع أثناء البث. |

### ⚠️ تنبيهات هامة
* **تعطيل البحث الصوتي:** يقوم السكربت بتعطيل حزمة `com.google.android.katniss` لتوفير كمية هائلة من الرام. هذا يعني أن زر الميكروفون في الريموت سيتوقف عن العمل. إذا كنت تعتمد على البحث الصوتي، قم بوضع علامة تعليق (`#`) بجانب هذا السطر في قائمة `BLOATWARE_DISABLE` في الكود.
* **الثبات:** بعض إصدارات نظام Android TV تقوم بإعادة ضبط حد التطبيقات في الخلفية (`activity_manager`) عند إعادة تشغيل الجهاز بالكامل. يُنصح بإعادة تشغيل السكربت إذا قمت بفصل التلفاز عن الكهرباء.

---
📝 **License / الترخيص:** This project is open-source and available under the MIT License.
