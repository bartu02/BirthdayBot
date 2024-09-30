import discord
from discord.ext import tasks, commands
from datetime import datetime
import json
import os
import asyncio

# Load birthdays from a JSON file
def load_birthdays():
    if not os.path.exists('birthdays.json'):
        # If the file doesn't exist, create an empty JSON file
        save_birthdays({})
    try:
        with open('birthdays.json', 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle case where JSON file is corrupted
        return {}

# Save birthdays to a JSON file
def save_birthdays(birthdays):
    with open('birthdays.json', 'w') as f:
        json.dump(birthdays, f)

# Set up bot command prefix and intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Birthdays dictionary
birthdays = load_birthdays()

# Set Birthday Command
@bot.command(name="birthday")
async def set_birthday(ctx, date: str):
    user_id = str(ctx.author.id)
    try:
        # Parse the date
        datetime.strptime(date, '%m-%d')
        birthdays[user_id] = date
        save_birthdays(birthdays)
        await ctx.send(f"Birthday set for {ctx.author.mention} on {date}")
    except ValueError:
        await ctx.send("Please use the format MM-DD")

# Info Command
@bot.command(name="info")
async def info(ctx):
    info_message = (
        "To register your birthday, use the command:\n"
        "`!birthday MM-DD`\n"
        "For example, to register your birthday as April 15, you would type:\n"
        "`!birthday 04-15`\n"
        "Make sure to use the format MM-DD!"
    )
    await ctx.send(info_message)

# Daily task to check birthdays
@tasks.loop(hours=24)
async def check_birthdays():
    today = datetime.now().strftime('%m-%d')
    channel = bot.get_channel(1290087726497927199)  # Replace with your actual channel ID
    if not birthdays:
        # If there are no birthdays, don't check
        print("No birthdays registered.")
        return
    for user_id, birthday in birthdays.items():
        if birthday == today:
            user = await bot.fetch_user(int(user_id))
            await channel.send(f"🎉 Happy Birthday {user.mention}! 🎉")

# Start the birthday check loop
@bot.event
async def on_ready():
    if not check_birthdays.is_running():
        check_birthdays.start()
    print(f'Logged in as {bot.user}')

# Running the bot
async def run_bot():
    await bot.start('MTI5MDA4MTgzMjE3MTQ3MDg4MA.G_JPEt.PpwLJLcX9QKBnRkeVBoggjwB9yEXF-HAl238xk')  # Replace with your actual bot token

if __name__ == "__main__":
    asyncio.run(run_bot())
