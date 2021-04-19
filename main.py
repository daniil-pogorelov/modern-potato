import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Activity, ActivityType
import asyncio
import datetime
import random
import json
import cfg
from keep_alive import keep_alive

Bot = commands.Bot(command_prefix="$")
queue = []
queuer = []
COOLDOWN = 10
Bot.remove_command( 'help' )

@Bot.event
async def on_mention(ctx):
  emb=discord.Embed(colour = discord.Color.blurple(), description=f"Исходный код: [ModernBot 2021©](https://github.com/daniil-pogorelov/modern-potato/tree/main) ```Покупай алмазы просто в магазине!```")
  emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/803000873361473617.gif?v=1")
  emb.add_field(name="$free", value="Активация; Получение подарка!", inline=False)
  emb.add_field(name="$balance", value="Проверить баланс", inline=False)
  emb.add_field(name="$shop", value="Магазин", inline=False)
  emb.add_field(name="$buy <@Предмет>", value="Купить предмет", inline=False)
  emb.add_field(name="$give<@Получатель> <Сумма>", value="Перевести сумму", inline=False)
  emb.set_footer(text="Если вы нашли баги, то сообщите разработчику.")
  await ctx.send(embed= emb)


@Bot.event
async def on_ready():
    print("Бот запустился")
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Kings of Leon - Sex On Fire"))
@Bot.event
async def on_message(ctx):
    unix_time = ctx.created_at.timestamp()
    with open('economy.json', 'r') as f:
        data = json.load(f)
    if not str(ctx.author.id) in data:
        data[str(ctx.author.id)] = {}
        data[str(ctx.author.id)]['Money'] = 0
        data[str(ctx.author.id)]['last_message'] = unix_time
        data[str(ctx.author.id)]['Money'] += 1
    elif unix_time - data[str(ctx.author.id)]['last_message'] > COOLDOWN:
        data[str(ctx.author.id)]['Money'] += 1
    data[str(ctx.author.id)]['last_message'] = unix_time
    with open('economy.json', 'w') as f:
        json.dump(data, f)
    await Bot.process_commands(ctx)

@Bot.command()
async def help(ctx):
  emb=discord.Embed(colour = discord.Color.blurple(), description=f"[ModernBot 2021©](https://github.com/daniil-pogorelov/modern-potato/tree/main) ```Покупай алмазы просто в магазине!```")
  emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/803000873361473617.gif?v=1")
  emb.add_field(name="$free", value="Получение подарка!", inline=False)
  emb.add_field(name="$balance", value="Проверить баланс", inline=False)
  emb.add_field(name="$shop", value="Магазин", inline=False)
  emb.add_field(name="$buy <@Предмет>", value="Купить предмет", inline=False)
  emb.add_field(name="$give<@Получатель> <Сумма>", value="Перевести сумму", inline=False)
  emb.set_footer(text="Если вы нашли баги, то сообщите разработчику.")
  await ctx.message.add_reaction("<a:CoolDog:812709382780878878>")
  await ctx.send(embed= emb)
