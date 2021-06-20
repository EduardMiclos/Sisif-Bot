# PYTHON PROJECT - DISCORD BOT, SISIF
# AUTHOR: MICLOȘ EDUARD-PAVEL


# ------------- IMPORTS -------------

import discord
from discord.ext import commands
import codecs
import random
from reddit_extractor import MEMES, JOKES, NEWS
from google_sheets import write_date
from google_sheets import update_week
from google_sheets import exams
# -----------------------------------





# ------------- SELECTARE PREFIX COMENZI SI TOKEN -------------

client = commands.Bot(command_prefix='.')
BOT_TOKEN = ''
REPORTS_CHANNEL = ''
# -------------------------------------------------------------





# ------------- LINK-URI UTILE -------------

class Links:
    fb_link = '###'
    tutoriere = '###'
    calendar = '###'
    drives = {}
    cursuri = {}

Links.drives["info"] ='###'
Links.drives["ipc"] = '###'
Links.drives["fc"] ='###'

Links.cursuri["tp"] = '###'
Links.cursuri["microeconomie"] = '###'
Links.cursuri["ms"] = '###'

LINK_ORAR = '###'

# ------------------------------------------





# ------------- CINE POATE FOLOSI BOT-UL -------------

ROLES = ['Andrei', 'Sefu La Grupa', 'Certified Meme Expert', 'Grupa 1', 'Grupa 2', 'Grupa 3', 'Duamna Profesoară', 'DJ', 'Vik']
SPECIAL_ROLES = ['Andrei', 'Sefu La Grupa']

# ----------------------------------------------------






# ------------- EVENTS -------------

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name = "Rolling Stones"))
    print('Sisif, la dispoziția dumitale.')

@client.event
async def on_member_join(member):
    print(f'{member} s-a alăturat server-ului!')

# ----------------------------------






# ------------- ERROR HANDLING -------------

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Te rog sa introduci toate argumentele comenzii.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Nu înțeleg, maestre.")
    elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Îmi pare rău, nu ascult de tine.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Nu ești stăpânul meu, Micloș este.")
    elif isinstance(error, commands.BotMissingRole):
        await ctx.send("Îmi pare rău. Sunt în starea de debugging și nu răspund la comenzi.")

# ------------------------------------------





# ------------- TEHNICE ȘI ADMINISTRATIVE -------------

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*SPECIAL_ROLES)
async def ping(ctx):
        await ctx.send(f'Ping = {round(client.latency * 1000)} ms')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*SPECIAL_ROLES)
async def calendar(ctx, *, txt):
    if not write_date(txt):
        await ctx.send('Stăpânul a introdus o dată incorectă.')
    else:
        await ctx.send('Calendarul a fost actualizat.')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*SPECIAL_ROLES)
async def updateweek(ctx):
    if update_week():
        await ctx.send('Saptămâna curentă a fost actualizată.')
    else:
        await ctx.send('Încă nu e timpul să actualizăm săptămâna.')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*SPECIAL_ROLES)
async def info(ctx, *, member: discord.Member):
    crated_at = member.joined_at.strftime("%d.%m.%Y")
    roles = len(member.roles) - 1
    txt = f'{member} s-a alaturat server-ului in data de {crated_at} și ';
    if roles == 0:
        txt+= 'nu are roluri special.'
    elif roles == 1:
        txt+= 'are un rol special.'
    else:
        txt+= f'are {roles} roluri speciale.'

    await ctx.send(txt)

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def report(ctx, reported_member: discord.Member, *, msg=''):
    channel = client.get_channel(int(REPORTS_CHANNEL))
    author = ctx.author
    text = 'Autor: **' + str(author) + '**\n' + 'Membru raportat: **' + str(reported_member) + '\n**Motiv: *'
    if '~' in msg:
        (reason, evidence) = msg.split('~')
        text += reason + '*\nDovada: *' + evidence + '*\n'
    else:
        reason = msg
        text += reason + '*'

    await channel.send(text)
    await ctx.send(f'Membrul **{reported_member}** a fost raportat. Motiv: *{reason}*\nUn admin va analiza situația.')


@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*SPECIAL_ROLES)
async def kick(ctx, member: discord.Member, *, motiv=''):
    await member.kick(reason = motiv)
    await ctx.send(f'La voia maestrului, **{member}** a primit kick.')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*SPECIAL_ROLES)
async def ban(ctx, member: discord.Member, *, motiv=''):
    await member.ban(reason = motiv)
    await ctx.send(f'La voia maestrului, **{member}** a primit ban.')

# -----------------------------------






# ------------- MANIPULARE FISIERE -------------

with codecs.open('Credentials.txt', 'r', 'utf-8') as f:
    (BOT_TOKEN, REPORTS_CHANNEL) = f.readlines()
    f.close()

# ---------------------------------------------






# ------------- FUNCTII AUXILIARE -------------

