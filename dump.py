# pip install SpeechRecognition
# pip install pyttsx3
# pip install pywhatkit
# pip install wikipedia
# import speech_recognition as sr
# print(sr.Microphone.list_microphone_names())

# voice_control ###################################################################
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime

r = sr.Recognizer()
phone_numbers = {"ravi":"1234567890", "raja": "9999988888", "kumar":"7777777777"}
bank_account_numbers = {"tt": "123456789", "mm": "99993333999"}

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()
def commands():
    try:
        with sr.Microphone(device_index=0) as source:
            r.adjust_for_ambient_noise(source)
            print("Listening... Ask now...")
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin)
            my_text = my_text.lower()
            print(my_text)

            # ask to play song
            if 'play' in my_text:
                my_text = my_text.replace('play', '')
                speak('playing' + my_text)
                pywhatkit.playonyt(my_text)

            # ask date
            elif 'date' in my_text:
                today = datetime.date.today()
                speak(today)
                
            # ask time
            elif 'time' in my_text:
                timenow = datetime.datetime.now().strftime('%H:%M')
                speak(timenow)

            # ask details about any person
            elif "who is" in my_text:
                person = my_text.replace('who is', '')
                info = wikipedia.summary(person, 1)
                speak(info)

            # ask phone numbers
            elif "phone number" in my_text:
                names = list(phone_numbers)
                print(names)
                for name in names:
                    if name in my_text:
                        print(name + " phone number is " + phone_numbers[name])
                        speak(name + " phone number is " + phone_numbers[name])

            # ask personal bank account numbers
            elif "account number" in my_text:
                banks = list(bank_account_numbers)
                for bank in banks:
                    if bank in my_text:
                        print(bank + " bank account number is " + bank_account_numbers[bank])
                        speak(bank + " bank account number is " + bank_account_numbers[bank])
            else:
                speak("Please ask a valid question")

    except:
        print('Error in capturing microphone...')
        
while True:
    commands()

#screen_control ############################################################
import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variables to track gesture
prev_x, prev_y = 0, 0
gesture_threshold = 50  # Minimum movement to consider a swipe

def perform_swipe(direction):
    if direction == "left":
        pyautogui.hotkey('ctrl', 'left')  # Example: Switch desktop left
    elif direction == "right":
        pyautogui.hotkey('ctrl', 'right')  # Example: Switch desktop right
    elif direction == "up":
        pyautogui.scroll(500)  # Scroll up
    elif direction == "down":
        pyautogui.scroll(-500)  # Scroll down

# Capture video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for natural viewing
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with Mediapipe
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract landmark for the index finger tip
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w)
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
            
            if prev_x != 0 and prev_y != 0:
                dx = x - prev_x
                dy = y - prev_y
                
                # Detect swipe direction
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

    # Display the frame
    cv2.imshow("Hand Gesture Recognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()


#Joined ########################################################################
import cv2
import mediapipe as mp
import pyautogui
import time
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import os
import subprocess
import psutil

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variables for hand gesture
prev_x, prev_y = 0, 0
gesture_threshold = 50  # Minimum movement to consider a swipe

# Phone numbers and bank accounts (voice assistant)
phone_numbers = {"ravi": "1234567890", "raja": "9999988888", "kumar": "7777777777"}
bank_account_numbers = {"tt": "123456789", "mm": "99993333999"}

# Speak Function for Voice Assistant
def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

# Perform a swipe action
def perform_swipe(direction):
    if direction == "left":
        pyautogui.hotkey('ctrl', 'left')  # Switch desktop left
    elif direction == "right":
        pyautogui.hotkey('ctrl', 'right')  # Switch desktop right
    elif direction == "up":
        pyautogui.scroll(500)  # Scroll up
    elif direction == "down":
        pyautogui.scroll(-500)  # Scroll down

# Hand Gesture Recognition
def hand_gesture_control():
    global prev_x, prev_y
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for natural viewing
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw landmarks on the frame
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmark for the index finger tip
                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w)
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)

                if prev_x != 0 and prev_y != 0:
                    dx = x - prev_x
                    dy = y - prev_y

                    # Detect swipe direction
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

        # Display the frame
        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

# Open applications
def open_app(app_name):
    if "notepad" in app_name:
        os.system("notepad")
        speak("Opening Notepad")
    elif "calculator" in app_name:
        os.system("calc")
        speak("Opening Calculator")
    elif "chrome" in app_name:
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                speak("Opening Google Chrome")
                chrome_found = True
                break
        if not chrome_found:
            speak("Google Chrome not found in default locations.")
    else:
        speak("Sorry, I cannot open this application.")

# Close applications
def close_app(app_name):
    try:
        app_process_names = {
            "notepad": "notepad.exe",
            "calculator": "ApplicationFrameHost.exe",
            "chrome": "chrome.exe"
        }
        process_name = app_process_names.get(app_name.lower())
        if not process_name:
            speak(f"Sorry, I don't know how to close {app_name}.")
            return

        app_closed = False
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                app_closed = True
                speak(f"Closing {app_name}.")
                break

        if not app_closed:
            speak(f"{app_name} is not running.")
    except Exception as e:
        print(f"Error closing application: {e}")
        speak("An error occurred while trying to close the application.")

# Voice Command Recognition
def voice_assistant():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone(device_index=0) as source:
                r.adjust_for_ambient_noise(source)
                print("Listening... Ask now...")
                audioin = r.listen(source)
                my_text = r.recognize_google(audioin).lower()
                print(my_text)

                if 'play' in my_text:
                    my_text = my_text.replace('play', '')
                    speak('Playing ' + my_text)
                    pywhatkit.playonyt(my_text)

                elif 'date' in my_text:
                    today = datetime.date.today()
                    speak(f"Today's date is: {today}")

                elif 'time' in my_text:
                    timenow = datetime.datetime.now().strftime('%H:%M')
                    speak(f"The current time is {timenow}")

                elif "who is" in my_text:
                    person = my_text.replace('who is', '')
                    info = wikipedia.summary(person, 1)
                    speak(info)

                elif "phone number" in my_text:
                    for name, number in phone_numbers.items():
                        if name in my_text:
                            speak(f"{name}'s phone number is {number}")

                elif "account number" in my_text:
                    for bank, account in bank_account_numbers.items():
                        if bank in my_text:
                            speak(f"{bank}'s account number is {account}")

                elif "open" in my_text:
                    app_name = my_text.replace("open", "").strip()
                    open_app(app_name)

                elif "close" in my_text:
                    app_name = my_text.replace("close", "").strip()
                    close_app(app_name)

                else:
                    speak("Please ask a valid question.")
        except Exception as e:
            print(f"Error in capturing microphone: {e}")
            speak("An error occurred while capturing the microphone.")

# Run both functionalities in parallel
if __name__ == "__main__":
    gesture_thread = threading.Thread(target=hand_gesture_control)
    voice_thread = threading.Thread(target=voice_assistant)

    gesture_thread.start()
    voice_thread.start()

    gesture_thread.join()
    voice_thread.join()

