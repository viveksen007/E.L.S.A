import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv 
import os
import datetime

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('?') , intents=intents)

Special_role = "Almighty"

OWNER_ID = 871321517504475157
LOG_CHANNEL_ID = 1505239893482275057

async def send_log(title, description, color):

    channel = bot.get_channel(LOG_CHANNEL_ID)

    if channel:

        owner = await bot.fetch_user(OWNER_ID)

        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        embed.add_field(
            name="Owner",
            value=owner.mention,
            inline=True
        )

        embed.set_footer(text="ELSA's LOG")

        await channel.send(embed=embed)


responses = {

    "hello":
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXMyY3Vsb21wdGo3cmF2c2d0YWk5MXJxMTh3Mjg3NzZvcXFiemNmaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xT9IgG50Fb7Mi0prBC/giphy.gif",

    "cat":
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXc1MzE1aXR4bW5jcWhkMHh6bjYwbDQ0YjR1N3BhYWFyanpyOW10aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yWku98eNsMSZOEEWnC/giphy.gif",

    "dog":
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDAwZHc0enJjZ2d0Zm50eDZoYXBha3F0cDNhZjBidDEwdnczd3NqZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/HIWNaM05qJAENE1TJM/giphy.gif",

    "goat":
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTFhNWo4a3Roa3VyeG83anMxbWJyYTAxaDR6Zjd2M3M3YXFkeXk2ZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EcnAlQcGnZq9y/giphy.gif",

    "vivek":
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMHhxeXZreXQ4aXZneThhMXVsZzJwaWNjdTR0azE0NXNhYWF3OTNpZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/HgV0lPKaTvWjKjbTmz/giphy.gif"
}


@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    await send_log(
        "✅ Bot Online",
        f"{bot.user.name} is now connected!",
        discord.Color.gold()
    )

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server Cosmos {member.mention}")

    await send_log(
        "👤 Member Joined",
        f"{member.mention} joined {member.guild.name}",
        discord.Color.green()
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg = message.content.lower()

    for word, gif in responses.items():

        if word in msg:

            await message.channel.send(gif)

            await send_log(
                "🎬 GIF AutoResponder",
                f"{message.author.mention} triggered word: `{word}`",
                discord.Color.purple()
            )

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} don't use that word!")

        await send_log(
                "🚫 Bad Word Deleted",
                f"{message.author.mention} used banned word",
                discord.Color.red()
            )

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! , How are you ?")  

    await send_log(
        "⚡ Command Used",
        f"{ctx.author.mention} used ?hello",
        discord.Color.blue()
    )

@bot.command()
async def assign (ctx):
    role = discord.utils.get(ctx.guild.roles, name=Special_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {Special_role}")

        await send_log(
            "🎭 Role Assigned",
            f"{ctx.author.mention} received {Special_role}",
            discord.Color.gold()
        )

    else:
        await ctx.send("Role doesn't exist")

        await send_log(
            "❌ Role Error",
            "Role does not exist",
            discord.Color.red()
        )

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Special_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {Special_role} removed")

        await send_log(
            "🎭 Role Removed",
            f"{ctx.author.mention} demoted from {Special_role}",
            discord.Color.gold()
        )

    else:
        await ctx.send("Role doesn't exist")

        await send_log(
            "❌ Role Error",
            "Role does not exist",
            discord.Color.red()
        )


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

