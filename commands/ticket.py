from discord.ext import commands
import discord

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_id = 0

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(1119342414742687894)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="> Utwórz ticket", custom_id="create_ticket", emoji='🎟️'))
        await channel.send("Kliknij poniżej, aby utworzyć ticket.", view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data['custom_id'] == 'create_ticket':
            self.ticket_id += 1
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            category = self.bot.get_channel(1119342314305900755)
            channel = await interaction.guild.create_text_channel(f'Ticket-{self.ticket_id}', category=category, overwrites=overwrites)
            await channel.send(f'Cześć {interaction.user.mention}, Twój ticket został utworzony!')
            await interaction.response.send_message('Twój ticket został utworzony!', ephemeral=True)

async def setup(bot):
   await bot.add_cog(TicketSystem(bot))
