import discord
from config import TOKEN


intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'giriş yapıldı {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('sa ben aura sen DİSCORD BOTUNU DENEMEDİN Mİ?')

    if message.content == "$hepsini-sil":
        if not message.channel.permissions_for(message.author).manage_messages:
            await message.channel.send("❌ Bu işlemi yapmaya yetkin yok.")
            return

        await message.channel.send("⚠️ Mesajlar siliniyor...")

        try:
            deleted = await message.channel.purge(limit=1000)
            await message.channel.send(f"✅ {len(deleted)} mesaj başarıyla silindi.")
        except discord.Forbidden:
            await message.channel.send("❌ Yetkim yok, mesajları silemiyorum.")
        except discord.HTTPException as e:
            await message.channel.send(f"⚠️ Hata oluştu: {e}")
client.run(TOKEN)


