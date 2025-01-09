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

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

gesture_detected = False  # To track if the gesture is detected

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def hand_gesture_control():
    global gesture_detected
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

                # Get the x, y coordinates of thumb tip (4th) and index finger tip (8th)
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Print coordinates for debugging
                print(f"Thumb Tip: ({thumb_tip.x:.2f}, {thumb_tip.y:.2f}), "
                      f"Index Tip: ({index_tip.x:.2f}, {index_tip.y:.2f})")

                # Calculate the Euclidean distance between thumb tip and index finger tip
                distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

                # Check if the distance is below a certain threshold (indicating touch)
                if distance < 0.03:  # Adjust for better sensitivity
                    gesture_detected = True
                    cv2.putText(frame, "Gesture Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    gesture_detected = False

        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()


def open_app(app_name):
    global gesture_detected
    while not gesture_detected:  # Wait until the gesture is detected
        speak("Please perform the open gesture to proceed.")
        time.sleep(2)  # Give the user time to perform the gesture

    if "notepad" in app_name:
        os.system("notepad")
        speak("Opening Notepad")
    elif "calculator" in app_name:
        os.system("calc")
        speak("Opening Calculator")
    elif "whatsapp" in app_name:
        whatsapp_path = "C:\\Program Files\\WindowsApps\\5319275A.WhatsAppDesktop_2.2450.6.0_x64__cv1g1gvanyjgm\\WhatsApp.exe"
        if os.path.exists(whatsapp_path):
            subprocess.Popen([whatsapp_path])
            speak("Opening WhatsApp")
        else:
            speak("WhatsApp not found in the default location.")
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

def close_app(app_name):
    try:
        app_process_names = {
            "notepad": "notepad.exe",
            "calculator": "ApplicationFrameHost.exe",
            "whatsapp": "WhatsApp.exe",
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
            # speak("An error occurred while capturing the microphone.")

if __name__ == "__main__":
    gesture_thread = threading.Thread(target=hand_gesture_control)
    voice_thread = threading.Thread(target=voice_assistant)

    gesture_thread.start()
    voice_thread.start()

    gesture_thread.join()
    voice_thread.join()
