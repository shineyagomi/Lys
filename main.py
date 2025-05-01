import discord
from discord.ext import commands
from discord import app_commands
import json
from flask import Flask
from threading import Thread

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
GUILD_ID = 1364561849399378021  # テスト時のみ使用

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@tree.command(
    name="setup_panel",
    description="認証スタートパネルを表示します",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.checks.has_permissions(administrator=True)
async def setup_panel(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("このコマンドはサーバー内でのみ使用できます。", ephemeral=True)
        return

    embed = discord.Embed(
        title="取引認証スタート",
        description="このBotで取引を始めるには、まず本人認証が必要です。\n下のボタンをタップして認証を開始してください。",
        color=discord.Color.green()
    )
    view = StartVerificationView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("認証パネルを表示しました。", ephemeral=True)

class StartVerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ 認証スタート", style=discord.ButtonStyle.success)
    async def start_verification(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.user.send("こんにちは！本人認証を開始します。\n売り手 or 買い手の情報を入力してください。")
        # ここでDMに選択ボタン or Modal を送る（今後追加）

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Bot起動：{bot.user.name}")

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
bot.run(TOKEN)
