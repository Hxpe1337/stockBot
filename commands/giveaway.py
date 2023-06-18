from discord.ext import commands
import discord
from datetime import datetime, timedelta
import re
import time
import random
import asyncio

class GiveawayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="giveaway")
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: str, winners: int, sponsor: discord.Member, *args):        
        prize = ' '.join(args)
        # Próba przetworzenia czasu
        time_delta = self.parse_time(duration)
        if time_delta is None:
            await ctx.send("Niepoprawny format czasu!")
            return
        
        end_time = datetime.utcnow() + time_delta
        
        # Tworzenie embedu
        embed = discord.Embed(
            title="🎉 Giveaway!",
            description=f"**Nagroda**: {prize}\n**Liczba zwycięzców**: {winners}\n**Sponsor**: {sponsor.mention}\n**Koniec**: {end_time.strftime('%d.%m.%Y %H:%M UTC')}",
            colour=discord.Colour.green()
        )
        embed.set_footer(text=f"Organizowane przez: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        
        # Wysyłanie wiadomości o giveaway
        message = await ctx.send(embed=embed)
        # Dodawanie reakcji do wiadomości
        await message.add_reaction("🎉")
        
        # Oczekiwanie na koniec giveaway
        await asyncio.sleep(time_delta.total_seconds())
        # Aktualizacja embedu
        embed.title += " - Zakończone"
        embed.colour = discord.Colour.red()
        await message.edit(embed=embed)

        # Zbieranie reakcji
        reaction = None
        for r in message.reactions:
            if str(r.emoji) == "🎉":
                reaction = r
                break

        if reaction is None:
            return

        # Zbieranie użytkowników, którzy zareagowali
        users = await reaction.users().flatten()
        users.remove(self.bot.user)

        if len(users) < winners:
            await ctx.send("Nie wystarczająco dużo uczestników do wyłonienia zwycięzców!")
            return

        # Losowanie zwycięzców
        winners = random.sample(users, winners)
        winners_mentions = ", ".join(user.mention for user in winners)

        await ctx.send(f"Gratulacje {winners_mentions}, wygraliście {prize}!")

    @staticmethod
    def parse_time(time_string: str):
        match = re.search(r"(\d+)([smhdw])$", time_string)
        if match is None:
            return None
        amount, unit = match.groups()
        amount = int(amount)
        if unit == "s":
            return timedelta(seconds=amount)
        elif unit == "m":
            return timedelta(minutes=amount)
        elif unit == "h":
            return timedelta(hours=amount)
        elif unit == "d":
            return timedelta(days=amount)
        elif unit == "w":
            return timedelta(weeks=amount)


async def setup(bot):
    await bot.add_cog(GiveawayCommand(bot))
