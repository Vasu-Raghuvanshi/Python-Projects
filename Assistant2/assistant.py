import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import sys
from dotenv import load_dotenv
import openai
import google.generativeai as genai
import json
import smtplib
import requests
import pyautogui
import psutil
import pygame
import time
from datetime import datetime, timedelta
import schedule
import keyboard
import screen_brightness_control as sbc
from bs4 import BeautifulSoup
import wolframalpha

# Load environment variables
load_dotenv()

# Initialize APIs
openai.api_key = os.getenv('OPENAI_API_KEY')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
WOLFRAM_API_KEY = os.getenv('WOLFRAM_API_KEY')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)  # Adjust speaking rate

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-pro')

# Initialize pygame for music
pygame.mixer.init()

# Global variables
reminders = []
music_folder = os.path.join(os.path.expanduser('~'), 'Music')
current_volume = 50

def speak(audio):
    """Convert text to speech"""
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")
        # If speech fails, at least print the message
        print(f"Assistant: {audio}")

def wishMe():
    """Wish according to time of day"""
    hour = datetime.now().hour
    if 4 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 16:
        speak("Good Afternoon")
    elif 16 <= hour < 21:
        speak("Good Evening")
    else:
        speak("Good Night")
    
    # Only try weather if API key exists
    if os.getenv('WEATHER_API_KEY'):
        try:
            weather = get_weather("your_city")
            speak(f"Current weather is {weather['description']} at {weather['temperature']}°C")
        except:
            pass
    
    speak("I am your AI Assistant. How may I help you?")

def takeCommand():
    """Takes microphone input and returns string output"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)  # Shorter ambient noise check
            r.pause_threshold = 0.8
            r.energy_threshold = 300
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("Listening timed out. Please try again.")
                return "none"
        
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "none"
        except sr.RequestError:
            print("Could not request results; check your internet connection")
            return "none"
        except Exception as e:
            print(f"Error: {e}")
            return "none"
    except Exception as e:
        print(f"Microphone error: {e}")
        return "none"

def get_openai_response(prompt):
    """Get response from OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I encountered an error with the OpenAI service."

def get_gemini_response(prompt):
    """Get response from Google's Gemini API"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "I encountered an error with the Gemini service."

def get_weather(city):
    """Get weather information for a city"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity']
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return None

def get_news():
    """Get top news headlines"""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        articles = response.json()['articles'][:5]
        return [article['title'] for article in articles]
    except Exception as e:
        print(f"News API error: {e}")
        return None

def control_system_volume(command):
    """Control system volume"""
    global current_volume
    if 'up' in command:
        current_volume = min(100, current_volume + 10)
    elif 'down' in command:
        current_volume = max(0, current_volume - 10)
    elif 'mute' in command:
        current_volume = 0
    # Set system volume using pyautogui
    pyautogui.press('volumemute' if 'mute' in command else 'volumeup' if 'up' in command else 'volumedown')

def control_brightness(command):
    """Control screen brightness"""
    try:
        current = sbc.get_brightness()[0]
        if 'up' in command:
            sbc.set_brightness(min(100, current + 10))
        elif 'down' in command:
            sbc.set_brightness(max(0, current - 10))
    except Exception as e:
        print(f"Brightness control error: {e}")

def play_music(command):
    """Play music from the music folder"""
    try:
        if not os.path.exists(music_folder):
            speak("Music folder not found")
            return
        
        music_files = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        if not music_files:
            speak("No music files found")
            return

        if 'random' in command:
            import random
            song = random.choice(music_files)
        else:
            song = music_files[0]

        pygame.mixer.music.load(os.path.join(music_folder, song))
        pygame.mixer.music.play()
        speak(f"Playing {song}")
    except Exception as e:
        print(f"Music playback error: {e}")

def set_reminder(command):
    """Set a reminder"""
    try:
        speak("What should I remind you about?")
        message = takeCommand()
        speak("In how many minutes?")
        minutes = int(''.join(filter(str.isdigit, takeCommand())))
        
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        reminders.append({
            'message': message,
            'time': reminder_time
        })
        speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}")
    except Exception as e:
        speak("Sorry, I couldn't set the reminder")
        print(f"Reminder error: {e}")

