# s01_interrupt.py — Polling vs Interrupt: ปุ่มแบบ "ขัดจังหวะ" + กระพริบไฟแบบไม่บล็อก
#
# วิธีรัน: เปิดใน BENTO IDE แล้วกด Program to Device
#
# ใน Dev I เราอ่านปุ่มแบบ polling: วน while แล้วถาม is_pressed() ซ้ำ ๆ ตลอดเวลา
# วิธีนั้นใช้ได้ แต่มี "ต้นทุน" คือ CPU ต้องคอยถามเองทุกรอบ ถ้าเผลอ sleep ยาว ๆ
# อาจพลาดจังหวะกดได้ แล็บนี้ยกระดับขึ้นมาหนึ่งขั้น มาทำความรู้จัก "interrupt":
# ให้ฮาร์ดแวร์เป็นฝ่าย "สะกิด" เราเองตอนปุ่มถูกกด เราไม่ต้องนั่งเฝ้าถาม
#
# สิ่งที่จะได้ฝึก:
#   1) Pin.irq() — ผูก callback กับขอบขาลงของปุ่ม (hardware interrupt จริงบนชิป)
#   2) loop หลักแบบ "ไม่บล็อก" ด้วย time.ticks_ms() แทนการ sleep ยาว ๆ
#   3) เห็นด้วยตาว่าไฟกระพริบสม่ำเสมอ "พร้อมกัน" กับการนับปุ่ม โดยไม่ขวางกัน

from machine import Pin   # คลาส Pin มาพร้อม .irq() สำหรับ interrupt
import gpio               # โมดูลบอร์ด: gpio.led(n) ใช้คุม LED ง่าย ๆ
import time

# หมายเหตุสำคัญเรื่อง API ของบอร์ดนี้:
#   พอร์ต MicroPython ของ PSoC Edge "ยังไม่มี" machine.Timer (ไม่มีคลาส Timer ให้เรียก)
#   เพราะฉะนั้น callback แบบ "ตั้งเวลาเป็นช่วง ๆ" เราจะทำด้วยซอฟต์แวร์ timer:
#   ใช้ time.ticks_ms() เทียบเวลาเองในลูปแบบไม่บล็อก — ได้ผลเหมือนกระพริบเป็นจังหวะ
#   ส่วน interrupt ของจริงบนฮาร์ดแวร์ เราใช้กับปุ่มผ่าน Pin.irq() (รองรับเต็มตัว)

led = gpio.led(0)            # ไฟดวงแรกไว้กระพริบเป็นจังหวะ
btn = Pin("USER_BUTTON", Pin.IN)   # ปุ่ม SW1 = P7_0 บนบอร์ด, ตั้งเป็นขาเข้า

press_count = 0   # ตัวนับจำนวนครั้งที่ปุ่มถูกกด — อัปเดตจากใน interrupt

def on_button(pin):
    # นี่คือ "interrupt handler" — ฮาร์ดแวร์เรียกฟังก์ชันนี้เองตอนปุ่มถูกกด
    # เราไม่ได้เรียกมันเอง และไม่รู้ล่วงหน้าว่ามันจะถูกเรียกตอนไหน
    # กฎเหล็กของ handler: ทำให้สั้นและเร็วที่สุด ห้ามงานหนัก/หน่วงเวลานาน
    global press_count
    # เติม: นับเพิ่มทีละ 1 ทุกครั้งที่ถูกกด ใช้ press_count += 1
    pass

# เติม: ผูก handler เข้ากับปุ่มที่ขอบขาลง ใช้ btn.irq(handler=..., trigger=Pin.IRQ_FALLING)


print("กดปุ่ม SW1 ได้เลย — ไฟจะกระพริบไปด้วยโดยไม่สะดุด (Ctrl+C เพื่อหยุด)")

BLINK_MS = 500              # อยากให้ไฟสลับสถานะทุก ๆ กี่มิลลิวินาที
led_on = False
last_blink = time.ticks_ms()   # จดเวลาเริ่มต้นไว้เทียบ
last_reported = -1             # กันพิมพ์ค่าซ้ำ ๆ เมื่อจำนวนกดไม่เปลี่ยน

while True:
    now = time.ticks_ms()

    # ซอฟต์แวร์ timer: ถ้าครบช่วง BLINK_MS แล้ว ค่อยสลับไฟ — ไม่ใช้ sleep ยาว
    # ข้อดี: ระหว่างรอ ลูปยังวิ่งฉิว ไม่บล็อก งานอื่น ๆ ยังทำต่อได้ทันที
    # เติม: เช็กว่าครบช่วงเวลาหรือยัง ใช้ time.ticks_diff(now, last_blink) >= BLINK_MS
    if False:
        led_on = not led_on
        led.on() if led_on else led.off()
        last_blink = now

    # ปุ่มถูกนับให้แล้วโดย interrupt — ลูปแค่คอยรายงานเมื่อค่าเปลี่ยน
    if press_count != last_reported:
        print("ปุ่มถูกกดแล้ว", press_count, "ครั้ง")
        last_reported = press_count

    time.sleep_ms(5)   # พักสั้น ๆ พอ ไม่ให้ลูป busy เกินจำเป็น (ยังถือว่าไม่บล็อก)
