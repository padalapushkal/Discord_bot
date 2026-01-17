import discord
from discord.ui import View, Button


class TicTacToeButton(Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="⬜", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view

        if interaction.user != view.current_player:
            await interaction.response.send_message(
                "It's not your turn!", ephemeral=True
            )
            return

        if view.board[self.y][self.x] != "":
            await interaction.response.send_message(
                "That spot is already taken!", ephemeral=True
            )
            return

        symbol = view.symbols[interaction.user.id]
        view.board[self.y][self.x] = symbol
        self.label = symbol
        self.style = discord.ButtonStyle.success if symbol == "❌" else discord.ButtonStyle.danger
        self.disabled = True

        winner = view.check_winner()
        if winner:
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(
                content=f"🏆 **{interaction.user.display_name} wins!**",
                view=view
            )
            view.stop()
            return

        if view.is_draw():
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(
                content="It's a **draw**!",
                view=view
            )
            view.stop()
            return

        view.switch_turn()
        await interaction.response.edit_message(
            content=f"It is now **{view.current_player.display_name}'s** turn",
            view=view
        )


class TicTacToeView(View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.symbols = {
            player1.id: "❌",
            player2.id: "⭕"
        }
        self.board = [["", "", ""] for _ in range(3)]

        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def switch_turn(self):
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )

    def check_winner(self):
        lines = self.board + list(zip(*self.board)) + [
            [self.board[i][i] for i in range(3)],
            [self.board[i][2 - i] for i in range(3)]
        ]
        for line in lines:
            if line[0] != "" and all(cell == line[0] for cell in line):
                return True
        return False

    def is_draw(self):
        return all(cell != "" for row in self.board for cell in row)
