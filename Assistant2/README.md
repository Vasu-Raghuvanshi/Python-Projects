# AI Voice/Text Assistant 🤖

A powerful AI assistant that combines voice and text interaction with multiple AI models and system controls. Built with Python, this assistant integrates OpenAI GPT and Google Gemini for intelligent responses while providing various system utilities and information services.

## 🌟 Features

### AI Integration
- 🤖 Dual AI Model Support:
  - OpenAI GPT-3.5
  - Google Gemini
- 🔄 Easy switching between AI models
- 💡 Intelligent responses to general queries

### Input Methods
- 🎤 Voice Recognition
- ⌨️ Text Input
- 🔄 Switch between input modes anytime

### System Controls
- 🔊 Volume control (up/down/mute)
- 💡 Screen brightness adjustment
- 📊 System information monitoring
- 📸 Screenshot capability

### Information Services
- 🌤️ Weather updates
- 📰 News headlines
- 📚 Wikipedia searches
- 🔢 Mathematical calculations (via WolframAlpha)
- 🌐 Web searches

### Utilities
- 🎵 Music playback controls
- ⏰ Reminder system
- 📧 Email sending capability
- 🌐 Web browser controls

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Windows OS (for some system controls)
- Internet connection
- Microphone (for voice input)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     - OpenAI API key
     - Google API key
     - Weather API key (OpenWeatherMap)
     - News API key (NewsAPI)
     - WolframAlpha API key
     - Email credentials

### Running the Assistant
```bash
python assistant.py
```

## 🎯 Usage

### Basic Commands
- "what can you do" - Show available commands
- "change input mode" - Switch between voice and text input
- "use openai" / "use gemini" - Switch AI models
- "exit" or "quit" - Close the assistant
- "emergency exit" - Force quit

### System Controls
- "volume up/down/mute"
- "brightness up/down"
- "system info"
- "screenshot"

### Information Queries
- "weather in [city]"
- "tell me the news"
- "wikipedia [topic]"
- "calculate [expression]"
- "search for [query]"

### Music Controls
- "play music"
- "play random music"
- "stop/pause/resume music"

### Reminders
- "remind me"
- "check reminders"

## 🔑 API Keys Required

The assistant uses several external APIs. Get your API keys from:
- [OpenAI](https://platform.openai.com/)
- [Google AI](https://makersuite.google.com/app/apikey)
- [OpenWeatherMap](https://openweathermap.org/api)
- [NewsAPI](https://newsapi.org)
- [WolframAlpha](https://developer.wolframalpha.com)

## 🛠️ Error Handling

The assistant includes robust error handling:
- Graceful fallback if API keys are missing
- Network error handling
- Speech recognition error recovery
- Timeout controls
- Emergency exit option

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- Google for Gemini API
- Various Python libraries and their maintainers
- Weather, News, and WolframAlpha API providers

## 🔮 Future Improvements

- [ ] Add more AI models
- [ ] Implement natural language processing for better command recognition
- [ ] Add GUI interface
- [ ] Expand system control capabilities
- [ ] Add custom voice training
- [ ] Implement multi-language support

## ⚠️ Note

Some features require specific API keys and may be limited without them. The assistant will notify you about missing keys and continue with available features.
