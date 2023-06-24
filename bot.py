from bot import bot
from config import Config

if __name__ == "__main__":
    bot.run(Config.Discord.bot_token)
