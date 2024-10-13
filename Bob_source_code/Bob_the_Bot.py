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
from parametersLoader import Parameters
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER_CHANNEL = int(os.getenv('DISCORD_SERVER_CHANNEL'))

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

parameters = Parameters()
dv = parameters.getDefaultValues()
settings = parameters.getSettings()


@bot.event
async def on_connect():
    print("Bot connected")


@bot.event
async def on_ready():
    print("Bob is ready!")
    await bot.get_channel(DISCORD_SERVER_CHANNEL).send("Bob is ready!")


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
    if day == 'Mon':
        return 'Monday'
    elif day == 'Tue':
        return 'Tuesday'
    elif day == 'Wed':
        return 'Wednesday'
    elif day == 'Thu':
        return 'Thursday'
    elif day == 'Fri':
        return 'Friday'
    elif day == 'Sat':
        return 'Saturday'
    elif day == 'Sun':
        return 'Sunday'
    else:
        return None


@bot.command(name='roll_call')
async def roll_call(ctx, start_time_utc=dv.get('default_start_time_utc'),
                    slot1react=':green_apple:',
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
    days_list = dv.get('days_list')
    today = datetime.datetime.utcnow()
    first_msg = True
    first_day_week = False
    for i in range(12):
        if not days_list:
            break
        print(f"scanning {today.strftime('%a %w %b %Y')} with first CB day = {days_list[0]}")
        if today.strftime("%a") == days_list[0]:  # check that the first CB day of the week has been found
            first_day_week = True
        if (today.strftime("%a") in days_list) and first_day_week:  # TODO: this line and the previous one are somewhat useless - if replace with a break instruction at the end of this if block
            days_list = days_list[1:]  # useless
            day_title = today.strftime("%A, %d %B %Y")
            generate_timemarker = lambda h: calendar.timegm(today.replace(hour=start_time_utc + h,
                                                                          minute=dv.get('minute_offset'),
                                                                          second=dv.get('second_offset'),
                                                                          microsecond=dv.get('microsecond_offset'))
                                                            .timetuple())
            timemarker1 = generate_timemarker(0)
            timemarker2 = generate_timemarker(1)
            timemarker3 = generate_timemarker(2)
            timemarker4 = generate_timemarker(3)
            timemarker5 = generate_timemarker(4)

            message_body = (f"This is the roll-call for **{day_title}**. Please react accordingly if you want to play "
                            f"in the respective time slots (times will be displayed as your local time if your device "
                            f"is set to the correct time zone):\n\n"
                            f"<t:{timemarker1}> to <t:{timemarker2}>: {slot1react}\n"
                            f"<t:{timemarker2}> to <t:{timemarker3}>: {slot2react}\n"
                            f"<t:{timemarker3}> to <t:{timemarker4}>: {slot3react}\n"
                            f"<t:{timemarker4}> to <t:{timemarker5}>: {slot4react}\n"
                            f"Cannot make it: {absentreact}")
            message_separator = "#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#\n"
            if first_msg:
                message = await ctx.send(message_body)
                first_msg = False
            else:
                message = await ctx.send(message_separator + message_body)
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
    await ctx.send(dv.get('help_message'))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")


# %% Run Bob_the_Bot
bot.run(TOKEN)
