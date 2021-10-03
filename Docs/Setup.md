# Setup

This doc highlights step-by-step how you can add this bot to your own server.

## Installation

**Method 1** - Install the zip file

> Pathfind to the `Code` button on the repository and click on the `Download ZIP` button

**Method 2** - GitHub CLI

> For this method you will need the [GitHub CLI](https://cli.github.com) installed on your computer.

> Copy the following code into your terminal to begin the installation!

```
gh repo clone GhostyCatt/TheCloud
```

## Discord Application

To create a discord application, visit the link below

**discord.com/developers/applications**

There, click on `New Application` in the top right corner.
After making your application, click on the "Bots" Section in the application, and add a bot to it!

Once you have the bot, copy the bots `Token`, it should look something like :

*`MjM4NDk0NzU2NTIxMzc3Nzky.CunGFQ.wUILz7z6HoJzVeq6pyHPmVgQgV4`*

Now you can start building the bot!

## Installing requirements

**Required Libraries** : 

* python-dotenv = "^0.19.0"
* colorama = "^0.4.4"
* Flask = "^2.0.1"
* pymongo = "^3.12.0"
* nextcord = "^2.0.0-alpha.3"
* mysql-connector = "^2.2.9"

You can install all these libraries using the `pip install` command in the console.

## Setting up

**Environment Variables**

You will need to create a `.Env` file in the same directory as the `Main.py` file.

```
DiscordToken=
Host=
Password=
```

Use this template. The `Host` and `Password` are used to connect with a MySQL database

**Database**

Assuming you have a database setup (which you need to have), you will need to go though the files and replace the table names / database names from the sql statements with the deetails of your database

**Options**

In the config folder, theres a `Options.json` file, you will need to modify the values of most of these variables!

## Running 

The bot can be started by a simple `python3 Main.py` command in the console. Join our [Discord server](https://discord.gg/qw3gGzz4w2) if you run into any problems with the bot or if you want to be a part of our community!