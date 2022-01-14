# Amogus Bot

Discord bot that spams Scuter's shitty among us memes

## Setup

### Install Python

Go to the [python download page](https://www.python.org/downloads/) and install version 3.10 or higher

## Requirements
Install the packages in the `requirements.txt` file using python's package manager. Open command prompt and type:

    pip install -r requirements.txt

If "pip" isn't found on your machine you have a python installation issue

### Create a bot application

Go to the [developer portal](https://discord.com/developers/applications) and use [this guide](https://astrogd.medium.com/how-to-create-a-discord-bot-application-afbe0e1e76af)

### Environment Variables

Create a file called `.env` in this directory like the following:

    # .env
    TOKEN=yourtokenhere
    PREFIX=&
    SAVE_CHANNEL=888490642815217714

`SAVE_CHANNEL` is the id of the channel where the bot will save new memes.

Leaving this blank will prevent users from uploading new memes (though they can still add text and link responses)