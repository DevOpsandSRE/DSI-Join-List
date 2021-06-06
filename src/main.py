import json
import logging

import coloredlogs
import discord
import pg8000.native
from discord.ext import commands
from discord.ext.commands import Context

# Set up logging
coloredlogs.install(level="INFO", fmt="[%(asctime)s][%(levelname)s]: %(message)s")

# Load config
config = json.loads(open("../config.json").read())

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)
db = pg8000.native.Connection(config["db_username"],
                              host=config["db_hostname"] if config["db_hostname"] != "" else "localhost",
                              password=config["db_password"])


@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} running!")
    logging.info(f"Prefix is \"{bot.command_prefix}\"")

    db.run("CREATE TABLE IF NOT EXISTS joins (id TEXT PRIMARY KEY, joined_at TIMESTAMP)")


@bot.event
async def on_member_join(member: discord.Member):
    db.run("""INSERT INTO joins ("id", "joined_at") VALUES (:id, :joined_at::timestamp) ON CONFLICT ("id")
              DO UPDATE SET joined_at = :joined_at""",
           id=member.id,
           joined_at=str(member.joined_at).split(".")[0])


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error!\n```{error}```")


@bot.command()
@commands.has_role(config["staff_role_name"])
async def fetch(ctx: Context, *, args):
    dates = [arg.strip() for arg in args.split(";")]

    ids = db.run("""SELECT id FROM joins WHERE joined_at BETWEEN :first::timestamp AND :second::timestamp""",
                 first=dates[0], second=dates[1])

    if len(ids) > 0:
        await ctx.send("\n".join(id[0] for id in ids))
    else:
        await ctx.send("No members joined in that time frame!")


bot.remove_command("help")
bot.run(config["token"])