def check_reminders():
    """Check for due reminders"""
    global reminders
    current_time = datetime.now()
    due_reminders = [r for r in reminders if r['time'] <= current_time]
    for reminder in due_reminders:
        speak(f"Reminder: {reminder['message']}")
        reminders.remove(reminder)

def get_system_info():
    """Get system information"""
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    return f"CPU Usage: {cpu}%, Memory Usage: {memory.percent}%, Battery: {battery.percent}% {'Plugged In' if battery.power_plugged else 'Not Plugged In'}"

def calculate_expression(query):
    """Calculate mathematical expressions using WolframAlpha"""
    try:
        client = wolframalpha.Client(WOLFRAM_API_KEY)
        res = client.query(query)
        return next(res.results).text
    except Exception as e:
        print(f"Calculation error: {e}")
        return None

def process_ai_query(query, use_gemini=False):
    """Process query using either OpenAI or Gemini"""
    # Check if API keys are available
    if use_gemini and os.getenv('GOOGLE_API_KEY'):
        return get_gemini_response(query)
    elif not use_gemini and os.getenv('OPENAI_API_KEY'):
        return get_openai_response(query)
    else:
        return "I'm sorry, but I need an API key to process this request. Please add the appropriate API key to the .env file."

def get_available_commands():
    """Get list of all available commands"""
    commands = {
        "AI Models": [
            "use openai - Switch to OpenAI for responses",
            "use gemini - Switch to Google Gemini for responses"
        ],
        "System Controls": [
            "volume up/down/mute - Control system volume",
            "brightness up/down - Adjust screen brightness",
            "system info - Get CPU, memory, and battery status",
            "screenshot - Take a screenshot"
        ],
        "Music": [
            "play music - Play music from your Music folder",
            "play random music - Play random song",
            "stop music - Stop playing",
            "pause music - Pause playing",
            "resume music - Resume playing"
        ],
        "Information": [
            "weather in [city] - Get weather information",
            "tell me the news - Get top headlines",
            "wikipedia [topic] - Search Wikipedia",
            "calculate [expression] - Solve math problems",
            "search for [query] - Search Google"
        ],
        "Reminders": [
            "remind me - Set a new reminder",
            "check reminders - Check pending reminders"
        ],
        "Email": [
            "send email - Send an email"
        ],
        "General": [
            "what can you do - Show this help message",
            "exit/quit - Close the assistant"
        ]
    }
    return commands

def show_help():
    """Display all available commands"""
    commands = get_available_commands()
    speak("Here are the things I can do. I'll display them on screen for you to read.")
    
    # Print all commands at once
    print("\n=== Available Commands ===")
    for category, cmd_list in commands.items():
        print(f"\n{category}:")
        for cmd in cmd_list:
            print(f"  • {cmd}")
    
    # Speak a brief summary instead of every command
    speak("I can help you with:")
    summary = ["AI responses", "System controls", "Music playback", "Weather and news", 
              "Reminders", "Emails", "Web searches", "and more"]
    for item in summary:
        speak(item)

def get_input_mode():
    """Let user choose between voice and text input"""
    print("\nInput Mode:")
    print("1. Voice Input")
    print("2. Text Input")
    while True:
        try:
            choice = input("Choose input mode (1/2): ").strip()
            if choice in ['1', '2']:
                return 'voice' if choice == '1' else 'text'
        except Exception:
            pass
        print("Please enter 1 for voice or 2 for text input")

def get_text_input():
    """Get manual text input from user"""
    try:
        return input("\nYou: ").lower().strip()
    except Exception as e:
        print(f"Input error: {e}")
        return "none"

def get_user_input(input_mode):
    """Get user input based on selected mode"""
    if input_mode == 'voice':
        return takeCommand()
    else:
        return get_text_input()

