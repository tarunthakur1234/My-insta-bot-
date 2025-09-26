import os
import time
import random
from dotenv import load_dotenv
from instagrapi import Client

# .env file se variables load karega
load_dotenv()

# --- CONFIGURATION ---
REPEAT_COUNT = 5  # Ek baar mein 5 message bhejega

def validate_environment():
    """Check karega ki .env file mein GROUP_ID aur MESSAGE_TEXT hai ya nahi"""
    required_vars = ['GROUP_ID', 'MESSAGE_TEXT']
    if not all(os.getenv(var) for var in required_vars):
        print("❌ Error: .env file mein GROUP_ID ya MESSAGE_TEXT nahi mila.")
        return False
    return True

class InstagramMessenger:
    def _init_(self):
        self.client = Client()

    def login_from_session(self, session_file: str = "session.json") -> bool:
        """session.json file se login karega"""
        try:
            print("session.json file se login karne ki koshish...")
            self.client.load_settings(session_file)
            self.client.login_by_sessionid(self.client.sessionid)
            self.client.get_user_info(self.client.user_id)
            print("✅ Safaltapoorvak login ho gaya!")
            return True
        except FileNotFoundError:
            print(f"❌ CRITICAL ERROR: '{session_file}' file nahi mili.")
            return False
        except Exception as e:
            print(f"❌ Login ke dauran error: {str(e)}")
            return False

    def send_message_once(self, group_id: int, message: str) -> bool:
        """Group mein ek message bhejega"""
        try:
            self.client.direct_send(message, thread_ids=[group_id])
            return True
        except Exception as e:
            print(f"❌ Message bhejte samay error: {str(e)}")
            return False

def run_looping_sender(messenger: InstagramMessenger, group_id: int, message_text: str):
    """Messages ko loop mein bhejta rahega"""
    print(f"🚀 Bot shuru ho raha hai... Har burst mein {REPEAT_COUNT} messages bhejega.")
    burst_num = 0
    try:
        while True:
            burst_num += 1
            print(f"\n🔁 Burst #{burst_num} shuru...")
            
            sent_count = 0
            for i in range(REPEAT_COUNT):
                unique_message = f"{message_text} [ID: {burst_num}-{i+1}]"
                print(f"📤 [{i+1}/{REPEAT_COUNT}] Bhej raha hai...")
                if messenger.send_message_once(group_id, unique_message):
                    sent_count += 1
                    print("   ✅ Bhej diya")
                else:
                    print("   ❌ Bhejne mein vifal")
                time.sleep(random.uniform(20, 30)) # Har message ke beech thoda delay
            
            print(f"✅ Burst #{burst_num} poora hua. {sent_count}/{REPEAT_COUNT} messages bheje gaye.")
            print(f"⏸ Agle burst ke liye lagbhag 1 minute intezar...")
            time.sleep(random.uniform(55, 75)) # Agle burst se pehle lamba delay
            
    except Exception as e:
        print(f"\n❌ Loop mein achanak error: {e}")
    finally:
        print("🔚 Sending loop samapt.")

def run_instagram_bot():
    """Bot ko shuru karne ka main function"""
    print("🤖 Instagram Bot shuru ho raha hai...")
    
    if not validate_environment():
        return

    messenger = InstagramMessenger()
    
    if messenger.login_from_session():
        group_id = int(os.getenv('GROUP_ID'))
        message_text = os.getenv('MESSAGE_TEXT')
        run_looping_sender(messenger, group_id, message_text)
    else:
        print("❌ Login vifal hone ke karan bot shuru nahi ho sakta.")
    
    print("🤖 Bot thread samapt ho gaya hai.")

# --- Script yahan se chalna shuru hoga ---
if __name__ == "__main__":
    run_instagram_bot()
