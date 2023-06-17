from discord.ext import commands
import discord

class MembersCountCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="members-count", aliases=["mc"])
    async def members_count(self, ctx):
        guild = ctx.guild

        online = len([member for member in guild.members if member.status == discord.Status.online])
        offline = len([member for member in guild.members if member.status == discord.Status.offline])
        total = len(guild.members)

        embed = discord.Embed(title="", colour=0xa70bbf)
        embed.add_field(name="`🧍‍♂️` Online", value=f"{online}", inline=True)
        embed.add_field(name="`👤` Offline", value=f"{offline}", inline=True)
        embed.add_field(name="`⏮️` Łącznie", value=f"{total}", inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MembersCountCommand(bot))
