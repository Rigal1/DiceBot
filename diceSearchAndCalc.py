# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 07:21:27 2021

@author: iriut
"""
import re
import jaconv
import random
commentOutWord = "(#)"

def checkDice(getText):
    checkD = re.findall(r"([0-9]+d[0-9]+)", getText, flags=re.IGNORECASE)
    checkB = re.findall(r"([0-9]+b[0-9]+)", getText, flags=re.IGNORECASE)
    return [checkB, checkD]
    
def calcDice(getText, id):
    checkDType = re.search("b|d", getText, flags=re.IGNORECASE).group()
    dice = getText.split(checkDType)
    result = 0
    allDice = []
    if int(dice[0]) > 100 and int(dice[1]) > 1000:
        return [getText, [], -3]
    elif int(dice[0]) > 100:
        return [getText, [], -1]
    elif int(dice[1]) > 1000:
        return [getText, [], -2]
    
    for i in range(int(dice[0])):
        diceResult = random.randint(1, int(dice[1]))
        if id == 543824507178057742:
            diceResult = 1
            
        allDice.append(diceResult)
        result += diceResult
        
    if checkDType.upper() == "D":
        allDice.sort()
        
    return [getText, allDice, result]

def calcD66(id):
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    if id == 543824507178057742:
        dice1 = 1
        dice2 = 1
    
    dice = [dice1,dice2]
    dice.sort()
    return (10*dice[0]+dice[1])

def replaceAndCalc(getText, id):
    commentWord = ""
    commentExist = re.search(commentOutWord, getText)
    if commentExist:
        commentWord = getText[commentExist.end():]  #コメントアウト
        getText = getText[:commentExist.start()]

    getText = jaconv.z2h(getText, ascii=True, digit=True)
    if getText.upper() == "D66":
        d66 = calcD66(id)
        sendData = [getText, "", str(d66), "", ""]
        markedText = markdownText(sendData)
        return markedText
    
    equality = re.search(">=|<=|=|>|<", getText)
    answer = 0
    calcText = ""
    returnText = ""
    trueOrFalse = ""
    diceText = getText
    targetLevel = 0
    if equality != None:
        getList = getText.split(equality.group())
        diceText = getList[0]
        targetLevel = eval(getList[1])
    
    calcText = diceText
    returnText = diceText
    checkAllDice = checkDice(diceText)
    resultDice = []
    for item in checkAllDice:
        for item2 in item:
            if item2 != "":
                resultDice.append(calcDice(item2, id))
            
    if len(checkAllDice[0]) != 0 or len(checkAllDice[1]) != 0:
        for item in resultDice:
            if item[2] == -1:
                return "そんなにたくさんダイス振れないニャ！"
            elif item[2] == -2:
                return "そんなに大きいダイス振れないニャ！"
            elif item[2] == -3:
                return "どっちも大きすぎるニャ！　もうてんやわんやニャ！"
    
    for item in resultDice:
        calcText = calcText.replace(item[0], str(item[2]), 1)
    
    for item in resultDice:
        intList = "+".join([str(i) for i in item[1]])
        returnText = returnText.replace(item[0], f"{item[2]}({intList})", 1)
        
    try:
        answer = eval(calcText)
    except (SyntaxError, NameError):
        #print("ERROR!!!")
        return "式が間違ってるニャ！"
    
    if equality != None:
        if eval(str(answer) + equality.group() + str(targetLevel)):
            trueOrFalse = "成功"
        else:
            trueOrFalse = "失敗"
    
    sendData = [getText, returnText, str(answer), trueOrFalse, commentWord]
    markedText = markdownText(sendData)
    return markedText

def markdownText(getData):
    inputText = f"`{getData[0]}`"
    allDiceText = ""
    if getData[1] != "":        
        allDiceText = f" {getData[1]} =>"
        
    resultDiceText = f"**{getData[2]}**"
    judgeResultText = ""
    if getData[3] != "":
        judgeResultText = f" => **{getData[3]}**"
    
    commentText = ""
    if getData[4] != "":
        commentText = f"  `#{getData[4]}`"
    
    formattedText = f"{inputText} =>{allDiceText} {resultDiceText}{judgeResultText}{commentText}"
    return formattedText

#s = "1D100+10-20<=70#これはコメントです"
#checkDice(s)
