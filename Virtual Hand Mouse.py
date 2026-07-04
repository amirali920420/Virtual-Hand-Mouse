import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui as p
import math
import time
cap = cv2.VideoCapture(0)
click = False
drag = False
detector = HandDetector(maxHands=1)

screen_w, screen_h = p.size()

# متغیرهای Smoothing
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7
ptime = 0
while True:

    ctime = time.time()



    ptime = ctime
    success, img = cap.read()

    if not success:
        continue

    # آینه‌ای کردن تصویر
    img = cv2.flip(img, 1)

    h, w, _ = img.shape

    hands, img = detector.findHands(img, draw=False)

    if hands:
        hand = hands[0]

        x, y = hand["lmList"][8][:2]
        thumb = hand["lmList"][4][:2]
        index = hand["lmList"][8][:2]
        middle = hand["lmList"][12]
        if middle[1] < index[1]:
            p.scroll(80)
        distance = math.hypot(
        thumb[0] - index[0],
        thumb[1] - index[1]
        )

        # تبدیل مختصات دوربین به مختصات مانیتور
        mouse_x = int((x / w) * screen_w)
        mouse_y = int((y / h) * screen_h)

        # Smoothing
        clocX = plocX + (mouse_x - plocX) / smoothening
        clocY = plocY + (mouse_y - plocY) / smoothening

        p.moveTo(clocX, clocY)

        plocX, plocY = clocX, clocY
        if distance < 30 and not click:
            p.click()
            click = True

        if distance > 40:
            click = False
        if distance < 20 and not drag:
            p.mouseDown()
            drag = True

        if distance > 40 and drag:
            p.mouseUp()
            drag = False
        ctime = time.time()

        if ctime != ptime:
            fps = 1 / (ctime - ptime)
        else:
            fps = 0

        ptime = ctime

    # ESC برای خروج
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
