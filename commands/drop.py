import discord
from discord.ext import commands

class DropCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="drop")
    async def drop(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("> Podaj tytuł dropu (np. Konto do ligi):")
        title = await self.bot.wait_for("message", check=check)

        await ctx.send("> Podaj konto/nagrodę z dropu (np. passy do konta):")
        price = await self.bot.wait_for("message", check=check)

        await ctx.send("> Podaj tekst stopki embedu (footer):")
        footer = await self.bot.wait_for("message", check=check)

        await ctx.send("> Podaj sponsora dropu (oznacz lub podaj nick):")
        author_input = await self.bot.wait_for("message", check=check)

        author = None
        if author_input.content.startswith("<@") and author_input.content.endswith(">"):
            # Jeśli podano wzmiankę użytkownika, pobierz informacje o nim
            user_id = int(author_input.content[2:-1])
            author = self.bot.get_user(user_id)
        else:
            # Jeśli podano nick, wyszukaj użytkownika po nicku
            author = discord.utils.get(ctx.guild.members, name=author_input.content)

        if not author:
            embed = discord.Embed(title="`⛔` PayFast・Błąd",
                                description="**Nie można** znaleźć sponsora. Użyj oznaczenia użytkownika lub podaj poprawny nick.\n\n**Przykład:**\n```@OBNHype```",
                                colour=0x000000
                                )


            await ctx.send(embed=embed)
            return

        await ctx.send("Czy na pewno chcesz wysłać ten drop?")

        embed = discord.Embed(title=title.content, description=price.content, color=0xa70bbf)
        embed.set_footer(text=footer.content)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1098320532220416112/1113140568109879436/payfast_banner.png")

        if isinstance(author, discord.Member):
            embed.set_author(name=author.display_name, icon_url=author.avatar_url, url=author.avatar_url)
        else:
            embed.set_author(name=author.name)

        preview_msg = await ctx.send("Podgląd:")
        preview_embed_msg = await ctx.send(embed=embed)
        await preview_embed_msg.add_reaction("✅")
        await preview_embed_msg.add_reaction("❌")

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add",
                check=lambda r, u: u == ctx.author and r.message.id == preview_embed_msg.id and str(r.emoji) in ["✅", "❌"],
                timeout=60
            )
            if str(reaction.emoji) == "✅":
                await ctx.message.delete()
                await preview_msg.delete()
                await preview_embed_msg.delete()
                channel = self.bot.get_channel(1118965208350724106)
                msg = await channel.send(embed=embed)
                await msg.add_reaction("<a:fire:1118968205264818176>")
            else:
                await ctx.send("Anulowano wysyłanie osadzenia.")
                await preview_msg.delete()
                await preview_embed_msg.delete()
        except asyncio.TimeoutError:
            await ctx.send("Przekroczono limit czasu. Anulowano wysyłanie osadzenia.")

async def setup(bot):
    await bot.add_cog(DropCommand(bot))
