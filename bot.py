import discord
from discord import app_commands
import json

TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open("skins.json", "r", encoding="utf-8") as f:
    skins = json.load(f)

heroes = sorted(skins.keys())

# Lưu trạng thái chọn tướng
# {user_id: [hero1, hero2, ...]}
user_choose_state = {}

# ---------- SLASH COMMAND ----------

@tree.command(name="choose", description="Chon tuong bang cach nhap ten hoac so")
async def choose(interaction: discord.Interaction):
    user_choose_state[interaction.user.id] = heroes
    await interaction.response.send_message(
        "Nhap ten tuong hoac go '.' de hien danh sach",
        ephemeral=True
    )

# ---------- MESSAGE HANDLER ----------

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    uid = message.author.id
    if uid not in user_choose_state:
        return

    content = message.content.strip().lower()
    hero_list = user_choose_state[uid]

    # In toàn bộ danh sách tướng
    if content == ".":
        text = "Danh sach tuong:\n\n"
        for i, hero in enumerate(hero_list, start=1):
            text += f"{i}. {hero}\n"

        text += "\nNhap so thu tu de chon tuong"
        await message.reply(text)
        return

    # Chọn theo số
    if content.isdigit():
        index = int(content) - 1
        if index < 0 or index >= len(hero_list):
            await message.reply("So khong hop le")
            return

        hero = hero_list[index]
        hero_skins = skins[hero]

        text = f"Skin cua {hero}:\n\n"
        for sid, name in hero_skins.items():
            text += f"{name} (ID: {sid})\n"

        await message.reply(text)
        del user_choose_state[uid]
        return

    # Tìm theo tên (lọc danh sách)
    filtered = [h for h in heroes if content in h.lower()]
    if not filtered:
        await message.reply("Khong tim thay tuong phu hop")
        return

    user_choose_state[uid] = filtered

    text = "Danh sach tuong phu hop:\n\n"
    for i, hero in enumerate(filtered, start=1):
        text += f"{i}. {hero}\n"

    text += "\nNhap so thu tu de chon tuong"
    await message.reply(text)

# ---------- READY ----------

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot dang online: {client.user}")

client.run(TOKEN)
