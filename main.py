# PYTHON PROJECT - DISCORD BOT, SISIF
# AUTHOR: MICLOȘ EDUARD-PAVEL


# ------------- IMPORTS -------------

import discord
from discord.ext import commands
import xlrd

# -----------------------------------






# ------------- SELECTARE PREFIX COMENZI SI TOKEN -------------

client = commands.Bot(command_prefix='.')
BOT_TOKEN = '##############'

# -------------------------------------------------------------






# ------------- LINK-URI UTILE -------------

class Links:
    fb_link = '##############'
    drives = {}
    cursuri = {}

Links.drives["info"] ='Drive-ul nostru: ##############'
Links.drives["ipc"] = 'Drive IPC: ##############'
Links.drives["fc"] ='Drive FC: ##############'

Links.cursuri["ipc"] = '##############'
Links.cursuri["fc"] = '##############'

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
        await ctx.send("Nu înțeleg, maiestre.")
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send("Îmi pare rău, nu ascult de tine.")

# ------------------------------------------






# ------------- TEHNICE ȘI ADMINISTRATIVE -------------

@client.command()
@commands.has_any_role(*SPECIAL_ROLES)
async def ping(ctx):
        await ctx.send(f'Ping = {round(client.latency * 1000)} ms')

@client.command()
@commands.has_any_role(*SPECIAL_ROLES)
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

@client.command()
@commands.has_any_role(*SPECIAL_ROLES)
async def kick(ctx, member: discord.Member, *, motiv=''):
    await member.kick(reason = motiv)
    await ctx.send(f'La voia maiestrului, {member} a primit kick.')

@client.command()
@commands.has_any_role(*SPECIAL_ROLES)
async def ban(ctx, member: discord.Member, *, motiv=''):
    await member.ban(reason = motiv)
    await ctx.send(f'La voia maiestrului, {member} a primit ban.')

@client.command()
@commands.has_any_role(*SPECIAL_ROLES)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for entry in banned_users:
        user = entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f'La voia maiestrului, {user.name}#{user.discriminator} a primit unban. ')

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
    return ctx.author.id == ##############

# ------------------------------------





# ------------- RASPUNSURI UZUALE-------------

@client.command(aliases=['fb'])
@commands.has_any_role(*ROLES)
async def facebook(ctx):
    await ctx.send(f'Link-ul grupului de facebook este: {Links.fb_link}')



@client.command()
@commands.has_any_role(*ROLES)
async def drives(ctx, drive):
    if drive.upper() == 'INFO' or drive.upper() == 'IPC' or drive.upper() == 'FC':
        await ctx.send(Links.drives[drive])


@client.command()
@commands.has_any_role(*ROLES)
async def student(ctx, *, name):
    txt = search(name.upper())
    await ctx.send(txt)


@client.command(aliases=['teste', 'examene'])
@commands.has_any_role(*ROLES)
async def incoming(ctx):
    await ctx.send(incoming_text)


@client.command()
@commands.has_any_role(*ROLES)
async def lider(ctx, *, indice_grupa:int):
    if int(indice_grupa) == 1:
        await ctx.send('Liderul grupei 1 este Berechet Lucian-Ion.')
    elif int(indice_grupa) == 2:
        await ctx.send('Liderul grupei 2 este Micloș Eduard-Pavel.')
    elif int(indice_grupa) == 3:
        await ctx.send('Liderul grupei 3 este Preda Octavian.')

@client.command()
@commands.has_any_role(*ROLES)
async def sef(ctx):
    await ctx.send("Șeful de an este Balea Andrei-Petru. Dar stăpânul meu rămâne Micloș.")


@client.command()
@commands.has_any_role(*ROLES)
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