@Bot.command()
async def free(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(ctx.author.id) in money:
        money[str(ctx.author.id)] = {}
        money[str(ctx.author.id)]['Money'] = 0

    if not str(ctx.author.id) in queue:
        emb = discord.Embed(colour = discord.Color.gold(), description=f'**{ctx.author}** Вы получили **100** монет <a:yellowverify:832972871641989156>')
        emb.add_field(name="Получай награду каждые 12 часов!", value="`$free`", inline=False)
        await ctx.send(embed= emb)
        money[str(ctx.author.id)]['Money'] += 100
        queue.append(str(ctx.author.id))
        with open('economy.json','w') as f:
            json.dump(money,f)
        await asyncio.sleep(12*60)
        queue.remove(str(ctx.author.id))
    if str(ctx.author.id) in queue:
        emb = discord.Embed(colour = discord.Color.red(), description=f'**{ctx.author}** Вы уже получили свою награду')
        await ctx.send(embed= emb)
@Bot.command()
async def balance(ctx,member:discord.Member = None):
    if member == ctx.author or member == None:
        with open('economy.json','r') as f:
            money = json.load(f)
        if not str(ctx.author.id) in money:
            emb = discord.Embed(colour = discord.Color.red(), description=f'**{ctx.author}**, зарегестрируйся! ''Команда - `$free`')
            await ctx.send(embed= emb)
        if str(ctx.author.id) in money:
            emb = discord.Embed(colour = discord.Color.green(), description=f'У **{ctx.author}** {money[str(ctx.author.id)]["Money"]} монет')
            await ctx.send(embed= emb)

    else:
        with open('economy.json','r') as f:
            money = json.load(f)
        if not str(member.id) in money:
            emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}** еще не зарегестрирован!')
            await ctx.send(embed= emb)
        if str(member.id) in money:
            emb = discord.Embed(colour = discord.Color.green(), description=f'У **{member}** {money[str(member.id)]["Money"]} монет')
            await ctx.send(embed= emb)
