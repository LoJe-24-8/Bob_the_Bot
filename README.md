# Bob the Bot
## Project overview

*Bob the bot* is the official Discord bot for the NOFUN server. It is designed to help with doing the roll calls for the clan battle sessions.

## Getting started

<TBC>

## Using the bot

Commands need to be typed in a Discord message.

`?greet` - check if the bot is alive.
`?roll call <start-hour>[ <emote1> <emote2> <emote3> <emote4> <emote5>]` - generate the roll call for the upcoming week. The bot is set up to generate 1 message for each CB session - Wed, Thu, Sat, Sun. Each session will begin on the *start-hour* parameter and go on for the following 4 hours. An emote is assigned at each hour so that other users can react accordingly, indicating their presence for the time slots. Note: the *emote5* is assigned to the "Cannot make it" answer.
