import discord
import json
import random
import asyncio
from discord_components import *
from datetime import datetime, timedelta
from discord.ext import commands

TOKEN = 'OTQ5Mjg3NzMyMjMwOTAxNzgw.YiILGA.HIgjbg_1HCjH0qZCpsSzWAVmv28'
USERS_JSON_PATH = 'D:/Projekty/Python/eco bot/users.json'
TIME_JSON_PATH = 'D:/Projekty/Python/eco bot/time.json'
MAIN_CHANEL = 949282343703691295
LOG_CHANEL = 949286503576657940
PREFIX = '.'

client = commands.Bot(command_prefix= PREFIX)

@client.event
async def on_ready():
    DiscordComponents(client)
    
    print("======================")
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("======================")

# Com-Balance
@client.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    if ctx.channel.id != MAIN_CHANEL: return

    if member == None: user = ctx.author
    else: user = member

    await create_user(user.id)

    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f)

    embed = discord.Embed(color = discord.Color.green())
    embed.set_author(name = user.name, icon_url = user.avatar_url)
    embed.add_field(name ="Portfel:", value = f'$ {data[str(user.id)]["wallet"]}')
    embed.add_field(name ="Bank:", value = f'$ {data[str(user.id)]["bank"]}')
    embed.add_field(name ="Suma:", value = f'$ {data[str(user.id)]["wallet"] + data[str(user.id)]["bank"]}')
    await ctx.send(embed = embed)

