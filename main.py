# PYTHON PROJECT - DISCORD BOT, SISIF
# AUTHOR: MICLOȘ EDUARD-PAVEL


# ------------- IMPORTS -------------

import discord
from discord.ext import commands
import xlrd

# -----------------------------------






# ------------- SELECTARE PREFIX COMENZI SI TOKEN -------------

client = commands.Bot(command_prefix='.')
BOT_TOKEN = '#######################'

# -------------------------------------------------------------






# ------------- LINK-URI UTILE -------------

class Links:
    fb_link = 'https://www.facebook.com/groups/323385562186944/about'
    drives = {}
    cursuri = {}


Links.drives["info"] ='Drive-ul nostru: https://drive.google.com/drive/folders/1MjE9FocU4ZZor5TITJD7grgZILZH_FN-?usp=sharing'
Links.drives["ipc"] = 'Drive IPC: https://docs.google.com/spreadsheets/d/1ndI8qUHxgtKdZFs6CT2IRVecYZGuVMOLr5JUzYktVWc/edit#gid=0'
Links.drives["fc"] ='Drive FC: https://drive.google.com/drive/folders/1p7wi23muoQevyHvvP7tg0FmC4G0bCI7d'

Links.cursuri["ipc"] = 'https://upt-ro.zoom.us/j/95060505628'
Links.cursuri["fc"] = 'https://zoom.us/j/4646489463?pwd=TFVYd2dGWnMwWFhBckN3TENPOEJsQT09'

# ------------------------------------------




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
        await ctx.send("Nu înțeleg, maiestre.")

# ------------------------------------------







# ------------- TEHNICE -------------

@client.command()
async def ping(ctx):
        await ctx.send(f'Ping = {round(client.latency * 1000)} ms')

@client.command()
async def info(ctx, *, member: discord.Member):
    crated_at = member.joined_at.strftime("%d.%m.%Y")
    roles = len(member.roles)
    txt = f'{member} s-a alaturat server-ului in data de {crated_at} și ';
    if roles == 0:
        txt+= 'nu are roluri.'
    elif roles == 1:
        txt+= 'are un rol.'
    else:
        txt+= f'are {roles} roluri.'

    await ctx.send(txt)

# -----------------------------------






# ------------- CONECTARE LA EXCEL -------------

path = 'info.xls'
inputWorkboot = xlrd.open_workbook(path)
inputWorksheet = inputWorkboot.sheet_by_index(0)
rows = inputWorksheet.nrows
cols = inputWorksheet.ncols

# -----------------------------------------------







# ------------- MANIPULARE FISIERE -------------

incoming_text = ''

with open('Teste.txt', 'r', encoding='utf-8') as f:
    f.seek(0)
    read = f.read(1)

    if read:
        incoming_text = read + f.read()
    else:
        incoming_text = 'Nu sunt examene, teste sau parțiale în următoarele săptămâni...'

# ---------------------------------------------







# ------------- FUNCTII AUXILIARE -------------


def diacritica(litera):
    return (litera.upper() == 'Ă' or litera.upper() == 'Â' or litera.upper() == 'Î' or litera.upper() == 'Ș' or litera.upper() == 'Ț')


def diacritice(nume):
    sum = 0

    for litera in nume:
        if diacritica(litera):
            sum = sum+1

    return sum



def replace(initial, nume):

    lst_initial = list(initial)
    lst_nume = list(nume)

    for i in range(0, len(nume)):
        if lst_initial[i] == '?':
            lst_initial[i] = lst_nume[i]

    return ''.join(lst_initial)


def search(std_name):

    for r in range(rows):
        search_name = inputWorksheet.row(r)[1]
        search_group = inputWorksheet.row(r)[2]

        if '?' in search_name.value and diacritice(std_name):
            search_name.value = replace(search_name.value, std_name)

        if std_name in search_name.value:
            reply = "Am găsit.\n " + search_name.value + ' - grupa: ' + search_group.value
            return reply
        else:
            reply = "Nu am găsit, stăpâne. Îmi pare rău."

    return reply



def my_lord(ctx):
    return ctx.author.id == 217299692176801794


# ------------------------------------








# ------------- RASPUNSURI -------------


@client.command(aliases=['fb'])
async def facebook(ctx):
    await ctx.send(f'Link-ul grupului de facebook este: {Links.fb_link}')



@client.command()
async def drives(ctx, drive):
    if drive.upper() == 'INFO' or drive.upper() == 'IPC' or drive.upper() == 'FC':
        await ctx.send(Links.drives[drive])


@client.command()
async def student(ctx, *, name):
    txt = search(name.upper())
    await ctx.send(txt)


@client.command(aliases=['teste', 'examene'])
async def incoming(ctx):
    await ctx.send(incoming_text)


@client.command()
async def lider(ctx, *, indice_grupa:int):
    if int(indice_grupa) == 1:
        await ctx.send('Liderul grupei 1 este Berechet Lucian-Ion.')
    elif int(indice_grupa) == 2:
        await ctx.send('Liderul grupei 2 este Micloș Eduard-Pavel.')
    elif int(indice_grupa) == 3:
        await ctx.send('Liderul grupei 3 este Preda Octavian.')


@client.command()
async def link(ctx, *, materie):
    if materie == 'ipc' or materie == 'fc':
        await ctx.send(f'Link: {Links.cursuri[materie]}')


@client.command()
@commands.check(my_lord)
async def stapan(ctx):
    await ctx.send('Tu ești stăpânul meu!')

# --------------------------------------







# ------------- CONECTARE LA API -------------

client.run(BOT_TOKEN)

# --------------------------------------------