@Bot.command()
@commands.has_permissions(administrator = True)
async def createshop(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str('shop') in money:
        money[str('shop')] ={}
        emb = discord.Embed(colour = discord.Color.green(), description=f'Вы создали магазин! <a:greenverify:832661528490541087>')
        await ctx.send(embed = emb)
    if str('shop') in money:
        emb = discord.Embed(colour = discord.Color.red(), description=f'Вы уже создали магазин!')
        await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
@commands.has_permissions(administrator = True)
async def createbank(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str('bank') in money:
        money[str('bank')] ={}
        money[str('bank')]['Money'] = 0
        emb = discord.Embed(colour = discord.Color.green(), description=f'Вы создали банк! <a:greenverify:832661528490541087>')
        await ctx.send(embed = emb)
    if str('bank') in money:
        emb = discord.Embed(colour = discord.Color.red(), description=f'Вы уже создали банк!')
        await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
@commands.has_permissions(administrator = True)
async def addshop(ctx,role:discord.Role,cost:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        emb = discord.Embed(colour = discord.Color.orange(), description=f'Эта роль уже есть в магазине!')
        await ctx.send(embed = emb)
    if not str(role.id) in money['shop']:
        money['shop'][str(role.id)] ={}
        money['shop'][str(role.id)]['Cost'] = cost
        emb = discord.Embed(colour = discord.Color.green(), description=f'Роль добавлена в магазин! <a:greenverify:832661528490541087>')
        await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
async def bank(ctx):
  with open('economy.json','r') as f:
        money = json.load(f)
        bankk = 'bank'
        emb = discord.Embed(colour = discord.Color.purple(), description=f'В банке находится: {money[str(bankk)]["Money"]} монет! <a:greenverify:832661528490541087>')
        emb.set_footer(text="На все переводы между участниками действует комиссия 1%.")
        await ctx.send(embed= emb)
@Bot.command()
async def shop(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
        emb = discord.Embed(colour = discord.Color.teal(), title="Магазин", description=f'Для получения предмета свяжитесь с <@!341542480447143936>! ')
        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/789043859869925416/832626316552962118/ezgif.com-gif-maker_4.gif')
        for role in money['shop']:
            emb.add_field(name=f'<a:pinkarrow:832661766181879889>Цена: {money["shop"][role]["Cost"]}',value=f'<@&{role}>',inline=False)
            emb.set_footer(text="На все транзакции действует комиссия 3%.")
        await ctx.send(embed=emb)

@Bot.command()
@commands.has_permissions(administrator = True)
async def removeshop(ctx,role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(role.id) in money['shop']:
        emb = discord.Embed(colour = discord.Color.red(), description=f'Этой роли нет в магазине!')
        await ctx.send()
    if str(role.id) in money['shop']:
        emb = discord.Embed(colour = discord.Color.green(), description=f'Роль удалена из магазина! <a:greenverify:832661528490541087>')
        await ctx.send(embed = emb)
        del money['shop'][str(role.id)]
    with open('economy.json','w') as f:
        json.dump(money,f)
@Bot.command()
async def buy(ctx,role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        if money['shop'][str(role.id)]['Cost'] <= money[str(ctx.author.id)]['Money']:
            if not role in ctx.author.roles:
                emb = discord.Embed(colour = discord.Color.green(), description=f'Вы купили товар! Свяжитесь с <@!341542480447143936> и получете его! <a:greenverify:832661528490541087>')
                await ctx.send(embed = emb)
                for i in money['shop']:
                    if i == str(role.id):
                        buy = discord.utils.get(ctx.guild.roles,id = int(i))
                        await ctx.author.add_roles(buy)
                        money[str(ctx.author.id)]['Money'] -= money['shop'][str(role.id)]['Cost'] / 100 * 3 + money['shop'][str(role.id)]['Cost']
                        money['bank']['Money'] += money['shop'][str(role.id)]['Cost'] / 100 * 3 + money['shop'][str(role.id)]['Cost']
                        role = discord.utils.get( ctx.author.guild.roles, id = 832663535485976627 )
                        await ctx.author.add_roles(role)
            else:
                emb = discord.Embed(colour = discord.Color.red(), description=f'У вас уже куплен этот товар! Свяжитесь с <@!341542480447143936> и получете его!')
                await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
async def give(ctx,member:discord.Member,arg:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(ctx.author.id) == str(member.id):
      emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}**, невозможно перевести средства самому себе.')
      await ctx.send(embed = emb)
    if not str(ctx.author.id) == str(member.id):
      if str(member.id) in money:
        if arg > 0:
          if money[str(ctx.author.id)]['Money'] >= arg:
              emb = discord.Embed(colour = discord.Color.green(), description=f'**{ctx.author}** перевел **{member}** **{arg}** монет <a:greenverify:832661528490541087>')
              money['bank']['Money'] += arg / 100 * 1 + arg
              money[str(ctx.author.id)]['Money'] -= arg
              money[str(member.id)]['Money'] += arg
              await ctx.send(embed = emb)
          else:
              emb = discord.Embed(colour = discord.Color.red(), description=f'У вас недостаточно средств!')
              await ctx.send(embed = emb)
          with open('economy.json','w') as f:
              json.dump(money,f)
        if arg < 0:
          emb = discord.Embed(colour = discord.Color.red(), description=f'Хорошая попытка, **{member}**. Увы тут протект от хацкеров <a:zloy:803001315139256341>')
          await ctx.send(embed = emb)
        if arg == 0:
          emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}**, невозможно отправлять суммы меньше **1**!')
          await ctx.send(embed = emb)
      if not str(member.id) in money:
          emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}** еще не зарегестрирован!')
          await ctx.send(embed= emb)

@Bot.command()
@commands.has_permissions(administrator = True)
async def cash(ctx,member:discord.Member,arg:int,text = None):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(member.id) in money:
      if arg > 0:
        emb = discord.Embed(colour = discord.Color.dark_green(), description=f'**{ctx.author}** выдал награду **{member}**! **{arg}** монет <a:greenverify:832661528490541087>')
        emb.add_field(name="Причина:", value=text, inline=False)
        money[str(member.id)]['Money'] += arg
        await ctx.send(embed = emb)
        with open('economy.json','w') as f:
            json.dump(money,f)
      if arg < 0:
        emb = discord.Embed(colour = discord.Color.orange(), description=f'**{ctx.author}** отнял у **{member}** **{arg}**! монет Причина: **{text}** <a:greenverify:832661528490541087>')
        money[str(member.id)]['Money'] += arg
        await ctx.send(embed = emb)
        with open('economy.json','w') as f:
            json.dump(money,f)
      if arg == 0:
        emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}**, не действительное значение!')
        await ctx.send(embed = emb)
    if not str(member.id) in money:
        emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}** еще не зарегестрирован!')
        await ctx.send(embed= emb)

keep_alive()
Bot.run(cfg.TOKEN)