# Com-job
@client.command()
async def job(ctx, arg = None):
    if ctx.channel.id != MAIN_CHANEL: return   
    await create_user(ctx.author.id)
    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id
    with open(TIME_JSON_PATH, "r") as tf: time_data = json.load(tf)

    if arg == "help":
        embed = discord.Embed(description = "help menu **|** job <podkomenda>" , color = discord.Color.green())
        embed.set_author(name = client.user.name, icon_url = client.user.avatar_url)
        embed.add_field(name ="quit", value="Opuszcza pracę (musisz posiadać)")
        await ctx.send(embed = embed)
        return

    if data[str(user)]["job"] == "none":
        if arg != None:
            if arg == "drwal": 
                
                data[str(user)]["job"] = "drwal"
                with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)
                
            elif arg == "rybak": 
                
                data[str(user)]["job"] = "rybak"
                with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)

            else: 
                embed = discord.Embed(description = "Nie ma takiej pracy!" , color = discord.Color.green())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                return

            if arg != None:
                job = data[str(user)]["job"]
                embed = discord.Embed(description = f"Twoja nowa praca to {job} **|** Użyj komendy job żeby pracować" , color = discord.Color.green())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                await log(ctx, f"wybrał/a pracę '**{job}**'")
                return

        else:
            embed = discord.Embed(description = "Nie posiadasz pracy, więc wybierz jedną! **|** Użyj komendy job <praca>" , color = discord.Color.green())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            embed.add_field(name ="drwal", value="🪓")
            embed.add_field(name ="rybak", value="🐟")
            await ctx.send(embed = embed)
            return

    if arg == "quit":
        embed = discord.Embed(description = "Odchodzisz z pracy!" , color = discord.Color.green())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        await log(ctx, f"Odchodzi z poracy")
        data[str(user)]["job"] = "none"
        with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)
        return
    
    if data[str(user)]["job"] == "drwal":

        if time_data[str(user)]["work_cld"] != "none":

            json_datetime = datetime.strptime(time_data[str(user)]["work_cld"], '%Y-%m-%d %H:%M:%S.%f')

            if json_datetime > datetime.now():

                dif = json_datetime - datetime.now()

                sec = dif.seconds

                hours = sec//3600
                seconds = sec % 60
                minutes = (sec//60) % 60

                embed = discord.Embed(description = f"Nie możesz pracować przez: **{str(hours)}**h, **{str(minutes)}**m, **{str(seconds)}**s!", color = discord.Color.green())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                return

        time_data[str(user)]["work_cld"] = str(datetime.now() + timedelta(hours = 3.5))

        with open(TIME_JSON_PATH, "w") as tf: json.dump(time_data, tf, indent=4)

        x = random.randint(1,4)
        y = random.randint(1,4)

        if x == 1: l = 'A'
        elif x == 2: l = 'B'
        elif x == 3: l = 'C'
        elif x == 4: l = 'D'

        if y == 4: sum = 0 + x
        elif y == 3: sum = 4 + x
        elif y == 2: sum = 8 + x
        elif y == 1: sum = 12 + x

        embed = discord.Embed(description = "Pracujesz jako drwal" , color = discord.Color.purple())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.add_field(name = f"``{y} | {l}``", value="**4**🌳🌳🌳🌳\n**3**🌳🌳🌳🌳\n**2**🌳🌳🌳🌳\n**1**🌳🌳🌳🌳\n\u1CBC**A** \u1CBC**B** \u1CBC**C** \u1CBC**D**")
        await ctx.send(embed = embed)

        while True:
            message = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            if str(sum) in message.content:
                amount = random.randint(50,150)
                data[str(user)]["wallet"] += amount
                with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)
                embed = discord.Embed(description = f"Pracowałeś i zarobiłeś **$ {amount}**!", color = discord.Color.purple())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                await log(ctx, f"Pracował/a jako drwal i zarobił/a **$ {amount}**")
                return
                
            else:
                embed = discord.Embed(description = "Popełniłeś błąd podczas pracy i nic nie zarobiłeś!", color = discord.Color.red())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                await log(ctx, "Pracował/a jako drwal i nic nie zarobił/a")
                return
        
    if data[str(user)]["job"] == "rybak":

        if time_data[str(user)]["work_cld"] != "none":

            json_datetime = datetime.strptime(time_data[str(user)]["work_cld"], '%Y-%m-%d %H:%M:%S.%f')

            if json_datetime > datetime.now():

                dif = json_datetime - datetime.now()

                sec = dif.seconds

                hours = sec//3600
                seconds = sec % 60
                minutes = (sec//60) % 60

                embed = discord.Embed(description = f"Nie możesz pracować przez: **{str(hours)}**h, **{str(minutes)}**m, **{str(seconds)}**s!", color = discord.Color.green())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                return

        time_data[str(user)]["work_cld"] = str(datetime.now() + timedelta(hours = 3.5))

        with open(TIME_JSON_PATH, "w") as tf: json.dump(time_data, tf, indent=4)

        embed = discord.Embed(description = "Zarzucasz sieć! | jak zobaczysz ryby to je złap!", color = discord.Color.purple())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        em = await ctx.send(embed = embed, components = [])

        await asyncio.sleep(random.randint(30,90))

        while True:
            try:
                await em.edit('', components = [Button(style=ButtonStyle.green, label="Złap!", emoji="🐟")])
                interaction = await client.wait_for("button_click", timeout= random.randint(2,4), check=lambda interaction: interaction.author == ctx.author)

                if interaction:
                    await em.edit('', components = [])
                    amount = random.randint(85,150)
                    data[str(user)]["wallet"] += amount
                    with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)
                    embed = discord.Embed(description = f"Pracowałeś i zarobiłeś **$ {amount}**!", color = discord.Color.green())
                    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = embed)
                    await log(ctx, f"Pracował/a jako rybak i zarobił/a **$ {amount}**")
                    return

            except asyncio.TimeoutError:
                await em.edit('', components = [])
                embed = discord.Embed(description = "Ryby ucieky i nic nie zarobiłeś", color = discord.Color.red())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                await log(ctx, "Pracował/a jako rybak i nic nie zarobił/a")
                return

