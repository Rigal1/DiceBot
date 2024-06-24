from discord.ext import commands
import os
import traceback
import diceSearchAndCalc as dice

#bot = commands.Bot(command_prefix='/')
client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

"""
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
"""
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    #print(message.content[0:2])
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    
    if client.user in message.mentions: # 話しかけられたかの判定
        await reply(message)
    
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    elif message.content[0:2] == "/r":
        diceText = message.content[3:]
        resultDice = dice.replaceAndCalc(diceText)
        await reply(message, resultDice)
        #await message.channel.send(resultDice)
            
    #print(message)
async def reply(message, result):
    reply = f'{message.author.mention} {result}' # 返信メッセージの作成
    await message.channel.send(reply) # 返信メッセージを送信


client.run(token)
"""    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

"""
