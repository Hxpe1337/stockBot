import discord
from discord.ext import commands

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faq(self, ctx):
        channel = self.bot.get_channel(1119978840442277970)

        embed = discord.Embed(
            title="Witamy w PayFast.eu",
            description="Zanim zaczniesz korzystać z serwera, musisz wiedzieć kilka rzeczy.\n\n- **Zasady.**\nIstnieją zasady, których musisz przestrzegać. Jeśli zasady zostaną naruszone, zostaniesz odpowiednio ukarany. Zasady te można znaleźć, naciskając przycisk Zasady poniżej.\n\n- **Regulamin.**\nKupując cokolwiek od nas, automatycznie wyrażasz zgodę na wszystkie nasze warunki. Warunki te można wyświetlić, naciskając przycisk ToS poniżej.\n\n- **FAQ.**\nPytania, które zwykle pojawiają się na czacie lub w kanałach pomocy technicznej, można przejrzeć, naciskając przycisk FAQ poniżej.",
            colour=0x9e3cd3
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119979794315096175/TOS.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119980060686942300/payfastlogo.png")

        select = discord.ui.Select(placeholder='Wybierz jedną z opcji:', options=[
            discord.SelectOption(label='Zasady', value='rules'),
            discord.SelectOption(label='ToS', value='tos'),
            discord.SelectOption(label='FAQ', value='faq')
        ])

        view = discord.ui.View()
        view.add_item(select)

        await channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.message.author != self.bot.user:
            return

        if interaction.data.get('values')[0] == "rules":
            embed = discord.Embed(
                title="Zasady PayFast.eu",
                description=(
                    "### Ważne! Przeczytaj zasady naszego serwera discord, "
                    "aby wiedzieć, co jest dozwolone, a co nie! Zasady mogą "
                    "być poprawiane i zmieniane w zależności od okoliczności.\n\n"
                    "**1. Podstawowe zasady**\n"
                    "**Wszystkie wykroczenia z tej kategorii skutkują banem.**\n\n"
                    "Promowanie jakiegokolwiek rodzaju jest zabronione "
                    "Treści NSFW lub Gore są zabronione.\n "
                    "odszywanie się pod członków Administracji jest zabronione.\n"
                    "Omijanie banów jest zabronione (tzn. poprzez tworzenie np. nowych kont) .\n"
                    "Botowanie serwera jest zabronione\nGenerowanie kont jest zabronione.\n\n"
                    "**2. Zasady czatu**\n"
                    "**Wszystkie wykroczenia w tej kategorii skutkują\nwyciszeniem.**\n\n"
                    "Spamowanie na czacie jest zabronione.\n"
                    "Obrażanie i grożenie jest zabronione.\n"
                    "Używanie wulgarnego języka jest zabronione.\n\n"
                    "**3. Zasady rynku**\n"
                    "**Wszystkie wykroczenia w tej kategorii skutkują banem.**\n\n"
                    "Sprzedaż jakiegokolwiek produktu jest nielegalna.\n"
                    "Promowanie innych usług/serwerów jest zabronione."
                ),
                colour=0x9e3cd3
            )

            embed.set_image(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119985332818038784/ZASADY.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119980060686942300/payfastlogo.png")

            await interaction.response.send_message(embed=embed,ephemeral=True)

        elif interaction.data.get('values')[0] == "tos":
            embed = discord.Embed(title="Terms of Service PayFast.eu",
                      description="- **1. Nasze usługi**\nWszystkie produkty są przez nas osobiście weryfikowane przed wysyłką.\nProces dostawy zwykle trwa od 1 do 8 godzin.\nNasze produkty są w 100% bezpieczne i niezawodne.\nPo dokonaniu zakupu, Twoje konto jest w 100% wolne od ryzyka.\n\n- **2. Nasze obietnice**\nRealizacja dostawy nastąpi w ciągu 1-48 godzin.\nWszystkie nasze produkty są objęte pełną gwarancją (1/2/3/6/12 miesięcy).\n\n- **3. Polityka zwrotów**\nZwroty są możliwe tylko w przypadku problemów po naszej stronie.\ni tylko JEŚLI zamówienie nie zostanie zrealizowane w ciągu 48 godzin, klient ma prawo do pełnego zwrotu pieniędzy.",
                      colour=0x9e3cd3)

            embed.set_image(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119979794315096175/TOS.png")

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119980060686942300/payfastlogo.png")

            await interaction.response.send_message(embed=embed,ephemeral=True)

        elif interaction.data.get('values')[0] == "faq":
            embed = discord.Embed(title="FAQ PayFast.eu",
                      description="Przed zadaniem jakiegokolwiek pytania odnoszącego się do naszego sklepu zalecamy przeczytać nasze FAQ które może zawierać już odpowiedź na twoje pytanie.\n\n- **Jak dokonać zakupu?**\n﻿\nAby dokonać zakupu, należy skontaktować się ze mną na prywatnej wiadomości lub utwórz ticketa na Discordzie i poinformuj mnie, jaki produkt cię interesuje.\n﻿\nW przypadku pytań lub wątpliwości, zachęcam do zadawania pytań.\n﻿\n- **Kiedy można oczekiwać dostarczenia przesyłki?**\n﻿\nCzas dostawy zależy od rodzaju przesyłki. Jeśli to przesyłka wirtualna, to czas oczekiwania wynosi zazwyczaj do 2 godzin. Jeśli chodzi o przesyłkę fizyczną, to czas oczekiwania wynosi około 2 dni robocze, a przesyłki są wysyłane za pośrednictwem firmy InPost.\n﻿\n- **Jakie metody płatności akceptujemy**\n﻿\n<#1119003175614173254>\n﻿\n- **Czy wszystkie metody na zarobek są legalne?**\n﻿\nNie.\n﻿\n- **Co polecam na początek?**\n﻿\nTo zależy od własnych preferencji dla każdego co innego, myślę że dla każdego się znajdzie odpowiednia rzecz.",
                      colour=0x9e3cd3)

            embed.set_image(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119988738773233724/FAQ.png")

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1090633507933536398/1119980060686942300/payfastlogo.png")

            await interaction.response.send_message(embed=embed,ephemeral=True)


async def setup(bot):
   await bot.add_cog(FAQ(bot))