def binary_search(name):

    with open('studenti_INFO.txt', 'r+', encoding='utf-8') as f:
        lines = f.readlines()

        left = 0
        right = len(lines) - 1

        while left <= right:
            mid = int((left+right)/2)
            line_split = lines[mid].split('1A')
            first_name__second_name = line_split[0]
            group = line_split[1]

            if name in first_name__second_name:
                return first_name__second_name + ' - grupa: 1A' + group
            elif name > first_name__second_name:
                left = mid + 1
            else:
                right = mid - 1

    f.close()
    return 'Nu am găsit, maiestre'

# ------------------------------------






# ------------- RASPUNSURI UZUALE-------------

@client.command(aliases=['fb'])
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def facebook(ctx):
    await ctx.send(f'Link-ul grupului de facebook este: {Links.fb_link}')
    await ctx.send('Detalii pe canalul `linkuri-utile` ')


@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def drives(ctx, drive):
    if drive.upper() == 'INFO' or drive.upper() == 'IPC' or drive.upper() == 'FC':
        await ctx.send(Links.drives[drive])
        await ctx.send('Detalii pe canalul `linkuri-utile` ')


@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def student(ctx, *, name):
    txt = binary_search(name.upper())
    await ctx.send(txt)


@client.command(aliases=['incoming'])
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def sesiune(ctx):
    EXAMS = exams()
    if EXAMS:
        await ctx.send('Examenele programate săptămâna aceasta și săptămâna viitoare:')
        for (date, info) in EXAMS:
            await ctx.send(f'** {date} **')
            await ctx.send(info)
    else:
        await ctx.send('Nu avem examene în săptămâna aceasta.')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def program(ctx):
    await ctx.send(f'Puteți accesa programul aici: {Links.calendar}')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def lider(ctx, *, indice_grupa:int):
    if int(indice_grupa) == 1:
        await ctx.send('Liderul grupei 1 este Berechet Ion-Lucian.')
    elif int(indice_grupa) == 2:
        await ctx.send('Liderul grupei 2 este Micloș Eduard-Pavel.')
    elif int(indice_grupa) == 3:
        await ctx.send('Liderul grupei 3 este Preda Octavian.')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def sef(ctx):
    await ctx.send("Șeful de an este Balea Andrei-Petru. Dar stăpânul meu rămâne Micloș. ")


@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def link(ctx, *, materie):
    if materie in Links.cursuri:
        await ctx.send(f'Link: {Links.cursuri[materie]}')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def tutoriere(ctx):
    await ctx.send(f'Link-ul grupului de tutoriere este: {Links.tutoriere}')
    await ctx.send('Detalii pe canalul `linkuri-utile` ')

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def orar(ctx):
    await ctx.send('Link orar: ' + LINK_ORAR);

@client.command()
@commands.bot_has_role('Functional')
@commands.has_any_role(*ROLES)
async def poke(user: discord.User, *, message=None):
    print(user)
    await user.send(message)

LAST_MEMES = []
@client.command()
@commands.bot_has_role('Functional')
async def meme(ctx):
    global LAST_MEMES

    rnd = random.randrange(0, len(MEMES)-1, 1)

    # Impiedica repetarea ultimelor meme-uri.
    while rnd in LAST_MEMES:
        rnd = random.randrange(0, len(MEMES), 1)

    if len(LAST_MEMES) > len(MEMES)/2:
        LAST_MEMES = []

    LAST_MEMES.append(rnd)
    await ctx.send(MEMES[rnd])


LAST_JOKES = []
@client.command()
@commands.bot_has_role('Functional')
async def joke(ctx):
    global LAST_JOKES

    rnd = random.randrange(0, len(JOKES) - 1, 1)

    # Impiedica repetarea ultimelor bancuri.
    while rnd in LAST_JOKES:
        rnd = random.randrange(0, len(JOKES), 1)

    if len(LAST_JOKES) > len(JOKES) / 2:
        LAST_JOKES = []

    LAST_JOKES.append(rnd)

    text = '**' + JOKES[rnd][0] + '**' + '\n' + JOKES[rnd][1]
    await ctx.send(text)

LAST_NEWS = []
@client.command(aliases=['news', 'stiri'])
@commands.bot_has_role('Functional')
async def noutati(ctx):
    global LAST_NEWS

    rnd = random.randrange(0, len(NEWS) - 1, 1)

    # Impiedica repetarea ultimelor noutati.
    while rnd in LAST_NEWS:
        rnd = random.randrange(0, len(NEWS), 1)

    if len(LAST_NEWS) > len(NEWS) / 2:
        LAST_NEWS = []

    LAST_NEWS.append(rnd)

    text = '**' + NEWS[rnd][0] + '**' + '\nLINK: ' + '<' + NEWS[rnd][1] + '>'
    await ctx.send(text)


@client.command()
@commands.bot_has_role('Functional')
@commands.is_owner()
async def stapan(ctx):
    await ctx.send('Tu ești stăpânul meu!')

# --------------------------------------





# ------------- TESTING ----------------------
# --------------------------------------------





# ------------- CONECTARE LA API -------------

client.run(BOT_TOKEN)

# --------------------------------------------

