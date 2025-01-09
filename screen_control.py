import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
gesture_threshold = 50  

def perform_swipe(direction):
    if direction == "left":
        pyautogui.hotkey('ctrl', 'left')  
    elif direction == "right":
        pyautogui.hotkey('ctrl', 'right')  
    elif direction == "up":
        pyautogui.scroll(500)  
    elif direction == "down":
        pyautogui.scroll(-500)  

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
 
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w)
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
            
            if prev_x != 0 and prev_y != 0:
                dx = x - prev_x
                dy = y - prev_y
       
                if abs(dx) > gesture_threshold and abs(dy) < gesture_threshold:
                    if dx > 0:
                        perform_swipe("right")
                    else:
                        perform_swipe("left")
                elif abs(dy) > gesture_threshold and abs(dx) < gesture_threshold:
                    if dy > 0:
                        perform_swipe("down")
                    else:
                        perform_swipe("up")
            
            prev_x, prev_y = x, y

    cv2.imshow("Hand Gesture Recognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
