import os
import logging
from typing import List
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_cryptography import CryptographySigner

# ---------------------------------------------------------
# 1. Logging Configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("AndroidTV_Optimizer")

# ---------------------------------------------------------
# 2. Core Optimizer Class
# ---------------------------------------------------------
class AndroidTVOptimizer:
    """A class to connect to Android TV devices and optimize performance via ADB."""
    
    def __init__(self, ip_address: str, port: int = 5555, key_path: str = 'adbkey'):
        self.ip_address = ip_address
        self.port = port
        self.key_path = key_path
        self.device = AdbDeviceTcp(self.ip_address, self.port)
        self.is_connected = False

    def _get_signer(self) -> CryptographySigner:
        if not os.path.exists(self.key_path):
            raise FileNotFoundError(f"RSA Key file '{self.key_path}' not found. Please generate it first.")
        return CryptographySigner(self.key_path)

    def connect(self) -> None:
        logger.info(f"Attempting to connect to {self.ip_address}:{self.port}...")
        try:
            signer = self._get_signer()
            self.device.connect(rsa_keys=[signer], transport_timeout_s=15)
            self.is_connected = True
            logger.info("Connected and authenticated successfully!")
        except Exception as e:
            logger.error(f"Connection failed. Ensure Wireless Debugging is enabled. Details: {e}")
            raise

    def execute_commands(self, commands: List[str], description: str) -> None:
        if not self.is_connected:
            logger.warning("Cannot execute commands. Device not connected.")
            return

        logger.info(f"Executing: {description}...")
        for cmd in commands:
            try:
                self.device.shell(cmd)
                logger.debug(f"Executed: {cmd}")
            except Exception as e:
                logger.warning(f"Failed to execute ({cmd}): {e}")

    def disconnect(self) -> None:
        if self.is_connected:
            self.device.close()
            logger.info("Connection closed safely.")

# ---------------------------------------------------------
# 3. Execution (The Tweaks)
# ---------------------------------------------------------
def main():
    # ⚠️ UPDATE THIS WITH YOUR TARGET DEVICE IP ⚠️
    TARGET_IP = '192.168.1.100' 
    
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

    optimizer = AndroidTVOptimizer(ip_address=TARGET_IP)

    try:
        optimizer.connect()
        optimizer.execute_commands(UI_TWEAKS, "UI & Hardware Acceleration Tweaks")
        optimizer.execute_commands(RAM_TWEAKS, "RAM & Dalvik Heap Management")
        optimizer.execute_commands(NETWORK_TWEAKS, "TCP Buffer Expansion (Network Streaming)")
        optimizer.execute_commands(BLOATWARE_DISABLE, "Disabling Bloatware & Telemetry")
        optimizer.execute_commands(MAINTENANCE, "Deep Cache Trimming")

        logger.info("🔥 Optimization complete! The device is now running at max performance.")
        
    except Exception as e:
        logger.error("Script terminated due to a fatal error.")
    finally:
        optimizer.disconnect()

if __name__ == "__main__":
    main()