# Com-crime
@client.command()
async def crime(ctx):
    if ctx.channel.id != MAIN_CHANEL: return

    await create_user(ctx.author.id)

    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id
    with open(TIME_JSON_PATH, "r") as tf: time_data = json.load(tf)

    if time_data[str(user)]["crime_cld"] != "none":

            json_datetime = datetime.strptime(time_data[str(user)]["crime_cld"], '%Y-%m-%d %H:%M:%S.%f')

            if json_datetime > datetime.now():

                dif = json_datetime - datetime.now()

                sec = dif.seconds

                hours = sec//3600
                seconds = sec % 60
                minutes = (sec//60) % 60

                embed = discord.Embed(description = f"Niedawno popełniłeś przestępstwo. Taka okazja powtórzy się dopiero za: **{str(hours)}**h, **{str(minutes)}**m, **{str(seconds)}**s!", color = discord.Color.green())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                return

    time_data[str(user)]["crime_cld"] = str(datetime.now() + timedelta(hours = 4.5))

    with open(TIME_JSON_PATH, "w") as tf: json.dump(time_data, tf, indent=4)

    amount = random.randint(100,250)
    win = random.choice([True, True, True, False, False])

    reply = random.choice(["Okradasz kasetkę", "Kradniesz portfel", "Sprzedajesz swoje dziecko", "Napadasz na sklep", "Kradniesz kartę płatniczą", "Pobiłeś sąsiada", "Ukradłeś portwel swojej mamie", "Sprzedałeś nerkę", "Oskamowałeś dziecko na bobuxy", "Sprzedajesz niewolnika", "Kradniesz auto", "Kradniesz simsona"])

    if win == True:
        data[str(user)]["wallet"] += amount

        with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)

        embed = discord.Embed(description = f"{reply} i zarabiasz **$ {amount}**", color = discord.Color.green())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

        await log(ctx, f"Używa komendy 'crime' i zarabia**$ {amount}**")
    else:
        await fjail(ctx, 1, random.randint(75,175))

# Com-pay
@client.command()
async def pay(ctx, member: discord.Member = None, amount = None):
    if ctx.channel.id != MAIN_CHANEL: return

    await create_user(ctx.author.id)

    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id

    if member != None or amount != None: await create_user(member.id)
    else: 
        embed = discord.Embed(description = "pay <@oznaczenie> <ilość>",color = discord.Color.red())
        await ctx.send(embed = embed)
        return
    if amount == "all":
        if data[str(user)]["wallet"] < 1:
            embed = discord.Embed(description ="Nie posiadasz pieniędzy w portfelu!", color = discord.Color.red())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        else:
            amount = data[str(user)]["wallet"]
    elif int(amount) < 1: 
        embed = discord.Embed(description ="**No i na huj kombinujesz**", color = discord.Color.gold())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return
    elif int(amount) > data[str(user)]["wallet"]:
        embed = discord.Embed(description = "Nie posiadasz tyle pieniedzy w portfelu!",color = discord.Color.red())
        await ctx.send(embed = embed)
        return

    data[str(user)]["wallet"] -= int(amount)
    data[str(member.id)]["wallet"] += int(amount)

    with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)

    embed = discord.Embed(description = f"Pomyślnie wysłano **$ {amount}** do {member}", color = discord.Color.green())
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

    await log(ctx, f"Użył/a komendy 'pay' i wpłacił/a na konto użytkownika **{member} $ {amount}**")

# Com-rob
@client.command()
async def rob(ctx, member: discord.Member = None):
    if ctx.channel.id != MAIN_CHANEL: return

    user = ctx.author.id
    muser = member.id

    await create_user(user)
    await create_user(muser)

    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f)
    with open(TIME_JSON_PATH, "r") as tf: time_data = json.load(tf)

    if time_data[str(user)]["rob_cld"] != "none":

            json_datetime = datetime.strptime(time_data[str(user)]["rob_cld"], '%Y-%m-%d %H:%M:%S.%f')

            if json_datetime > datetime.now():

                dif = json_datetime - datetime.now()

                sec = dif.seconds

                hours = sec//3600
                seconds = sec % 60
                minutes = (sec//60) % 60

                embed = discord.Embed(description = f"Niedawno próbowałeś kogoś okraść. Taka okazja powtórzy się dopiero za: **{str(hours)}**h, **{str(minutes)}**m, **{str(seconds)}**s!", color = discord.Color.green())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                return

    if data[str(muser)]["wallet"] < 1:
        embed = discord.Embed(description = f"**{muser}** ma pusty portfel!", color = discord.Color.green())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return

    time_data[str(user)]["rob_cld"] = str(datetime.now() + timedelta(hours = 1))

    with open(TIME_JSON_PATH, "w") as tf: json.dump(time_data, tf, indent=4)

    win = random.choice([True, True, True, False, False])
    reply = random.choice(["zegarka","srebnego wisiorka","portfela","karty płatniczej","pozłacanej skarpetki","auta"])

    amount = data[str(muser)]["wallet"]

    if win == True:
        data[str(muser)]["wallet"] = 0
        data[str(user)]["wallet"] += amount

        with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)

        embed = discord.Embed(description = f"okradasz **{member}** z {reply} i zarabiasz **$ {amount}**", color = discord.Color.green())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

        await log(ctx, f"Używa komendy 'rob' i okrada **{member}** na **$ {amount}**")
    else:
        await fjail(ctx, 1, round(amount / 3))

