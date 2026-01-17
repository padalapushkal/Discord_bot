import discord

HELP_CATEGORIES = {
    "ai": {
        "title": "🧠 AI & Chat",
        "commands": [
            "`/ask` – Ask a question using a persona",
            "`/ask fast:true` – Faster, cheaper AI response",
        ]
    },
    "personas": {
        "title": "🎭 Personas",
        "commands": [
            "`/persona_set` – Create or regenerate a persona",
            "`/persona_reset` – Reset a persona",
            "`/persona_list` – List all personas",
            "`/persona_cleanup` – Delete last N personas",
            "_Personas are auto-created on first use_",
        ]
    },
    "games": {
        "title": "🎮 Games",
        "commands": [
            "`/rps` – Rock Paper Scissors",
            "`/tictactoe` – Tic Tac Toe",
        ]
    },
    "social": {
        "title": "🗳️ Social & Fun",
        "commands": [
            "`/poll` – Create a poll",
            "`/pick` – Picker wheel",
        ]
    },
    "utils": {
        "title": "🛠 Utilities",
        "commands": [
            "`/clear` – Delete messages",
            "`/stats` – View game stats",
        ]
    },
    "fun": {
        "title": "🌸 Personality",
        "commands": [
            "`/sayhello` – Friendly greeting",
            "`/sayloveyou` – Send love",
            "`/aboutme` – Learn about the bot",
        ]
    }
}


def build_help_embed(category: str | None = None) -> discord.Embed:
    embed = discord.Embed(
        title="🌸 Sucrose Help",
        description=(
            "H-hello! I can chat using different personas, host games, "
            "run polls, and help with decisions.\n\n"
            "Use `/help category:<name>` to explore a category."
        ),
        color=discord.Color.blurple()
    )

    if category:
        key = category.lower()
        data = HELP_CATEGORIES.get(key)

        if not data:
            embed.add_field(
                name="❌ Unknown category",
                value="Available categories:\n"
                      "`ai`, `personas`, `games`, `social`, `utils`, `fun`",
                inline=False
            )
            return embed

        embed.add_field(
            name=data["title"],
            value="\n".join(data["commands"]),
            inline=False
        )
        return embed

    # Show all categories
    for data in HELP_CATEGORIES.values():
        embed.add_field(
            name=data["title"],
            value="\n".join(data["commands"]),
            inline=False
        )

    embed.set_footer(text="Tip: Try /help category:personas")
    return embed
