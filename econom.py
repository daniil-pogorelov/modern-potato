import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import datetime
import random
import json

import cfg
Bot = commands.Bot(command_prefix="$")
queue = []

Bot.remove_command( 'help' )

@Bot.command()
async def help(ctx):
    emb = discord.Embed(colour = discord.Color.blurple(), description=f'**UyU**')
    await ctx.send(embed= emb)
@Bot.command()
async def timely(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(ctx.author.id) in money:
        money[str(ctx.author.id)] = {}
        money[str(ctx.author.id)]['Money'] = 0

    if not str(ctx.author.id) in queue:
        emb = discord.Embed(colour = discord.Color.gold(), description=f'**{ctx.author}** Вы получили свои 100 монет')
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
            emb = discord.Embed(colour = discord.Color.red(), description=f'**{ctx.author}**, зарегестрируйся! ''Команда - `$timely`')
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
async def createshop(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str('shop') in money:
        money[str('shop')] ={}
        emb = discord.Embed(colour = discord.Color.green(), description=f'Вы создали магазин! <a:greenverify:832661528490541087>')
        await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
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
async def shop(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
        emb = discord.Embed(colour = discord.Color.teal(), title="Магазин", description=f'Для получения предмета свяжитесь с <@!341542480447143936>! ')
        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/789043859869925416/832626316552962118/ezgif.com-gif-maker_4.gif')
        for role in money['shop']:
            emb.add_field(name=f'<a:pinkarrow:832661766181879889>Цена: {money["shop"][role]["Cost"]}',value=f'<@&{role}>',inline=False)
        await ctx.send(embed=emb)

@Bot.command()
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
                emb = discord.Embed(colour = discord.Color.green(), description=f'Вы купили роль! <a:greenverify:832661528490541087>')
                await ctx.send(embed = emb)
                for i in money['shop']:
                    if i == str(role.id):
                        buy = discord.utils.get(ctx.guild.roles,id = int(i))
                        await ctx.author.add_roles(buy)
                        money[str(ctx.author.id)]['Money'] -= money['shop'][str(role.id)]['Cost']
                        role = discord.utils.get( ctx.author.guild.roles, id = 832663535485976627 )
                        await ctx.author.add_roles(role)
            else:
                emb = discord.Embed(colour = discord.Color.red(), description=f'У вас уже есть эта роль!')
                await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
async def give(ctx,member:discord.Member,arg:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(member.id) in money:
        if money[str(ctx.author.id)]['Money'] >= arg:
            emb = discord.Embed(colour = discord.Color.dark_green(), description=f'**{ctx.author}** перевел **{member}** **{arg}** монет <a:greenverify:832661528490541087>')
            money[str(ctx.author.id)]['Money'] -= arg
            money[str(member.id)]['Money'] += arg
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(colour = discord.Color.red(), description=f'У вас недостаточно денег')
            await ctx.send(embed = emb)
        with open('economy.json','w') as f:
            json.dump(money,f)
    if not str(member.id) in money:
        emb = discord.Embed(colour = discord.Color.red(), description=f'**{member}** еще не зарегестрирован!')
        await ctx.send(embed= emb)

Bot.run(cfg.TOKEN)