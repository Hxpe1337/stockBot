import discord
from discord.ext import commands

class PurgeChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge-channel")
    @commands.has_permissions(administrator=True)
    async def purge_channel(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            await ctx.send("Nie podano poprawnego kanału.")
            return

        confirmation_message = await ctx.send(f"Czy na pewno chcesz usunąć wszystkie wiadomości z kanału {channel.mention}?")
        await confirmation_message.add_reaction('✅')  # Reaction for confirmation
        await confirmation_message.add_reaction('❌')  # Reaction for cancellation

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == confirmation_message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == '✅':
                await channel.purge(limit=None)
                await ctx.send("Usunięto wszystkie wiadomości z kanału.")
            else:
                await ctx.send("Anulowano usunięcie wiadomości.")
        except asyncio.TimeoutError:
            await ctx.send("Przekroczono limit czasu. Usunięcie wiadomości zostało anulowane.")

    @purge_channel.error
    async def purge_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Nie masz uprawnień administratora do użycia tej komendy.")

async def setup(bot):
   await bot.add_cog(PurgeChannel(bot))
