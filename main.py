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

            if 'play' in my_text:
                my_text = my_text.replace('play', '')
                speak('playing' + my_text)
                pywhatkit.playonyt(my_text)

            elif 'date' in my_text:
                today = datetime.date.today()
                speak(today)

            elif 'time' in my_text:
                timenow = datetime.datetime.now().strftime('%H:%M')
                speak(timenow)

            elif "who is" in my_text:
                person = my_text.replace('who is', '')
                info = wikipedia.summary(person, 1)
                speak(info)
            elif "what is" in my_text:
                person1 = my_text.replace('what is', '')
                info1 = wikipedia.summary(person1, 1)
                speak(info1)

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
            else:
                speak("Please ask a valid question")

    except:
        print('Error in capturing microphone...')
        
while True:
    commands()
