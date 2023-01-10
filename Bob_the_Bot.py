# -*- coding: utf-8 -*-
"""
Bob the bot - NOFUN's CB roll-call discord bot.

Created on Sun Sep 18 18:03:43 2022

@author: loisj
"""

import os
import discord
import datetime
import calendar
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

from discord.ext import commands

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_connect():
    print("Bot connected")

@bot.event
async def on_ready():
    print("Bob is ready!")
    await bot.get_channel(874971354678558750).send("Bob is ready!")
    
@bot.command(name='greet')
async def greet(ctx):
    print(f"<greet> command called by {ctx.author.name} in {ctx.channel.name} at {datetime.datetime.utcnow()} UTC")
    await ctx.send(f"Hi there {ctx.author.mention}!")

@bot.command(name='creator')
async def creator(ctx):
    """
    Names the creator of the bot.
    """
    print(f"<creator> command called by {ctx.author.name} in {ctx.channel.name} at {datetime.datetime.utcnow()}")
    # creapy01= discord.User(id='<@688448403939655680>')
    await ctx.send("<@688448403939655680> is my creator!")

def short2longDAY(day):
    """Turns a day from short name (Mon) into long name (Monday)."""
    if day=='Mon': return 'Monday'
    elif day=='Tue': return 'Tuesday'
    elif day=='Wed': return 'Wednesday'
    elif day=='Thu': return 'Thursday'
    elif day=='Fri': return 'Friday'
    elif day=='Sat': return 'Saturday'
    elif day=='Sun': return 'Sunday'
    else:
        return None

@bot.command(name='roll_call')
async def roll_call(ctx, start_time_utc=18, slot1react=':green_apple:',
                                        slot2react=':apple:',
                                        slot3react=':pear:',
                                        slot4react=':tangerine:',
                                        absentreact=':cucumber:'):
    """
    Generates the sequence of messages for the roll call. Automatically adds reactions to them.
    :param ctx:
    :param start_time_utc: Time (UTC) of the day when the CB session begins.
    :param slot1react: Emote to sign up for the 1st timeframe.
    :param slot2react: Emote to sign up for the 2nd timeframe.
    :param slot3react: Emote to sign up for the 3rd timeframe.
    :param slot4react: Emote to sign up for the 4th timeframe.
    :param absentreact: Emote to indicate an absence.
    :return: Void
    """
    print(f"<roll_call> command called by {ctx.author.name} in {ctx.channel.name} at {datetime.datetime.utcnow()} UTC")
    await ctx.message.delete()
    reacts = [slot1react, slot2react, slot3react, slot4react, absentreact]
    days_list = ['Wed', 'Thu', 'Sat', 'Sun']   # list of CB days - from 'Mon Tue Wed Thu Fri Sat Sun'
    today = datetime.datetime.utcnow()
    first_msg = True
    first_day_week = False
    for i in range(12):
        if days_list == []: break
        print(f"scanning {today.strftime('%a %w %b %Y')} with first CB day = {days_list[0]}")
        if today.strftime("%a") == days_list[0]:    # check that the first CB day of the week has been found
            first_day_week = True
        if ((today.strftime("%a") in days_list) and first_day_week):
            days_list = days_list[1:]
            day_title = today.strftime("%A, %d %B %Y")
            timemarker1 = calendar.timegm(today.replace(hour=start_time_utc, minute=0, second=0, microsecond=0).timetuple())
            timemarker2 = calendar.timegm(today.replace(hour=start_time_utc+1, minute=0, second=0, microsecond=0).timetuple())
            timemarker3 = calendar.timegm(today.replace(hour=start_time_utc+2, minute=0, second=0, microsecond=0).timetuple())
            timemarker4 = calendar.timegm(today.replace(hour=start_time_utc+3, minute=0, second=0, microsecond=0).timetuple())
            timemarker5 = calendar.timegm(today.replace(hour=start_time_utc+4, minute=0, second=0, microsecond=0).timetuple())
            if first_msg:
                message = await ctx.send(f"This is the roll-call for **{day_title}**. Please react accordingly if you want to play in the respective time slots (times will be displayed as your local time if your device is set to the correct time zone):\n\n<t:{timemarker1}> to <t:{timemarker2}>: {slot1react}\n<t:{timemarker2}> to <t:{timemarker3}>: {slot2react}\n<t:{timemarker3}> to <t:{timemarker4}>: {slot3react}\n<t:{timemarker4}> to <t:{timemarker5}>: {slot4react}\nCannot make it: {absentreact}")
                first_msg = False
            else:
                message = await ctx.send(f"#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#\nThis is the roll-call for **{day_title}**. Please react accordingly if you want to play in the respective time slots (times will be displayed as your local time if your device is set to the correct time zone):\n\n<t:{timemarker1}> to <t:{timemarker2}>: {slot1react}\n<t:{timemarker2}> to <t:{timemarker3}>: {slot2react}\n<t:{timemarker3}> to <t:{timemarker4}>: {slot3react}\n<t:{timemarker4}> to <t:{timemarker5}>: {slot4react}\nCannot make it: {absentreact}")
            for react in reacts:
                await message.add_reaction(react)
        today += datetime.timedelta(days=1)

@bot.command(name='helpmebob')
async def helpmebob(ctx):
    """
    Generates a help message.
    :param ctx:
    :return: Void
    """
    print(f"<helpmebob> command called by {ctx.author.name} in {ctx.channel.name} at {datetime.datetime.utcnow()} UTC")
    await ctx.send("Bob is a bot. And does Bob the Bot do?\nBob the Bot does your beloved CB roll call.\nBut how can I get Bob the Bot to do what Bob the Bot does?\nAt the beginning of the CB week, type `/roll_call` followed by the UTC starting time of the CB session, and 5 emotes for people to react to.\nAnd then, sit and watch :wink:")

#%% Run Bob_the_Bot
bot.run(TOKEN)
