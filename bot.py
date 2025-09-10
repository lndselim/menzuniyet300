# bot.py
import discord
from discord.ext import commands
from discord.ui import View, Button, Select
import json

from confing import PREFIX

# Botu başlat
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Örnek veri tabanı (JSON formatında saklanecak)
with open("kariyer.json", "r", encoding="utf-8") as f:
    career_data = json.load(f)

    
# basit örnek bot
@bot.command()
async def kariyer(ctx):
    view = CareerView()
    await ctx.send("Kariyerini keşfetmek için bir kategori seç! ", view=view)


# Butonlar ve menüler
class CareerView(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Kategoriler
        self.add_item(CareerSelect())


class CareerSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Teknoloji", description="Yazılım, oyun geliştirme, yapay zeka"),
            discord.SelectOption(label="Sanat", description="Müzik, tasarım, görsel sanatlar"),
            discord.SelectOption(label="İş Dünyası", description="Girişimcilik, finans, yönetim"),
            discord.SelectOption(label="Eğitim", description="Öğretmenlik, rehberlik, danışmanlık"),
        ]
        super().__init__(placeholder="Bir kategori seç ", options=options)

    async def callback(self, interaction: discord.Interaction):
        secim = self.values[0]
        öneriler = career_data.get(secim, [])
        if öneriler:
            msg = f"**{secim} alanında bazı kariyer yolları:**\n"
            for o in öneriler:
                msg += f"- {o}\n"
        else:
            msg = f"Şu an için {secim} kategorisinde öneri yok."
        await interaction.response.send_message(msg, ephemeral=True)