# Com-deposit
@client.command(aliases=['dep'])
async def deposit(ctx, amount):
    if ctx.channel.id != MAIN_CHANEL: return

    await create_user(ctx.author.id)

    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id

    if amount == "all":
        if data[str(user)]["wallet"] < 1:
            embed = discord.Embed(description ="Nie posiadasz pieniędzy w portfelu!", color = discord.Color.red())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        else:
            amount = data[str(user)]["wallet"]

    elif int(amount) < 1: 
        embed = discord.Embed(description ="**No i na huj kombinujesz**", color = discord.Color.gold())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return

    elif int(amount) > data[str(ctx.author.id)]["wallet"]:
        embed = discord.Embed(description ="Nie posiadasz tyle pieniedzy w portfelu!", color = discord.Color.red())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return

    data[str(user)]["wallet"] -= int(amount)
    data[str(user)]["bank"] += int(amount)

    embed = discord.Embed(description = f"Wpłacono **$ {amount}**", color = discord.Color.green())
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

    with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)
    await log(ctx, f"Użył/a komendy 'deposit' i wpłacił/a na konto **$ {amount}**")

# Com-withdraw
@client.command(aliases=['with'])
async def withdraw(ctx, amount):
    if ctx.channel.id != MAIN_CHANEL: return

    await create_user(ctx.author.id)

    if await fjail(ctx) == True: return

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id

    if amount == "all":
        if data[str(user)]["bank"] < 1:
            embed = discord.Embed(description ="Nie posiadasz pieniędzy!", color = discord.Color.red())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        else:
            amount = data[str(user)]["bank"]
    
    elif int(amount) < 1: 
        embed = discord.Embed(description ="**No i na huj kombinujesz**", color = discord.Color.gold())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return

    elif int(amount) > data[str(ctx.author.id)]["bank"]:
        embed = discord.Embed(description ="Nie posiadasz tyle pieniedzy w banku!", color = discord.Color.red())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return

    data[str(user)]["wallet"] += int(amount)
    data[str(user)]["bank"] -= int(amount)

    embed = discord.Embed(description = f"Wpłacono **$ {amount}**", color = discord.Color.green())
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

    with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)
    await log(ctx, f"Użył/a komendy 'withdraw' i wypłacił/a z konta **$ {amount}**")

# Com-give_money
@client.command(aliases=['give-money'])
async def give_money(ctx, member: discord.Member, amount: int, wallet_or_bank = 'wallet'):
    if ctx.channel.id != MAIN_CHANEL: return

    id = member.id
    await create_user(id)

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id

    if data[str(user)]["prem"] != "admin":
        return
    else:

        if wallet_or_bank == 'wallet': data[str(id)]["wallet"] += amount
        elif wallet_or_bank == 'bank': data[str(id)]["bank"] += amount
        else: return

        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.add_field(name = "Dla użytkownika:", value = member, inline=False)
        embed.add_field(name = f"Dodano do '{wallet_or_bank}': ", value = f'$ {amount}')
        await ctx.send(embed = embed)

        with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)

        await log(ctx, f"Użył/a komendy 'give_money' i dał/a do '{wallet_or_bank}' **$ {amount}** dla użytkownika: **{member}**", 1)

