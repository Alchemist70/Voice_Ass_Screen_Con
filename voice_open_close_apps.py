import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import os
import subprocess
import psutil  

r = sr.Recognizer()
phone_numbers = {"ravi": "1234567890", "raja": "9999988888", "kumar": "7777777777"}
bank_account_numbers = {"tt": "123456789", "mm": "99993333999"}

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def open_app(app_name):
    """Function to open applications based on the app name."""
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

def close_app(app_name):
    """Function to close applications based on the app name."""
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



def commands():
    try:
        with sr.Microphone(device_index=0) as source:
            r.adjust_for_ambient_noise(source)
            print("Listening... Ask now...")
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin)
            my_text = my_text.lower()
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

            elif "what is" in my_text:
                person1 = my_text.replace('what is', '')
                info1 = wikipedia.summary(person1, 1)
                speak(info1)
            elif "where is" in my_text:
                person2 = my_text.replace('where is', '')
                info2 = wikipedia.summary(person2, 1)
                speak(info2)

            elif "phone number" in my_text:
                names = list(phone_numbers)
                print(names)
                for name in names:
                    if name in my_text:
                        print(name + " phone number is " + phone_numbers[name])
                        speak(name + " phone number is " + phone_numbers[name])

            elif "account number" in my_text:
                banks = list(bank_account_numbers)
                for bank in banks:
                    if bank in my_text:
                        print(bank + " bank account number is " + bank_account_numbers[bank])
                        speak(bank + " bank account number is " + bank_account_numbers[bank])

            elif "open" in my_text:
                app_name = my_text.replace("open", "").strip()
                open_app(app_name)

            elif "close" in my_text:
                app_name = my_text.replace("close", "").strip()
                close_app(app_name)

            else:
                speak("Please ask a valid question")

    except Exception as e:
        print(f'Error in capturing microphone: {e}')
        # speak("An error occurred while capturing the microphone.")

while True:
    commands()
