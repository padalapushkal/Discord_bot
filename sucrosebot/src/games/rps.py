import random
import discord
from discord.ui import View, Button


class RPSView(View):
    def __init__(self, player1: discord.User, player2: discord.User | None):
        super().__init__(timeout=60)
        self.player1 = player1
        self.player2 = player2
        self.choices = {}

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message(
                "This is not your game!", ephemeral=True
            )
            return False
        return True

    async def process_choice(self, interaction: discord.Interaction, choice: str):
        self.choices[interaction.user.id] = choice
        await interaction.response.send_message(
            f"You chose **{choice}**", ephemeral=True
        )

        if self.player2 is None:
            bot_choice = random.choice(["Rock", "Paper", "Scissors"])
            result = self.get_result(choice, bot_choice)
            self.stop()
            await interaction.followup.send(
                f"🪨 **{choice}** vs **{bot_choice}** ✂️\n\n{result}"
            )
        elif len(self.choices) == 2:
            self.stop()
            p1_choice = self.choices[self.player1.id]
            p2_choice = self.choices[self.player2.id]
            result = self.get_result(p1_choice, p2_choice, self.player1, self.player2)
            await interaction.followup.send(result)

    def get_result(self, c1, c2, p1=None, p2=None):
        wins = {
            ("Rock", "Scissors"),
            ("Scissors", "Paper"),
            ("Paper", "Rock"),
        }

        if c1 == c2:
            return "It's a **draw**!"

        if (c1, c2) in wins:
            return f"🏆 **{p1.display_name if p1 else 'You'} win!**"
        else:
            return f"🏆 **{p2.display_name if p2 else 'Bot'} wins!**"

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary)
    async def rock(self, interaction: discord.Interaction, _: Button):
        await self.process_choice(interaction, "Rock")

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.success)
    async def paper(self, interaction: discord.Interaction, _: Button):
        await self.process_choice(interaction, "Paper")

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.danger)
    async def scissors(self, interaction: discord.Interaction, _: Button):
        await self.process_choice(interaction, "Scissors")
