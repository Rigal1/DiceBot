import disnake
from disnake.ext import commands
from disnake.ext.commands.errors import CommandNotFound
from disnake.ext.commands.errors import MissingRequiredArgument
import diceSearchAndCalc as dice_roll

import random

import os
token = os.environ['DISCORD_BOT_TOKEN']

bot = commands.Bot(command_prefix = "!")
token = "ODE0NDE1NjIzMTgxMzAzODE4.YDdhpw.Ayw6AqC0HCPzqX50dnX3-uVgZDQ"


@bot.event
async def on_command_error(ctx, error):
    if type(error) == CommandNotFound:
        await ctx.send(f"{ctx.author.mention} そのコマンドは無いのニャ！")
    elif type(error) == MissingRequiredArgument:
        await ctx.send(f"{ctx.author.mention} コマンドが足りないニャ！")
    else:
        await ctx.send(f"{ctx.author.mention} ごめんなさいニャ、何かエラーが起こったみたいニャ")


@bot.slash_command(description = "基本的なダイスロールのコマンド")
async def roll(inter,
                dice: str = commands.Param(name = "ダイス", description = "上方、下方ロールにも対応。例：1D100<=50"), 
                comment: str = commands.Param(default = "", name = "女神へのご意見", description = "ダイスの女神に言いたいことを書こう！"),
                time: int = commands.Param(default = 1, name = "繰り返し", description = "何度か繰り返す時用。最大は20回まで", gt = 1, lt = 20)
            ):
    if comment != "":
        comment = f"  `#{comment}`"
    if time == 1:
        result = dice_roll.replaceAndCalc(dice)
        await inter.response.send_message(f"{inter.author.mention} {result}{comment}")
    else:
        all_result = f"{inter.author.mention}{comment}"
        for i in range(time):
            result = dice_roll.replaceAndCalc(dice)
            result_markup = f"{i+1:02d}:{result}"
            all_result += f"\n{result_markup}"
        await inter.response.send_message(all_result)


@bot.slash_command(description = "入力した選択肢から選ぶコマンド")
async def choice(inter, 
                items: str = commands.Param(name = "選択肢", description = "スペース区切りかカンマ区切りで入力。例：りんご ゴリラ ラッパ"),
                choice_same: int = commands.Param(default = 0, name = "選ぶ個数-重複アリ", description = "重複ありで幾つ選ぶか"),
                choice_difference: int = commands.Param(default = 0, name = "選ぶ個数-重複ナシ", description = "重複なしで幾つ選ぶか"),
                comment: str = commands.Param(default = "", name = "女神へのご意見", description = "ダイスの女神に言いたいことを書こう！")
                ):



    items = items.replace(",", " ")
    item_list = items.split()
    item_list_text = ", ".join(item_list)
    item_list_text = f"`[{item_list_text}]`"
    results_text = ""

    if comment != "":
        comment = f"  `#{comment}`"
    
    if choice_same == 0 and choice_difference == 0:
        result = random.choice(item_list)
        results_text = result
    
    elif choice_same != 0 and choice_difference == 0:
        results = random.choices(item_list, k = choice_same)
        results_text = ", ".join(results)
    
    elif choice_same == 0 and choice_difference != 0:
        if choice_difference > len(item_list):
            choice_difference = len(item_list)
        results = random.sample(item_list, choice_difference)
        results_text = ", ".join(results)
    
    elif choice_same != 0 and choice_difference != 0:
        return -1

    await inter.response.send_message(f"{inter.author.mention} {item_list_text} => **{results_text}**{comment}")


@bot.command()
async def neko(ctx):
    await ctx.send("ニャーア♪")

@bot.command()
async def r(ctx, arg):
    if ctx.author.bot:
        return

    result = dice_roll.replaceAndCalc(arg)
    reply = f"{ctx.author.mention} {result}"
    await ctx.send(reply)

@bot.event
async def on_ready():
    print("START")

bot.run(token)
