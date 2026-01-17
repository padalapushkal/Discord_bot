import discord

NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


async def create_poll(
    interaction: discord.Interaction,
    question: str,
    options: list[str]
):
    if len(options) < 2:
        await interaction.response.send_message(
            "A poll needs at least **2 options**.", ephemeral=True
        )
        return

    if len(options) > 5:
        await interaction.response.send_message(
            "You can have **at most 5 options**.", ephemeral=True
        )
        return

    description = "\n".join(
        f"{NUMBER_EMOJIS[i]} {opt}" for i, opt in enumerate(options)
    )

    embed = discord.Embed(
        title="📊 Poll",
        description=f"**{question}**\n\n{description}",
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()

    for i in range(len(options)):
        await message.add_reaction(NUMBER_EMOJIS[i])