if __name__ == "__main__":
    try:
        wishMe()
        use_gemini = False  # Toggle between OpenAI and Gemini
        
        # Let user choose input mode
        input_mode = get_input_mode()
        print(f"\nUsing {input_mode.upper()} input mode. You can change mode by typing 'change input mode'")
        
        # Check for missing critical API keys
        if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
            print("\nWarning: No AI API keys found. Some features will be limited.")
            print("To enable AI features, please add OPENAI_API_KEY or GOOGLE_API_KEY to your .env file.")
        
        while True:
            try:
                query = get_user_input(input_mode)
                
                if query == "none":
                    continue
                
                # Emergency exit command
                if query == "emergency exit":
                    print("Emergency exit activated")
                    break
                    
                # Input mode change
                if query == "change input mode":
                    input_mode = get_input_mode()
                    print(f"\nSwitched to {input_mode.upper()} input mode")
                    continue

                # Help command
                if any(phrase in query for phrase in ["what can you do", "help", "available commands", "show commands"]):
                    show_help()
                    continue

                # AI model selection
                if "use gemini" in query:
                    use_gemini = True
                    speak("Switched to Google Gemini")
                    continue
                elif "use openai" in query:
                    use_gemini = False
                    speak("Switched to OpenAI")
                    continue

                # System controls
                elif 'volume' in query:
                    control_system_volume(query)
                    continue
                elif 'brightness' in query:
                    control_brightness(query)
                    continue
                elif 'system info' in query:
                    info = get_system_info()
                    speak(info)
                    continue

                # Music controls
                elif 'play music' in query:
                    play_music(query)
                elif 'stop music' in query:
                    pygame.mixer.music.stop()
                elif 'pause music' in query:
                    pygame.mixer.music.pause()
                elif 'resume music' in query:
                    pygame.mixer.music.unpause()

                # Information queries
                elif 'weather' in query:
                    if not os.getenv('WEATHER_API_KEY'):
                        speak("Weather API key is not set. Please add it to the .env file to use this feature.")
                        continue
                    city = query.replace('weather', '').strip()
                    weather = get_weather(city or "your_city")
                    if weather:
                        speak(f"Temperature is {weather['temperature']}°C with {weather['description']}")

                elif 'news' in query:
                    if not os.getenv('NEWS_API_KEY'):
                        speak("News API key is not set. Please add it to the .env file to use this feature.")
                        continue
                    headlines = get_news()
                    if headlines:
                        speak("Here are today's top headlines:")
                        for headline in headlines:
                            speak(headline)

                elif 'wikipedia' in query:
                    speak('Searching Wikipedia')
                    query = query.replace("wikipedia", "")
                    try:
                        results = wikipedia.summary(query, sentences=2)
                        speak('According to Wikipedia')
                        print(results)
                        speak(results)
                    except Exception:
                        speak("Could not find that on Wikipedia")

                elif 'calculate' in query:
                    if not os.getenv('WOLFRAM_API_KEY'):
                        speak("WolframAlpha API key is not set. Please add it to the .env file to use this feature.")
                        continue
                    expression = query.replace('calculate', '').strip()
                    result = calculate_expression(expression)
                    if result:
                        speak(f"The result is {result}")

                # Reminders
                elif 'remind me' in query:
                    set_reminder(query)
                elif 'check reminders' in query:
                    check_reminders()

                # Web browsing
                elif 'open youtube' in query:
                    webbrowser.open("https://youtube.com")
                elif 'open google' in query:
                    webbrowser.open("https://google.com")
                elif 'search for' in query:
                    search_query = query.replace('search for', '')
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")

                # Email
                elif 'send email' in query:
                    try:
                        speak("What should I say in the email?")
                        content = takeCommand()
                        speak("To whom should I send it?")
                        to = takeCommand()  # You might want to maintain an email address book
                        if sendEmail(to, content):
                            speak("Email has been sent successfully")
                        else:
                            speak("Sorry, I couldn't send the email")
                    except Exception as e:
                        speak("Sorry, I couldn't send the email")

                # System commands
                elif 'screenshot' in query:
                    screenshot = pyautogui.screenshot()
                    screenshot.save(f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    speak("Screenshot taken")

                elif 'exit' in query or 'quit' in query:
                    speak("Goodbye!")
                    break

                # AI processing for general queries
                else:
                    response = process_ai_query(query, use_gemini)
                    print(response)
                    speak(response)

                # Check reminders periodically
                check_reminders()
            except Exception as e:
                print(f"Error in main loop: {e}")
                speak("I encountered an error. Please try again.")
                continue

    except Exception as e:
        print(f"Critical error: {e}")
        speak("Critical error occurred. Shutting down.")
    finally:
        print("\nAssistant shutting down...")
        try:
            engine.stop()
        except:
            pass