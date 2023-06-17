import discord
from discord.ext import commands
from datetime import datetime, timedelta
import humanize
import asyncio
class Ankieta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ankieta")
    @commands.has_permissions(administrator=True)
    async def ankieta(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("Podaj pytanie dla ankiety:")
        pytanie_message = await self.bot.wait_for("message", check=check, timeout=60)
        pytanie = pytanie_message.content

        await ctx.send("Podaj czas trwania ankiety (w sekundach, minutach lub godzinach):")
        czas_trwania_message = await self.bot.wait_for("message", check=check, timeout=60)
        czas_trwania_input = czas_trwania_message.content

        czas_trwania, jednostka_czasu = self.parsuj_czas(czas_trwania_input)
        if czas_trwania is None:
            await ctx.send("Nieprawidłowy format czasu trwania ankiety. Użyj formatu np. '10s', '5m' lub '2h'.")
            return

        czas_trwania_timedelta = timedelta(**{jednostka_czasu: czas_trwania})
        czas_zakonczenia = datetime.utcnow() + czas_trwania_timedelta
        now = datetime.utcnow()
        formatted_date = now.strftime("%d.%m.%Y %H:%M")
        embed = discord.Embed(title="`📊` PayFast・Ankieta", description=f"**{pytanie}**", colour=0xa70bbf)
        embed.add_field(name="`👍`", value="**Tak**", inline=True)
        embed.add_field(name="`👎`", value="**Nie**", inline=True)
        embed.add_field(name="`⏰ Czas Zakończenia`", value=f"<t:{int(czas_zakonczenia.timestamp())}:f>")
        embed.set_footer(text=f"@PayFast Ankieta • {formatted_date}")

        ankieta_channel = self.bot.get_channel(1119276863404118147)  # ID kanału, na którym ma być wysłana ankieta
        ankieta_message = await ankieta_channel.send(embed=embed)
        await ankieta_message.add_reaction("👍")  # Reakcja na TAK
        await ankieta_message.add_reaction("👎")  # Reakcja na NIE

        await ctx.send("Ankieta została wysłana.")

        czas_zakonczenia_delay = czas_zakonczenia - datetime.utcnow()
        await asyncio.sleep(czas_zakonczenia_delay.total_seconds())

        await self.zakoncz_ankiete(ankieta_message.id, czas_zakonczenia)

    def parsuj_czas(self, czas_input):
        jednostka_czasu = czas_input[-1]
        czas = czas_input[:-1]

        if not czas.isdigit():
            return None, None

        czas = int(czas)

        if jednostka_czasu == "s":
            return czas, "seconds"
        elif jednostka_czasu == "m":
            return czas, "minutes"
        elif jednostka_czasu == "h":
            return czas, "hours"
        else:
            return None, None

    async def zakoncz_ankiete(self, message_id, czas_zakonczenia):
        now = datetime.utcnow()
        formatted_date = now.strftime("%d.%m.%Y %H:%M")
        czas_zakonczenia_str = f"<t:{int(czas_zakonczenia.timestamp())}:R>"
        ankieta_channel = self.bot.get_channel(1119276863404118147)  # ID kanału z ankietami
        ankieta_message = await ankieta_channel.fetch_message(message_id)

        embed = ankieta_message.embeds[0]
        embed.title = "`📊` PayFast・Zakończona"
        embed.colour = 0xff0000
        embed.set_field_at(2, name="`⏰ Czas Zakończenia`", value=czas_zakonczenia_str, inline=True)
        embed.set_footer(text=f"@PayFast Zakończona • {formatted_date}")

        await ankieta_message.edit(embed=embed)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        ankieta_channel_id = 1119276863404118147  # ID kanału z ankietami

        if payload.channel_id == ankieta_channel_id:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

            if reaction and reaction.me:
                if payload.emoji.name == "👍":
                    print("Użytkownik zagłosował TAK")
                elif payload.emoji.name == "👎":
                    print("Użytkownik zagłosował NIE")


async def setup(bot):
    await bot.add_cog(Ankieta(bot))
