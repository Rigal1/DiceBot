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

    result = dice.replaceAndCalc(arg, ctx.author.id)
    reply = f"{ctx.author.mention} {result}"
    await ctx.send(reply)
    
@bot.command()
async def neko(ctx):
    await ctx.send("ニャーア♪")
    

    
@bot.command()
async def kitaiti(ctx):
    if ctx.author.id == 632853740159762435:
        await ctx.send("AAAAAAA")
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
    id = ctx.author.id
    dice = random.randint(1,6)
    if id == 495201006209073152:#モノアイ
        await ctx.send(f"{ctx.author.mention} **愛情** => `もこさんへの愛情/りんごさんへの愛情`")
    elif id == 452400598692659202:#正方形
        await ctx.send(f"{ctx.author.mention} **性質** => `気まぐれ/おもちゃ`")
    elif id == 543824507178057742:#サイア
        await ctx.send(f"{ctx.author.mention} **運命** => `君に星見は/微笑まない`")
    elif id == 238616371624280065:#咲月
        await ctx.send(f"{ctx.author.mention} **犬** => `チワワ/パピヨン`")
    elif id == 614789895487225877:#ゼロ
        await ctx.send(f"{ctx.author.mention} **挨拶** => `浸蝕/人質`")
    elif id == 670410622164402191:#ウーティス
        await ctx.send(f"{ctx.author.mention} **感情** => `ナナシノさんへの愛情/ナナシノさんへの狂信`")
    elif id == 607935585587298325:#ナナシノユクエフメイ
        await ctx.send(f"{ctx.author.mention} **彼女** => `うてさん/ウーティスさん`")
    elif id == 639430569989636099:#ハブクサ
        await ctx.send(f"{ctx.author.mention} **神忍法は** => `夜叉/帝釈天`")
    elif id == 557209926691454976:#つゆ
        await ctx.send(f"{ctx.author.mention} **年齢** => `2歳のJD/四十前半`")
    elif id == 347647544454807574:#そーは
        await ctx.send(f"{ctx.author.mention} **情緒を殺したのは** => `サボテンさん/つゆさん`")
    elif id == 335106138041352192:#京極
        await ctx.send(f"{ctx.author.mention} **犬＝** => `咲月さん/つゆさん`")
    elif id == 372355770316095488:#きんすざく
        await ctx.send(f"{ctx.author.mention} **{dice}** => `　　　　　　←あぶり出し`")
    elif id == 662676435911180304:#むぎはすく
        await ctx.send(f"{ctx.author.mention} **正体** => `遁甲符/双影呟鬼`")
    elif id == 302813277581213697:#砂木
        await ctx.send(f"{ctx.author.mention} **神絵師** => `可愛い/アイコン永遠に感謝`")
    elif id == 619504754959056906:#さるみかん
        await ctx.send(f"{ctx.author.mention} **ガバ** => `天井裏のベッド/辛い時は言ってYo`")
    elif id == 632853740159762435:#リガル
        await ctx.send(f"{ctx.author.mention} **この騒動の** => `主犯/元凶`")
    else:
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
