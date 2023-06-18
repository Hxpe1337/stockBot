import discord
from discord import PartialEmoji, ButtonStyle, app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View
from discord.errors import HTTPException
import os  
import asyncio
from datetime import datetime

class RankButton(Button):
    def __init__(self, add_role_ids: list, remove_role_ids: list, **kwargs):
        super().__init__(style=ButtonStyle.green, **kwargs)
        self.add_role_ids = add_role_ids
        self.remove_role_ids = remove_role_ids

    async def callback(self, interaction):
        try:
            for add_role_id in self.add_role_ids:
                add_role = interaction.guild.get_role(add_role_id)
                await interaction.user.add_roles(add_role)
            for remove_role_id in self.remove_role_ids:
                remove_role = interaction.guild.get_role(remove_role_id)
                await interaction.user.remove_roles(remove_role)
            await interaction.response.send_message('Pomyślnie udało się dodać role!', ephemeral=True)
        except HTTPException as e:
            await interaction.response.send_message(f'Coś poszło nie tak: {str(e)}', ephemeral=True)

class GiveRankView(View):
    def __init__(self, ctx: Context, add_role_ids: list, remove_role_ids: list):
        super().__init__()
        self.add_item(RankButton(add_role_ids, remove_role_ids, label='Weryfikacja', emoji=PartialEmoji(name='\N{money with wings}')))

intents = discord.Intents.default()
intents = discord.Intents().all()


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1119250047230550126) # Replace with your channel ID

    user = await bot.fetch_user(member.id)

    embed = discord.Embed(title="`🤝` PayFast・Witamy", colour=0xa70bbf)
    embed.description = f"<a:fire:1118968205264818176> **Witamy na serwerze użytknownika** {member.mention} mamy nadzieje że zostaniesz z nami na dłuzej!"
    embed.add_field(name="FAQ", value="<#1113141870902640640>", inline=True)
    embed.add_field(name="PLATNOSCI", value="<#1119003175614173254>", inline=True)
    embed.add_field(name="NEWS", value="<#1113139141379641414>", inline=True)
    embed.set_thumbnail(url=user.avatar.url)
    
    now = datetime.utcnow()
    formatted_date = now.strftime("%d.%m.%Y %H:%M")
    embed.set_footer(text=f"@PayFast Witamy • {formatted_date}")

    await channel.send(embed=embed)
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1119254702215934033)  # Replace with your channel ID

    embed = discord.Embed(title="`👋` PayFast・Żegnamy", colour=0xff0000)
    embed.description = f"<a:392103840_SAD_EMOJI_WITH_TEAR_40:1119255265477402744> **Żegnamy użytknownika ** {member.mention}"
    embed.set_thumbnail(url=member.avatar.url)
    now = datetime.utcnow()
    formatted_date = now.strftime("%d.%m.%Y %H:%M")
    embed.set_footer(text=f"@PayFast Żegnamy • {formatted_date}")

    await channel.send(embed=embed)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    channel = bot.get_channel(1113213292605886614) # Replace with your channel id
    add_role_ids = [1113204750805115030, 1113204818048196648] # Replace with the role ids to be added
    remove_role_ids = [1113215264071352362] # Replace with the role ids to be removed
    
    # Delete all messages on the channel
    await channel.purge(limit=None)

    embed = discord.Embed(title="`✅` PayFast・Weryfikacja", description="**Kliknij przycisk** poniżej aby zostać zweryfikowanym.", colour=0xa70bbf)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1113566341761335327/1119243220870766642/50a0b8ac4dc44c193509ee2525126b6d.jpg")

    view = GiveRankView(None, add_role_ids, remove_role_ids)
    await channel.send(embed=embed, view=view)



for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        asyncio.run(bot.load_extension(f'commands.{filename[:-3]}'))

bot.run('MTEwMzY2NTcxMDYyODA4MTY4NA.Gqz7OA.4Wey8QwerNVyrjK9Lqsfn8Ii-rhH8neZhiGWU4')
