# s12_net.py — เน็ต/IoT: ส่งคะแนนขึ้น Leaderboard ผ่าน MQTT
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด "Program to Device"
#
# ไอเดียของคาบนี้: ต่อ WiFi ก่อน แล้วใช้ MQTT คุยกับ broker
#   - publish  = ส่งคะแนนของเราขึ้นกระดาน
#   - subscribe + get_message = รับคะแนนของเพื่อนอีกบอร์ดมาดู
# โครงนี้จึงใช้เล่นแบบ "สองบอร์ดส่งคะแนนหากัน" ได้เลยนะ

import wifi
import mqtt
import time

# --- ตั้งค่า: แก้ 4 บรรทัดนี้ให้ตรงกับของจริงก่อนรัน ---
SSID    = "YOUR_WIFI_SSID"          # ชื่อ WiFi (2.4GHz) ของห้องเรา
PASSWORD = "YOUR_WIFI_PASSWORD"     # รหัส WiFi
BROKER  = "test.mosquitto.org"       # MQTT broker สาธารณะ (ทดสอบได้เลย)
TOPIC   = "tesaiot/class/leaderboard"   # ห้องเดียวกันทั้งคาบ ทุกคนใช้ topic นี้

PLAYER  = "board-01"                # ชื่อผู้เล่น/บอร์ดของเรา (แต่ละคนตั้งไม่ซ้ำ)

# --- 1) ต่อ WiFi ---
print("กำลังต่อ WiFi ...")
ok = False
for i in range(6):                       # ลองสูงสุด 6 ครั้ง (ครั้งแรกมักยังไม่ติด)
    if wifi.connect(SSID, PASSWORD):     # คืน True เมื่อต่อสำเร็จ
        ok = True
        break
    print("  ยังไม่ติด ลองใหม่ %d/6 ..." % (i + 1))
    time.sleep(2)                        # พัก 2 วิ ให้ WCM ตั้งตัว
if not ok:
    print("ต่อ WiFi ไม่ได้ ลองเช็ค SSID/รหัสอีกที")
    raise SystemExit
print("ต่อ WiFi แล้ว IP =", wifi.ip())   # โชว์ IP ที่ได้มา

# --- 2) ต่อ MQTT broker ---
print("กำลังต่อ MQTT broker ...")
if not mqtt.connect(BROKER, 1883, client_id=PLAYER):   # พอร์ต MQTT ปกติคือ 1883
    print("ต่อ broker ไม่ได้")
    raise SystemExit
print("ต่อ broker แล้ว")

# สมัครรับข้อความใน topic เดียวกัน เพื่อเห็นคะแนนของทุกบอร์ด
mqtt.subscribe(TOPIC)

# --- 3) ส่งคะแนนของเราขึ้นกระดาน ---
my_score = 1250                              # สมมุติว่าเพิ่งเล่นจบได้เท่านี้
payload = "%s:%d" % (PLAYER, my_score)       # รูปแบบง่าย ๆ "ชื่อ:คะแนน"
mqtt.publish(TOPIC, payload)
print("ส่งคะแนนแล้ว ->", payload)

# --- 4) วนรับคะแนนของเพื่อน 15 วินาที ---
deadline = time.time() + 15
while time.time() < deadline:
    msg = mqtt.get_message()                 # คืน (topic, payload) เป็น bytes หรือ None
    if msg is not None:
        topic, data = msg
        print("ได้คะแนนใหม่:", data.decode())  # payload เป็น bytes ต้อง .decode()
    time.sleep(0.2)                          # พักนิดให้ระบบหายใจ

mqtt.disconnect()
print("จบคาบ ปิดการเชื่อมต่อเรียบร้อย")
