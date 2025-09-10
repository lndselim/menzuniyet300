# bot.py
import os
import json
import sys
import discord
from discord.ext import commands
from discord.ui import View
from config import TOKEN, PREFIX  # config.py'den al

# Basit çalışma dizini / dosya kontrolü — hata ayıklama için
print("Çalışma dizini:", os.getcwd())
print("Klasördeki dosyalar:", os.listdir())

# Kariyer verisini yükle
try:
    with open("kariyer.json", "r", encoding="utf-8") as f:
        career_data = json.load(f)
    print("kariyer.json başarıyla yüklendi. Kategoriler:", list(career_data.keys()))
except Exception as e:
    print("HATA: kariyer.json yüklenemedi:", repr(e))
    sys.exit(1)

# Bot başlatma
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ---- Select Menüsü ----
class CareerSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Teknoloji", description="Yazılım, oyun geliştirme, yapay zeka"),
            discord.SelectOption(label="Sanat", description="Müzik, tasarım, görsel sanatlar"),
            discord.SelectOption(label="İş Dünyası", description="Girişimcilik, finans, yönetim"),
            discord.SelectOption(label="Eğitim", description="Öğretmenlik, rehberlik, danışmanlık"),
        ]
        super().__init__(placeholder="Bir kategori seç...", options=options, min_values=1, max_values=1)

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


# ---- View ----
class CareerView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CareerSelect())

# ---- Komutlar ----
@bot.command()
async def kariyer(ctx):
    """Kariyer seçim menüsünü açar."""
    view = CareerView()
    await ctx.send("Kariyerini keşfetmek için bir kategori seç!", view=view)

@bot.command()
async def jsonkontrol(ctx):
    """Bot içinden JSON anahtarlarını gösterir (debug)."""
    await ctx.send(f"Kategoriler: {', '.join(career_data.keys())}")

# Botu çalıştır
bot.run(TOKEN)