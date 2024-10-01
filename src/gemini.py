import os
import google.generativeai as genai
from dotenv import load_dotenv
from promptConfig import initial_context

load_dotenv()
API_KEY = os.getenv('GOOGLE')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=initial_context)