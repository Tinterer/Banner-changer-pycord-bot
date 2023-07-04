import datetime
import discord
import os

from discord.ext import tasks
from discord.utils import get
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} запущен и готов к использованию')
    change_banner.start()

@tasks.loop(minutes = 10)
async def change_banner():
    guild = bot.get_guild(891345145713270854)
    main_channel = bot.get_channel(891367331727564821) #общий чат
    flud_channel = bot.get_channel(966744691372597248) #флудилка
    cmnds_channel = bot.get_channel(1038011786105995275) #команды
    brmld_channel = bot.get_channel(1038011856108929094) #казино

    image = Image.open('banner.png')

    draw = ImageDraw.Draw(image)

    one_month = datetime.datetime.utcnow() - datetime.timedelta(days = 30)

    mes_cnt_main_channel = 0
    mes_cnt_flud_channel = 0
    mes_cnt_cmnds_channel = 0
    mes_cnt_brmld_channel = 0

    print('Start counting...')

    async for _ in main_channel.history(after = one_month, limit = None):
        mes_cnt_main_channel += 1

    print('pass 1')
    
    async for _ in flud_channel.history(after = one_month, limit = None):
        mes_cnt_flud_channel += 1
    
    print('pass 2')
    
    async for _ in cmnds_channel.history(after = one_month, limit = None):
        mes_cnt_cmnds_channel += 1
    
    print('pass 3')

    async for _ in brmld_channel.history(after = one_month, limit = None):
        mes_cnt_brmld_channel += 1

    print('Point 1 passed✅')

    message_count = mes_cnt_main_channel + mes_cnt_flud_channel + mes_cnt_cmnds_channel + mes_cnt_brmld_channel

    print('Point 2 passed✅')

    font = ImageFont.truetype('DynaPuff-Medium.ttf', size = 150)
    draw.text((527, 705), f'{message_count}', '#8D17BA', font = font)

    font = ImageFont.truetype('DynaPuff_Medium.ttf', size = 150)
    draw.text((1250, 705), f'{guild.member_count}', '#8D17BA', font = font)

    print('pass 5')

    image.save('stats_banner.png')
    print('Image is saved')
    with open('stats_banner.png', 'rb') as f:
        new_banner = f.read()
    await guild.edit(banner = new_banner)
    print('Final point passed✅')

bot.run(os.getenv('TOKEN'))