# Fun-fjail
async def fjail(ctx, opt = 0, fine = 0):
    await create_user(ctx.author.id)

    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id
    with open(TIME_JSON_PATH, "r") as tf: time_data = json.load(tf)
    
    if opt == 0:
        if time_data[str(user)]["jail_time"] != "none":

            json_datetime = datetime.strptime(time_data[str(user)]["jail_time"], '%Y-%m-%d %H:%M:%S.%f')

            if json_datetime > datetime.now():

                dif = json_datetime - datetime.now()

                sec = dif.seconds

                seconds = sec % 60
                minutes = (sec//60) % 60

                embed = discord.Embed(description = f"wyjdziesz z więzienia za: **{str(minutes)}**m, **{str(seconds)}**s!", color = discord.Color.red())
                embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)

                return True
            
            else: return False
        else: return False

    if opt == 1:
        jail_time = random.randint(5, 30)

        time_data[str(user)]["jail_time"] = str(datetime.now() + timedelta(minutes = jail_time))

        with open(TIME_JSON_PATH, "w") as tf: json.dump(time_data, tf, indent=4)

        if fine == 0:
            embed = discord.Embed(description = f"Policja cię złapała i trawiasz do bębna na **{jail_time}**m", color = discord.Color.red())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            log(ctx, f"Trafia do więzienia na **{jail_time}m**")
        else:
            data[str(user)]["wallet"] -= fine

            with open(USERS_JSON_PATH, "w") as f: json.dump(data, f, indent=4)

            embed = discord.Embed(description = f"Policja cię złapała i trawiasz do bębna na **{jail_time}**m. Przy okazji dostajesz grzywnę wysokości **$ {fine}**", color = discord.Color.red())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            await log(ctx, f"Trafia do więzienia na **{jail_time}m** i dostaje grzywnę o wysokosci **$ {fine}**")

# Fun-create_user
async def create_user(user):
    with open(USERS_JSON_PATH, "r") as f:
        data = json.load(f)

    with open(TIME_JSON_PATH, "r") as tf:
        time_data = json.load(tf)

    if str(user) in data:
        return
    else:
        data[str(user)] = {}
        data[str(user)]["prem"] = "user"
        data[str(user)]["wallet"] = 100
        data[str(user)]["bank"] = 0
        data[str(user)]["job"] = "none"
        data[str(user)]["exp"] = 0
        data[str(user)]["inv"] = []

        time_data[str(user)] = {}
        time_data[str(user)]["work_cld"] = "none"
        time_data[str(user)]["crime_cld"] = "none"
        time_data[str(user)]["slut_cld"] = "none"
        time_data[str(user)]["rob_cld"] = "none"
        time_data[str(user)]["jail_time"] = "none"

    
    with open(USERS_JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

    with open(TIME_JSON_PATH, "w") as tf:
        json.dump(time_data, tf, indent=4)

# fun-log
async def log(ctx, message, color = 0):
    with open(USERS_JSON_PATH, "r") as f: data = json.load(f); user = ctx.author.id

    if color == 0: embed = discord.Embed(description = message, color = discord.Color.green())
    elif color == 1: embed = discord.Embed(description = message, color = discord.Color.red())
    elif color == 2: embed = discord.Embed(description = message, color = discord.Color.blue())
    elif color == 3: embed = discord.Embed(description = message, color = discord.Color.gold())
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.add_field(name ="ID: ", value = f'``{ctx.author.id}``', inline=False)
    embed.add_field(name ="prem: ", value = f'``{data[str(user)]["prem"]}``')
    embed.add_field(name ="wallet: ", value = f'``$ {data[str(user)]["wallet"]}``')
    embed.add_field(name ="bank: ", value = f'``$ {data[str(user)]["bank"]}``')
    await client.get_channel(LOG_CHANEL).send(embed = embed)


client.run(TOKEN)