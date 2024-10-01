import os
import datetime
import discord
from weather import clima
from dotenv import load_dotenv
from gemini import chat
from promptConfig import initial_context

# token
load_dotenv()
token = os.getenv('TOKEN') 

# intents 
intents = discord.Intents.all()
intents.members = True

# bot 
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print('\033[35m-' * 24)
    print(f'\033[31m{bot.user} \033[32monline!')
    print(f'\033[34mID: \033[36m{bot.user.id}')
    print('\033[35m-\033[m' * 24)
    channel = bot.get_channel(1289913197230293024)
    online = discord.Embed(
        title='',
        color=15158332,
        description='BOT ONLINE'
    )
    # await channel.send(embed=online)


@bot.event
async def on_message(message):

    if message.content.lower().startswith('!clima'):
        dados = clima()

        response = chat.send_message(f'''Quero que gere uma mensagem sobre o clima de uberlandia utilizando as seguintes informações: {dados} 

A pessoa que voce esta respondendo se chama {message.author.name}
''')
        embeda = discord.Embed(
        title = '**Resposta**',
        color=discord.Color.green(),
        timestamp=datetime.datetime.now(),
        description= f'''{message.author.mention}

{response.text}
    ''')
        await message.channel.send(embed=embeda)


    # se vier com o prefixo
    elif message.content.lower().startswith('!breninho'):
        sensitive = message.content[9:]
        
        response = chat.send_message(f'''Gere uma resposta para a seguinte mensagem: {sensitive} 

A pessoa que voce esta respondendo se chama {message.author.name}
Lembre-se do seu prompt inicial: {initial_context}
''')
        embeda = discord.Embed(
                title = '**Resposta**',
                color=discord.Color.green(),
                timestamp=datetime.datetime.now(),
                description= f'''{message.author.mention}

{response.text}
''')
        await message.channel.send(embed=embeda)


bot.run(token)