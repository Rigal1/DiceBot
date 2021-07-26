from discord.ext import commands
import os
import traceback
import diceSearchAndCalc as dice
from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext.commands.errors import CommandNotFound
import random
import re
commentOutWord = "(#)"

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
percent = 0.3
memberList = []
emotionTable = ["共感/不信", "友情/怒り", "愛情/妬み", "忠誠/侮蔑", "憧憬/劣等感", "狂信/殺意"]
botSentences = ["コマンド間違えてるニャ！　気を付けるニャ！",
                "コマンドが違うニャ！",
                "また間違えてるのニャ！",
                "それは違うニャ！",
                "ニャー！　間違ってるのニャ！",
                "ほら、間違えてるのニャ"]


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    #print(type(error))
    #print(error_msg)
    if type(error) == CommandNotFound:
        await ctx.send(f"{ctx.author.mention} そのコマンドは無いのニャ！")
    elif type(error) == MissingRequiredArgument:
        await ctx.send(f"{ctx.author.mention} コマンドが足りないニャ！")
    else:
        #messageDice = random.randint(0,len(botSentences)-1)
        await ctx.send(f"{ctx.author.mention} ごめんなさいニャ、何かエラーが起こったみたいニャ")
         

@bot.command()
async def r(ctx, arg):
    if ctx.author.bot:
        return

    result = dice.replaceAndCalc(arg)
    reply = f"{ctx.author.mention} {result}"
    await ctx.send(reply)
    
@bot.command()
async def neko(ctx):
    await ctx.send("ニャーア♪")
    
@bot.command()
async def kitaiti(ctx):
    await ctx.send(f"{ctx.author.mention}**2D6** => 4(2+2) => **4**")
    
@bot.command()
async def ote(ctx):
    if random.random() >= percent:
        await ctx.send(f"{ctx.author.mention} ニャ（ぽふ）")
    else:
        await ctx.send(f"{ctx.author.mention} ニャ（ぷい）")
    
@bot.command()
async def okawari(ctx):
    if random.random() >= percent:
        await ctx.send(f"{ctx.author.mention} ニャ（ぺふ）")
    else:
        await ctx.send(f"{ctx.author.mention} ニャ（ぷい）")


@bot.command()
async def なでなで(ctx):
    await ctx.send(f"{ctx.author.mention} ニャァ～（ゴロゴロ）")
        
@bot.command()
async def et(ctx):
    dice = random.randint(1,6)
    await ctx.send(f"{ctx.author.mention} **{dice}** => `{emotionTable[dice-1]}`")

@bot.command()
async def リガルは美少女(ctx):
    await ctx.send(f"{ctx.author.mention} それは違うのニャ！")

async def random_choice(random_list):
    choice_num = random.randint(0, len(random_list)-1)
    return random_list[choice_num]

async def markup_choice(ctx, choice_list, choice_result):
    choice_list_text = ", ".join(choice_list)
    text = f"{ctx.author.mention} `[{choice_list_text}]` => **{choice_result}**"
    return text
    
@bot.command()
async def choice(ctx, *, arg):
    choice_list = []
    choice_text = arg
    comment_word = ""
    comment_exist = re.search(commentOutWord, choice_text)
    if comment_exist:
        comment_word = choice_text[comment_exist.end():]  #コメントアウト
        choice_text = choice_text[:comment_exist.start()]
    
    comma_exist = re.search(",", choice_text)
    
    
    if choice_text[0] == "[":
        choice_text = choice_text[1:]
    if choice_text[-1] == "]":
        choice_text = choice_text[:-1]
    if choice_text == "":
        await ctx.send("何か言ってほしいのニャ！")
        return -1
    
    if comma_exist:
        choice_list = [item.strip() for item in choice_text.split(',')]
    else:
        choice_list = choice_text.split()

    choice_result = await random_choice(choice_list)
    markup_text = await markup_choice(ctx, choice_list, choice_result)
    if comment_exist:
        markup_text = markup_text + f" `#{comment_word}`"
    await ctx.send(markup_text)

bot.run(token)
