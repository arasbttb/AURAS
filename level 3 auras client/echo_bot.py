import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)
# ➕ Toplama yapan sınıf
class Add:
    def __init__(self, sayi1, sayi2):
        self.sayi1 = sayi1
        self.sayi2 = sayi2

    def topla(self):
        return self.sayi1 + self.sayi2
# 📚 Toplama komutu
@client.command()
async def toplama(ctx, sayi1: int, sayi2: int):
    toplam = Add(sayi1, sayi2)
    await ctx.send(f"➕ Toplam: {toplam.topla()}")
# 🚘 Car sınıfı
class Car:
    def __init__(self, marka, renk):
        self.marka = marka.capitalize()
        self.renk = renk.capitalize()

    def info(self):
        return f"🚘 Bu araba bir {self.renk} renkli {self.marka}."

# 🔔 Bot açıldığında
@client.event
async def on_ready():
    print(f"✅ Giriş yapıldı: {client.user}")

# 📸 Mesaj işleyici
@client.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    # Görsel tepkisi
    if message.attachments:
        for attachment in message.attachments:
            if any(ext in attachment.url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                await message.channel.send("📸 Vay canına! Ne güzel bir fotoğraf!")
                break

    await client.process_commands(message)  # Komutları işlemeyi unutma!

# 👋 /hello komutu
@client.command()
async def hello(ctx):
    await ctx.send("👋 Sa ben Aura! Sen Discord botunu denemedin mi?")

# 🧹 /hepsini_sil komutu
@client.command()
async def hepsini_sil(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_messages:
        await ctx.send("❌ Bu işlemi yapmaya yetkin yok.")
        return

    await ctx.send("⚠️ Mesajlar siliniyor...")

    try:
        deleted = await ctx.channel.purge(limit=1000)
        await ctx.send(f"✅ {len(deleted)} mesaj başarıyla silindi.")
    except discord.Forbidden:
        await ctx.send("❌ Yetkim yok, mesajları silemiyorum.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠️ Hata oluştu: {e}")

# 🚗 /car komutu
@client.command()
async def car(ctx, renk: str, marka: str):
    araba = Car(marka, renk)
    await ctx.send(araba.info())

# 🔎 Diğer bilgi komutları
@client.command()
async def about(ctx):
    await ctx.send("📌 Bu bot, discord.py kütüphanesi ile yapılmıştır!")

@client.command()
async def info(ctx):
    await ctx.send("/about → Bot hakkında bilgi verir.\n🤨 Eğlenceli ve etkileşimli bir bot!")

# 🚨 Hatalı komut kullanımı durumunda bilgilendir
@car.error
async def car_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Doğru kullanım: `/car <renk> <marka>` — Örnek: `/car siyah bmw`")

client.run(TOKEN)


