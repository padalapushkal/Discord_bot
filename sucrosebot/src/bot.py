import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from llm import ask_llm
from games.help_command import build_help_embed
from games.rps import RPSView
from games.tictactoe import TicTacToeView
from games.polls import create_poll
from games.picker import pick_option
from personas import set_persona, reset_persona, get_persona, delete_last_n, list_personas
from persona_llm import generate_persona

# from discord.app_commands import Cooldown, CooldownType

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------------- READY ----------------
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("Slash commands synced")


# ---------------- HELP COMMAND ----------------
@bot.tree.command(
    name="help",
    description="See what Sucrose can do",
    guild=discord.Object(id=GUILD_ID)
)
async def help_command(
    interaction: discord.Interaction,
    category: str | None = None
):
    embed = build_help_embed(category)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ---------------- MESSAGE LISTENER ----------------
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content.lower() in ["piri no", "no piri", "nopiri"]:
        await message.reply(
            f"NO YOU TOO {message.author.display_name} <:fern_pout:1239754197952630814>"
        )

    await bot.process_commands(message)


# ---------------- SLASH COMMANDS ----------------
@bot.tree.command(name="sayhello", description="Sucrose replies hello to traveller", guild=discord.Object(id=GUILD_ID))
async def sayhello(interaction: discord.Interaction):
    rand_int = random.randint(1, 3)

    if interaction.user.id == 192697546446077953:
        await interaction.response.send_message(
            f"NO <@{interaction.user.id}> <:fern_pout:1224356099461873714>"
        )
    elif rand_int == 1:
        await interaction.response.send_message(
            f"I don't want to say hello to <@{interaction.user.id}>"
        )
    else:
        await interaction.response.send_message(
            f"Hello I'm Sucrose, a researcher of alchemy, it's nice to meet you "
            f"{interaction.user.display_name}, I'd love to hear any stories you have about your adventures"
        )


@bot.tree.command(name="sayloveyou", description="Sucrose tells I love you", guild=discord.Object(id=GUILD_ID))
@discord.app_commands.describe(person_name="Enter the name")
async def sayloveyou(interaction: discord.Interaction, person_name: str):
    rand_int = random.randint(1, 3)

    if rand_int == 1:
        msg = f"Love you {person_name} <:ganyulove:1185601264399159367>"
    elif rand_int == 2:
        msg = f"Love you {person_name} <:klee_hug:1068801227917381652>"
    else:
        msg = f"Love you {person_name} <:clara_heart:1163509399579537439>"

    await interaction.response.send_message(msg)


@bot.tree.command(name="aboutme", description="Sucrose tells more details about herself", guild=discord.Object(id=GUILD_ID))
async def aboutme(interaction: discord.Interaction):
    quotes = [
        "If you're busy, please don't let me stand in the way of progress. ...You're not busy? Really? It's fine, I—I get that you have stuff to do. I'm already quite used to working alone. ...You're truly not busy? I—In that case, I don't suppose you could help me with a few things? Or, you know, we could sit and chat about... stuff.",
        "Let me tell you a little secret, something I've never told anyone. The purpose behind my research is to create my own wonderland. Yes... just like the ones in fairy tales. The kind where all your dreams come true and you live happily ever after. Hehe, it's childish, isn't it? But, I still believe in fairy tales.",
        "Oh, you, ahh... noticed. My ears are a hereditary feature... quite different from everyone else's. So, I try to hide them with my hair as much as possible."
    ]
    await interaction.response.send_message(random.choice(quotes))


@bot.tree.command(name="artifact_value", description="Sucrose will judge your artifact CV", guild=discord.Object(id=GUILD_ID))
async def artifact_value(
    interaction: discord.Interaction,
    main_stat: float,
    crit_rate: float,
    crit_damage: float
):
    if main_stat <= 0 or crit_rate <= 2 or crit_damage <= 0:
        await interaction.response.send_message(
            "Sucrose says these stats don't look right, please check again traveller."
        )
        return

    cr = min(crit_rate, 100) / 100
    cd = crit_damage / 100
    result = round(main_stat * (1 + cr * cd), 2)

    await interaction.response.send_message(
        f"CV is {result} - for stats {main_stat},{crit_rate},{crit_damage}"
    )
# ---------------- SLASH COMMANDS Games----------------
@bot.tree.command(
    name="rps",
    description="Play Rock Paper Scissors",
    guild=discord.Object(id=GUILD_ID)
)
async def rps(interaction: discord.Interaction, opponent: discord.User | None = None):
    view = RPSView(interaction.user, opponent)
    await interaction.response.send_message(
        "Choose your move!", view=view
    )

