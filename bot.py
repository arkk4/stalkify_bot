import discord
from discord.ext import commands
from faker import Faker
from faker_stalker_names.uk_UA import Provider as StalkerNamesProvider
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

fake = Faker()
fake.add_provider(StalkerNamesProvider)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Синхронізація слешевих команд
    print(f'Bot {bot.user} is ready!')

@bot.tree.command(name='stalkify')
@discord.app_commands.describe(
    name_type='Тип імені (повне або прізвище)',
    fraction='Фракція (сталкер або бандит)'
)
@discord.app_commands.choices(
    name_type=[
        discord.app_commands.Choice(name='Повне ім\'я', value='full'),
        discord.app_commands.Choice(name='Прізвище', value='last')
    ],
    fraction=[
        discord.app_commands.Choice(name='Сталкер', value='stalker'),
        discord.app_commands.Choice(name='Бандит', value='bandit')
    ]
)
async def stalkify(interaction: discord.Integration, name_type: str = 'last', fraction: str = ''):
    if name_type == 'full':
        name = fake.stalker_name(name_type=fraction) if fraction else fake.stalker_name()
    else:
        last_name = fake.stalker_last_name(name_type=fraction) if fraction else fake.stalker_last_name()
        user_roles = [role.name for role in interaction.user.roles]
        if user_roles:
            latest_role = user_roles[-1]
            name = f"{latest_role} {last_name}"
        else:
            name = last_name
    
    try:
        await interaction.user.edit(nick=name)
        await interaction.response.send_message(f'Твоє нове ім\'я сталкера: {name}')
    except discord.HTTPException as e:
        error_message = e.text
        error_code = e.code
        print(f"Error {error_code}: {error_message}")
        await interaction.response.send_message(f"Виникла помилка: {error_code} - {error_message}")

bot.run(DISCORD_BOT_TOKEN)