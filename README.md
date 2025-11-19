# AI ChatBot

Simple Discord bot that uses Google Gemini AI and Open-Meteo for weather.

## Quick Start

### Requirements:

- Python 3.8+
- a Discord bot token
- a Google Gemini API key

### Installation:

```powershell
git clone https://github.com/Mykaell-Max/AiChatBot.git
cd AiChatBot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration:
1. Copy `.env.example` to `.env` and fill `TOKEN` and `GOOGLE`.
2. Copy `src/promptConfig.example.py` to `src/promptConfig.py` and edit if desired.

Run:
```powershell
python src/bot.py
```

### Commands:
- `!chatbot <message>` — chat with the AI
- `!weather` — get current weather for ChosenCity