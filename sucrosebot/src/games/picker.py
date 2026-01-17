import random
import discord
import asyncio


async def pick_option(
    interaction: discord.Interaction,
    options: list[str]
):
    if len(options) < 2:
        await interaction.response.send_message(
            "Please provide at least **2 options**.", ephemeral=True
        )
        return

    await interaction.response.send_message("🎡 Spinning the wheel...")
    msg = await interaction.original_response()

    # Fast spin
    for _ in range(8):
        await msg.edit(content=f"🎡 {random.choice(options)}")
        await asyncio.sleep(0.25)

    # Slow spin
    for _ in range(3):
        await msg.edit(content=f"🎡 {random.choice(options)}...")
        await asyncio.sleep(0.6)

    final_choice = random.choice(options)
    await msg.edit(content=f"🎯 **Chosen:** {final_choice}")
