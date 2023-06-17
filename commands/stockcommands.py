from discord.ext import commands
from database import Database
import discord
from datetime import datetime

class StockCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database('stocks.db')
        self.db.create_table()

    @commands.command(name="create-stock")
    async def create_stock(self, ctx):
        self.db.create_table()
        await ctx.send('Baza danych stworzona!')

    @commands.command(name="product")
    async def product(self, ctx, *product: str):
        product = ' '.join(product)
        self.db.insert_product(product)
        await ctx.send(f'Produkt {product} został stworzony!')

    @commands.command(name="clear-product")
    async def clear_product(self, ctx, *product: str):
        # Łączymy wszystkie słowa w jedną nazwę produktu
        product = ' '.join(product)

        self.db.clear_product(product)
        await ctx.send(f'Usunięto wszystkie konta dla produktu {product}!')


    @commands.command(name="restock")
    async def restock(self, ctx, *args):
        if len(args) < 2:
            await ctx.send("Podaj poprawną nazwę produktu i konto!")
            return

        # ostatni argument traktujemy jako 'account'
        accounts = args[-1].split(";")
        # wszystko przed ostatnim argumentem łączymy w nazwę produktu
        product = ' '.join(args[:-1])

        if not accounts:
            await ctx.send('Nie można dodać pustego konta!')
        else:
            for account in accounts:
                self.db.add_account(product, account.strip())
            await ctx.send(f'Dodano {len(accounts)} kont(a) do {product}!')

            # Logowanie uzupełnienia na kanał
            channel = self.bot.get_channel(1119557369312063558)
            if channel is not None:
                log_embed = discord.Embed(
                    title="`📦` Produkty zostały dostarczone",
                    description=f"**Uzupełniono produkty:**\n`+{len(accounts)}` {product}",
                    colour=0xcd42ff,
                    timestamp=datetime.now()
                )
                await channel.send(embed=log_embed)






    @commands.command(name="stock")
    async def stock(self, ctx, product: str=None):
        now = datetime.utcnow()
        formatted_date = now.strftime("%d.%m.%Y %H:%M")
        embed = discord.Embed(title="`🔄` PayFast・Stock", colour=0xa70bbf)
        if product is None:
            # Pokaż stan zapasów dla wszystkich produktów
            all_stocks = self.db.get_all_stocks()
            for product, count in all_stocks:
                embed.add_field(name=f"<a:arrow_right:1119294134281314416> {product}: {count}⁣", value=f"", inline=False)
                embed.set_footer(text=f"PayFast Stock・{formatted_date}")
        else:
            # Pokaż stan zapasów dla określonego produktu
            count = self.db.get_stock(product)
            if count is None:
                await ctx.send('Nie ma takiego produktu!')
                return
            embed.add_field(name=f"{product}:", value=f"{count[0]}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="show-accounts")
    async def show_accounts(self, ctx, *product: str):
        # Łączymy wszystkie słowa w jedną nazwę produktu
        product = ' '.join(product)

        accounts = self.db.get_all_accounts(product)
        if not accounts:
            await ctx.send('Brak kont dla tego produktu!')
        else:
            embed = discord.Embed(title=f"Konta dla produktu {product}", colour=0xa70bbf)
            for account in accounts:
                embed.add_field(name="Konto:", value=account[0], inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="send")
    async def send(self, ctx, member: discord.Member, *args):
        # Ostatni argument może być liczbą kont do wysłania
        try:
            num_accounts = int(args[-1])
            product = ' '.join(args[:-1])
        except ValueError:
            # Jeśli ostatni argument nie jest liczbą, wysyłamy jedno konto
            num_accounts = 1
            product = ' '.join(args)

        if num_accounts < 1:
            await ctx.send('Musisz wysłać przynajmniej jedno konto!')
            return

        accounts_sent = 0
        accounts_text = ''
        for _ in range(num_accounts):
            account = self.db.get_random_account(product)
            if account is None or account[0] is None:
                break
            self.db.delete_account(product, account[0])
            accounts_sent += 1
            accounts_text += f'\n{account[0]}'

        if accounts_sent == 0:
            await ctx.send('Brak dostępnych kont dla tego produktu!')
        else:
            embed = discord.Embed(
                title="`📨` PayFast・Otrzymano",
                description=f"**Otrzymałeś {accounts_sent} kont(a)** od użytkownika {ctx.author.mention} do {product}\n\n```{accounts_text}```",
                colour=0xa64dfe
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1090633507933536398/1116026225413083258/miner_banner.png")
            embed.set_footer(text="@PayFast Otrzymano")
            await member.send(embed=embed)
            
            # Logowanie wysłania na kanał
            channel = self.bot.get_channel(1119557369312063558)
            if channel is not None:
                log_embed = discord.Embed(
                    title="`🚀` Produkt został wysłany",
                    description=f"<:success:1119558435080511498> **Pomyślnie Wysłano {accounts_sent}** do {product}",
                    colour=0xcd42ff,
                    timestamp=datetime.now()
                )
                await channel.send(embed=log_embed)





async def setup(bot):
   await bot.add_cog(StockCommands(bot))
