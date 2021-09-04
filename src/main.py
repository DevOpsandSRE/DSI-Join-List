import json
import logging

import coloredlogs
import discord
import pg8000.native
from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import Context
from disputils import BotEmbedPaginator

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


# Util functions
async def send_paginated_ids(ctx, ids):
    amount = len(ids) // 100
    pages = []

    def get_embed(id_page):
        return Embed(description="\n".join(id[0] for id in id_page), color=Color.red())

    if len(ids) == 0:
        await ctx.send("No members joined in that time frame!")
        return

    if len(ids) <= 100:
        await ctx.send(embed=get_embed(ids))
        return

    for i in range(amount):
        pages.append(get_embed(ids[:100]))
        del ids[:100]

    if len(ids) > 0:
        pages.append(get_embed(ids[:100]))

    paginator = BotEmbedPaginator(ctx, pages)
    await paginator.run()


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

    await send_paginated_ids(ctx, ids)


bot.remove_command("help")
bot.run(config["token"])