@bot.tree.command(
    name="tictactoe",
    description="Play Tic Tac Toe with another user",
    guild=discord.Object(id=GUILD_ID)
)
async def tictactoe(interaction: discord.Interaction, opponent: discord.User):
    if opponent.bot:
        await interaction.response.send_message("You cannot play with bots!")
        return

    view = TicTacToeView(interaction.user, opponent)
    await interaction.response.send_message(
        f"Tic Tac Toe!\n❌ {interaction.user.display_name} vs ⭕ {opponent.display_name}\n"
        f"**{interaction.user.display_name} goes first**",
        view=view
    )

@bot.tree.command(
    name="poll",
    description="Create a poll",
    guild=discord.Object(id=GUILD_ID)
)
async def poll(
    interaction: discord.Interaction,
    question: str,
    options: str
):
    option_list = [opt.strip() for opt in options.split(",")]
    await create_poll(interaction, question, option_list)

@bot.tree.command(
    name="pick",
    description="Randomly pick one option",
    guild=discord.Object(id=GUILD_ID)
)
async def pick(
    interaction: discord.Interaction,
    options: str
):
    option_list = [opt.strip() for opt in options.split(",")]
    await pick_option(interaction, option_list)

# ---------------- SLASH COMMANDS LLM Persona Management----------------
@bot.tree.command(name="persona_list", description="List all personas", guild=discord.Object(id=GUILD_ID))
async def persona_list(interaction: discord.Interaction):
    personas = list_personas()

    if not personas:
        await interaction.response.send_message("No personas created yet.")
        return

    await interaction.response.send_message(
        "🎭 **Personas:**\n" + "\n".join(f"- {p}" for p in personas),
        ephemeral=True
    )
    
@bot.tree.command(
    name="persona_cleanup",
    description="Delete the last N personas",
    guild=discord.Object(id=GUILD_ID)
)
async def persona_cleanup(
    interaction: discord.Interaction,
    count: int = 5,
):
    delete_last_n(count)
    await interaction.response.send_message(
        f"🧹 Deleted last **{count}** personas.",
        ephemeral=True
    )

@bot.tree.command(
    name="persona_set",
    description="Set or create a character persona",
    guild=discord.Object(id=GUILD_ID),
)
async def persona_set(
    interaction: discord.Interaction,
    character: str,
    context: str = "fictional character",
):
    await interaction.response.defer(thinking=True)

    try:
        persona_prompt = await generate_persona(character, context)
        set_persona(character, context, persona_prompt)

        await interaction.followup.send(
            f"✅ Persona **{character}** set!\n\n"
            f"```{persona_prompt}```"
        )
    except Exception:
        await interaction.followup.send(
            "❌ Failed to generate persona. Try again later."
        )

@bot.tree.command(
    name="persona_reset",
    description="Reset a persona so it can be regenerated",
    guild=discord.Object(id=GUILD_ID),
)
async def persona_reset(
    interaction: discord.Interaction,
    character: str,
):
    if not get_persona(character):
        await interaction.response.send_message(
            "That persona does not exist.", ephemeral=True
        )
        return

    reset_persona(character)
    await interaction.response.send_message(
        f"🔄 Persona **{character}** has been reset."
    )
# ---------------- SLASH COMMANDS LLM Calls----------------
@bot.tree.command(
    name="ask",
    description="Ask a question using a persona",
    guild=discord.Object(id=GUILD_ID),
)
async def ask(
    interaction: discord.Interaction,
    question: str,
    persona: str = "sucrose",
    context: str | None = None,
    fast: bool = False,
):
    await interaction.response.defer(thinking=True)

    answer = await ask_llm(question, persona=persona, context=context, fast=fast)

    # if len(answer) > 1800:
    #     answer = answer[:1800] + "..."

    await interaction.followup.send(f"**Question:** {question}\n**{persona}'s Answer:** {answer}")


# @bot.tree.command(name="clear", description="Clears messages", guild=discord.Object(id=GUILD_ID))
# async def clear(interaction: discord.Interaction, count: int):
#     if count > 10:
#         await interaction.response.send_message("Too much work T_T, try less than 10")
#         return
#     if count <= 0:
#         await interaction.response.send_message("Please enter a valid number")
#         return

#     deleted = await interaction.channel.purge(limit=count)
#     await interaction.response.send_message(f"Cleared {len(deleted)} messages", delete_after=5)


# ---------------- RUN ----------------
bot.run(TOKEN)
