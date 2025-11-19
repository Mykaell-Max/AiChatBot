import logging
import datetime
from typing import Optional
import discord

from config import Config
from weather import clima
from gemini import chat
from promptConfig import initial_context

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = Config.BOT_PREFIX

    async def on_ready(self) -> None:
        logger.info(f'{self.user} is online!')
        logger.info(f'ID: {self.user.id}')
        print('-' * 24)
        print(f'{self.user} online!')
        print(f'ID: {self.user.id}')
        print('-' * 24)
        if Config.NOTIFICATION_CHANNEL_ID:
            channel = self.get_channel(Config.NOTIFICATION_CHANNEL_ID)
            if channel:
                online_embed = discord.Embed(
                    title='Bot Online',
                    color=Config.EMBED_COLOR_SUCCESS,
                    description=f'{self.user.mention} is online!',
                    timestamp=datetime.datetime.now()
                )
                try:
                    await channel.send(embed=online_embed)
                except discord.HTTPException as e:
                    logger.error(f"Error sending startup message: {e}")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        if message.content.lower().startswith(f'{self.prefix}clima'):
            await self._handle_weather_command(message)
        elif message.content.lower().startswith(f'{self.prefix}chatbot'):
            await self._handle_chat_command(message)
    
    async def _handle_weather_command(self, message: discord.Message) -> None:
        try:
            weather_data = clima()
            if not weather_data:
                await self._send_error_embed(message.channel, "Could not get weather data.")
                return
            prompt = f"Generate a short message about the weather in ChosenCity using this data: {weather_data}\nUser: {message.author.name}. Be brief."
            response = chat.send_message(prompt)
            if not response:
                await self._send_error_embed(message.channel, "Error processing weather data.")
                return
            embed = discord.Embed(
                title='Weather in ChosenCity',
                color=Config.EMBED_COLOR_INFO,
                timestamp=datetime.datetime.now(),
                description=f'{message.author.mention}\n\n{response.text}'
            )
            embed.set_footer(text='Data: Open-Meteo')
            await message.channel.send(embed=embed)
            logger.info(f"Weather command by {message.author}")
        except Exception as e:
            logger.error(f"Weather command error: {e}")
            await self._send_error_embed(message.channel, "An error occurred.")
    
    async def _handle_chat_command(self, message: discord.Message) -> None:
        try:
            user_message = message.content[len(f'{self.prefix}chatbot'):].strip()
            if not user_message:
                await self._send_error_embed(message.channel, "Please provide a message after the command.")
                return
            prompt = f"Reply to: {user_message}\nUser: {message.author.name}. Context: {initial_context}"
            response = chat.send_message(prompt)
            if not response:
                await self._send_error_embed(message.channel, "Could not generate a response.")
                return
            embed = discord.Embed(
                title='Response',
                color=Config.EMBED_COLOR_SUCCESS,
                timestamp=datetime.datetime.now(),
                description=f'{message.author.mention}\n\n{response.text}'
            )
            embed.set_footer(text='Powered by Google Gemini')
            await message.channel.send(embed=embed)
            logger.info(f"Chat command by {message.author}")
        except Exception as e:
            logger.error(f"Chat command error: {e}")
            await self._send_error_embed(message.channel, "An error occurred.")
    
    async def _send_error_embed(self, channel: discord.abc.Messageable, description: str) -> None:
        embed = discord.Embed(
            title='Error',
            color=Config.EMBED_COLOR_ERROR,
            description=description,
            timestamp=datetime.datetime.now()
        )
        try:
            await channel.send(embed=embed)
        except discord.HTTPException as e:
            logger.error(f"Error sending error embed: {e}")


def main() -> None:
    try:
        intents = discord.Intents.all()
        intents.members = True
        bot = Bot(intents=intents)
        logger.info("Starting bot...")
        bot.run(Config.DISCORD_TOKEN)
    except Exception as e:
        logger.critical(f"Critical error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()