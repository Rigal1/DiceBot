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
textDataLink = "textData.txt"
percent = 0.3
memberList = []
emotionTable = []
botSentences = []
help_text = ""

def initialData():
    getData = readFiles(textDataLink) 
    global emotionTable
    global botSentences
    global helpText
    #global helpCatText
    getEmotion = detectData("emotionTable", getData)
    emotionTable = getEmotion.split(",")
    getSentence = detectData("errorText", getData)
    botSentences = getSentence.split(",")
    helpText = detectData("help", getData)
    #helpCatText = detectData("help_cat", getData)
    print(emotionTable)

def readFiles(link):
    with open(link, encoding = "UTF-8") as f:
        strData = f.read()
        listData = strData.split("\n\n")
        return listData
    
def detectData(name, getList):
    for item in getList:
        List = item.split(":", 1)
        #print(List)
        if len(List) >= 2:
            if List[0] == name:
                return List[1]
            
    return None



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
async def et(ctx):
    dice = random.randint(1,6)
    await ctx.send(f"{ctx.author.mention} **{dice}** => `{emotionTable[dice-1]}`")


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

    bracket_exist = re.search("\[(.*?)\]", choice_text)
    if bracket_exist:
        choice_text = bracket_exist.group(1)
    
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
    
@bot.command()
async def command(ctx):
    await ctx.send(help_text)

initialDate()
bot.run(token)
