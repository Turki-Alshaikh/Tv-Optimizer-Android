# 🚀 Android TV & Xiaomi Ultimate Optimizer (GUI Edition)

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Android_TV-green)
![UI](https://img.shields.io/badge/UI-Tkinter-lightgrey)
![License](https://img.shields.io/badge/License-MIT-orange)

[**العربية 🇸🇦**](#-النسخة-العربية) | [**English 🇬🇧**](#-english-version)

---

<div align="center">
  <h3>🌍 Bilingual UI / واجهة ثنائية اللغة</h3>
  <img src="windowphoto.ar.png" alt="Android TV Optimizer GUI - Arabic" width="48%">
  <img src="windowphoto-en.png" alt="Android TV Optimizer GUI - English" width="48%">
</div>

---

## 🇸🇦 النسخة العربية

### 📌 نظرة عامة
تطبيق سطح مكتب متقدم وسهل الاستخدام بواجهة رسومية (GUI) مصمم لتحسين أداء الأجهزة الضعيفة التي تعمل بنظام Android TV بشكل جذري (مثل شاومي ستيك، مي بوكس، وكروم كاست)[cite: 2]. تم بناء الأداة باستخدام لغة بايثون ومكتبة Tkinter، وتقوم بالاتصال بجهاز التلفاز عبر الواي فاي (ADB) لحقن تعديلات عميقة في نظام التشغيل لزيادة كفاءة العتاد وإدارة الرام بشراسة[cite: 2].

### ✨ المميزات الرئيسية
* **واجهة ثنائية اللغة (جديد):** التبديل الفوري بين اللغتين العربية والإنجليزية بضغطة زر دون الحاجة لإعادة تشغيل البرنامج.
* **التعامل الذكي مع الأخطاء (جديد):** تخطي آمن بصمت للحزم غير الموجودة (مثل غياب خدمات جوجل بلاي أو حزم شاومي في بعض الأنظمة المخصصة) دون توقف الأداة.
* **فحص ذكي للشبكة:** اكتشاف تلقائي لأجهزة Android TV المتصلة بالشبكة المحلية لسهولة الاتصال[cite: 2].
* **تخصيص كامل:** التحكم في كل خيار تحسين عبر صناديق اختيار (Checkboxes) لتفعيل ما تحتاجه فقط[cite: 2].
* **استعادة ضبط المصنع:** زر مخصص للتراجع عن كافة التحسينات وإعادة الجهاز لحالته الأصلية بأمان[cite: 2].
* **توليد تلقائي للمفاتيح:** يقوم التطبيق بإنشاء مفاتيح المصادقة (RSA) تلقائياً إذا لم تكن موجودة[cite: 2].
* **استجابة فورية للواجهة:** تعطيل كافة التأثيرات الحركية من جذور النظام لضمان استجابة فورية للريموت[cite: 2].
* **تسريع العتاد (GPU):** إجبار النظام على استخدام معالج الرسوميات لعرض الواجهة، مما يفرغ المعالج الرئيسي لمهام البث[cite: 2].
* **إدارة صارمة للرام:** تحديد العمليات في الخلفية لتكون عملية واحدة فقط، وتعديل حجم الذاكرة (Dalvik VM) للأجهزة الضعيفة[cite: 2].
* **توسيع نوافذ الشبكة:** تعديل قيم شبكة TCP في الكيرنل لتسريع نقل البيانات ومنع التقطيع أثناء البث المباشر[cite: 2].
* **التحكم بالمايك والبحث الصوتي:** خيار مخصص لإيقاف أو تشغيل مساعد جوجل (`Katniss`) للحفاظ على عمل المايك أو تحرير 150 ميجابايت من الرام[cite: 2].

### 🛠️ المتطلبات الأساسية
1. **تفعيل وضع المطور في التلفاز:**
   * اذهب إلى `الإعدادات` > `تفضيلات الجهاز` > `لمحة`[cite: 2].
   * اضغط على `رقم الإصدار (Build)` 7 مرات حتى يظهر الإشعار[cite: 2].
   * ارجع للخلف، وادخل إلى `خيارات المطور`، وقم بتفعيل **تصحيح أخطاء USB (USB Debugging)**[cite: 2].
2. تأكد أن التلفاز والكمبيوتر متصلان بنفس شبكة الواي فاي[cite: 2].

### 🚀 التثبيت وطريقة الاستخدام
1. استنسخ المستودع: `git clone https://github.com/Turki-Alshaikh/Tv-Optimizer-Android.git`[cite: 2]
2. ثبت المكتبات: `pip install adb-shell cryptography`[cite: 2]
3. قم بتشغيل التطبيق: `python tv_optimizer.py`
4. خطوة حاسمة: انظر إلى شاشة التلفاز فوراً. ستظهر رسالة "السماح بتصحيح أخطاء USB؟". حدد خيار **"السماح دائماً من هذا الكمبيوتر"** واضغط **موافق**[cite: 2].

### 📺 Supported By | بدعم من متجر مفاتيحي
كما تساعدك هذه الأداة في تنظيف وتحسين أداء شاشات وأنظمة الأندرويد، يمكنك أيضاً حماية جهازك الشخصي والارتقاء بأدائه عبر استخدام برامج أصلية من **[متجر مفاتيحي (Mfatihy)](https://mfatihy.com)**[cite: 2]. 
تجنب مشاكل وبطء النظام الناتجة عن الكراكات، واحصل على **[مفاتيح تفعيل ويندوز أصلية](https://mfatihy.com/windows-keys/c1242520213)** وحزم **[مايكروسوفت أوفيس](https://mfatihy.com/Office/c2015509396)** بأسعار تنافسية جداً[cite: 2]. نحن نلتزم بتوفير تراخيص آمنة وموثوقة مع سياسة دعم واضحة لعملائنا في السعودية والخليج[cite: 2].
[![Optimize Your PC](https://img.shields.io/badge/Optimize_Your_PC-Mfatihy.com-2563EB?style=for-the-badge&logo=windows)](https://mfatihy.com)[cite: 2]

---

## 🇬🇧 English Version

### 📌 Overview
An advanced, user-friendly desktop application with a GUI designed to radically optimize the performance of low-end Android TV devices (such as Xiaomi Stick, Mi Box, and Chromecast)[cite: 2]. Built with Python and Tkinter, it connects to your TV over Wi-Fi (ADB) to inject deep OS modifications, boosting hardware efficiency and aggressively managing RAM[cite: 2].

### ✨ Key Features
* **Bilingual UI (New):** Instantly switch between English and Arabic with a single click without restarting the app.
* **Intelligent Error Handling (New):** Safely and silently skips missing packages (like the absence of Google Play Services or specific Xiaomi bloatware on modified OS versions) without crashing.
* **Smart Network Scan:** Auto-detects Android TV devices on your local network[cite: 2].
* **Full Customization:** Toggle individual tweaks via checkboxes[cite: 2].
* **Factory Reset:** A dedicated button to safely revert all changes to stock settings[cite: 2].
* **Auto RSA Generation:** Automatically generates ADB authentication keys if missing[cite: 2].
* **Instant UI Response:** Disables all animations at the system level for zero input lag[cite: 2].
* **GPU Hardware Acceleration:** Forces the GPU to render the UI, freeing up the CPU for streaming tasks[cite: 2].
* **Aggressive RAM Management:** Limits background processes to 1 and tweaks Dalvik VM heap sizes for weak hardware[cite: 2].
* **Network Buffers Expansion:** Tweaks kernel TCP network values to speed up data transfer and prevent streaming buffer issues[cite: 2].
* **Mic & Voice Search Control:** Toggle Google Assistant (`Katniss`) to keep the mic working or disable it to free up ~150MB of RAM[cite: 2].

### 🛠️ Prerequisites
1. **Enable Developer Mode on your TV:**
   * Go to `Settings` > `Device Preferences` > `About`[cite: 2].
   * Click on `Build` 7 times until the toast notification appears[cite: 2].
   * Go back, open `Developer Options`, and enable **USB Debugging**[cite: 2].
2. Ensure both your TV and PC are on the same Wi-Fi network[cite: 2].

### 🚀 Installation & Usage
1. Clone repo: `git clone https://github.com/Turki-Alshaikh/Tv-Optimizer-Android.git`[cite: 2]
2. Install requirements: `pip install adb-shell cryptography`[cite: 2]
3. Run: `python tv_optimizer.py`
4. Crucial Step: Look at your TV immediately. Check **"Always allow from this computer"** on the USB debugging prompt and press **OK**[cite: 2].

### 📺 Supported By | Mfatihy Store
Just as this tool optimizes your Android TV for maximum performance, you can secure and optimize your PC's performance with genuine software from **[Mfatihy Store](https://mfatihy.com)**[cite: 2]. Say goodbye to malware from cracked software and upgrade to authentic **[Windows 11/10 Pro keys](https://mfatihy.com/windows-keys/c1242520213)** and reliable **[Security & Antivirus subscriptions](https://mfatihy.com/security/c2023318291)** at unbeatable prices[cite: 2].
[![Optimize Your PC](https://img.shields.io/badge/Optimize_Your_PC-Mfatihy.com-2563EB?style=for-the-badge&logo=windows)](https://mfatihy.com)[cite: 2]

---
## 📄 License
This project is licensed under the [MIT License](LICENSE)[cite: 2].

## ⚠️ Disclaimer
This tool makes system-level modifications. Use at your own risk. Ensure you understand the changes before applying them[cite: 2].