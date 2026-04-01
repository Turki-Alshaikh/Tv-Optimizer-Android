# 🚀 Android TV Ultimate Optimizer (ADB Python)

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Android_TV%20%7C%20Google_TV-green)
![License](https://img.shields.io/badge/License-MIT-orange)

🌍 **Choose your language / اختر لغتك:**
* [🇬🇧 English Version](#-english-version)
* [🇸🇦 النسخة العربية](#-النسخة-العربية)

---

## 🇬🇧 English Version

### 📌 Overview
An advanced, object-oriented Python script designed to drastically improve the performance of low-end Android TV devices (e.g., Xiaomi TV Stick, Mi Box, Chromecast). By utilizing ADB over Wi-Fi, this tool injects deep OS-level system tweaks to maximize hardware efficiency, manage RAM aggressively, and eliminate UI lag.

### ✨ Key Features
* **Zero UI Lag:** Natively disables all window animations to ensure instantaneous remote response.
* **Hardware Acceleration (GPU):** Forces the OS to utilize the GPU for UI rendering, offloading the CPU for heavy streaming tasks.
* **Aggressive RAM Management:** Limits background processes to exactly **1 process** and tunes the Dalvik VM heap size specifically for 1GB/2GB RAM environments.
* **Network Streaming Buffer Boost:** Expands TCP buffer sizes in the Kernel to prevent buffering during high-bitrate streaming (IPTV, 4K content).
* **Bloatware & Telemetry Killer:** Safely disables resource-heavy tracking services and the Google Voice Search engine (`Katniss`), freeing up to 150MB+ of RAM.
* **Deep Cache Trimming:** Clears accumulated cache from the eMMC storage to prevent read/write bottlenecks.

### 🛠️ Prerequisites
1. **Python 3.8+** installed on your machine.
2. Enable ADB on your TV:
   * `Settings` > `Device Preferences` > `About`.
   * Click on `Build` 7 times to unlock **Developer Options**.
   * Go back, open `Developer Options`, and enable **USB Debugging** (and **Wireless Debugging** if available).
3. Find your TV's IP Address (`Settings` > `Network & Internet`).

### 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/Turki-Alshaikh/Tv-Optimizer-Android.git](https://github.com/Turki-Alshaikh/Tv-Optimizer-Android.git)
   cd Tv-Optimizer-Android
