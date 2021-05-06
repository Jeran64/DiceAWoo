import math
import random
import pygame




diceLevel=0;
currentScore=0;
totalScore=0;
diceOutcomes=[
    ["red",["win",.4],["lose",.4],["gameover",.1],["levelup",.1]],
    ["blue",["win",.35],["lose",.35],["nothing",.1],["gameover",.1],["levelup",.1]],
    ["green",["win",.3],["lose",.3],["nothing",.1],["prize",.1],["gameover",.1],["levelup",.1]],
    ["yellow",["win",.3],["lose",.3],["nothing",.1],["prize",.1],["gameover",.1],["levelup",.1]],
    ["silver",["win",.3],["lose",.3],["nothing",.1],["jackpot",.1],["gameover",.1],["levelup",.1]],
    ["purple",["win",.3],["lose",.3],["jackpot",.1],["prize",.1],["gameover",.1],["random",.1]]
    ];
prizeList=["burger","fries","pizza","sushi","soup","BBQ","spaghetti","salad","curry","carrots","strawberries","steak","beer"];
wonPrizes=[];
###########################
### Logic Functions #######
###########################

def getRoll(rollFloat):
    a=0.0;
    b=0;#normally this would need to be -1, but we want to skip the first entry due to the data stored at 0
    while(a<rollFloat): #iterate throught eh list of outcomes. each outcome has a chance, and the algorithm will return the first value that goes over the rolled amount. 
        b=b+1; #this iterates through the list of outcomes
        if(b>len(diceOutcomes[diceLevel])):
           print("Something is terribly wrong. check to see if the dice chances add to 1 on level "+diceOutcomes[diceLevel][0]);
           return "error"
        a=a+diceOutcomes[diceLevel][b][1] #save a running total of the chances of every previous nonvalid outcome.
    return diceOutcomes[diceLevel][b][0]#return the name of the outcome

def executeResults(result):
    global diceLevel,currentScore,totalScore,wonPrizes, diceOutcomes, prizeList, textHolder
    if(result=="win"):
        prize=random.randrange(1,10)*(diceLevel+1)
        currentScore=currentScore+prize
        textHolder=drawFont.render("You won "+str(prize)+" points!",True,(0,0,0));
        #todo high level point doubling
    elif(result=="lose"):
        prize=random.randrange(-10,-1)*(diceLevel+1)
        currentScore=currentScore+prize
        textHolder=drawFont.render("oh no! you lost "+str(prize)+" points.",True,(0,0,0));
        #to do, add high level point halfing.
    elif(result=="nothing"):
        textHolder=drawFont.render("Nothing happened.... we swear...",True,(0,0,0));
    elif(result=="levelup"):
        if(random.random()>.5):
            diceLevel=diceLevel+1;
            textHolder=drawFont.render("oh boy! You leveled up!",True,(0,0,0));
        else:
            textHolder=drawFont.render("You almost leveled up!",True,(0,0,0));
    elif(result=="gameover"):
        if(random.random()>.5):
            diceLevel=0;
            currentScore=0;
            wonPrizes=[];
            textHolder=drawFont.render("YOU LOST! THE AGONY!!!",True,(0,0,0));
        else:
            textHolder=drawFont.render("You almost lost there!",True,(0,0,0));
    elif(result=="prize"):
        prize=prizeList[random.randint(0,len(prizeList)-1)];  
        textHolder=drawFont.render("oh boy, a prize! you won "+str(prize),True,(0,0,0));
        wonPrizes.append(prize);
    elif(result=="random"):
        prize=random.randrange(100,500);
        textHolder=drawFont.render("weird! you found "+str(prize),True,(0,0,0));
        currentScore=currentScore+prize
    elif(result=="jackpot"):
        prize=random.randrange(1000,10000);
        textHolder=drawFont.render("YEAH ! That's the JACKPOT! You won "+str(prize),True,(0,0,0));
        currentScore=currentScore+prize;
        diceLevel=0;
        totalScore=totalScore+currentScore;
        currentScore=0;
        wonPrizes=[];
        
    if(currentScore<0):#we cant have negative points in this game.
        currentScore=0;
        
###########################
### PyGame Nonsense #######
###########################
pygame.init();
display_width = 256;
display_height = 128;
gameDisplay = pygame.display.set_mode((display_width,display_height));
textHolder=gameDisplay;
pygame.display.set_caption("Dice - A - woo");
drawFont = pygame.font.SysFont('Comic Sans MS', 12)

def showResults():
    global result,currentScore, diceLevel, prize
    diceToShow= pygame.image.load(diceOutcomes[diceLevel][0]+result+".gif");#load the appropriate dice image.
    gameDisplay.fill((128,128,128));#clears out the screen for the next draw
    gameDisplay.blit(diceToShow,(88,0));#write the pixels to canvas. show the dice in the top left
    
def showText():
    global textHolder
    gameDisplay.blit(textHolder,(0,80));#draw the text under the image.
    textHolder=drawFont.render("score:"+str(currentScore),True,(0,0,0));
    gameDisplay.blit(textHolder,(0,94));#draw score under that.
    textHolder=drawFont.render("prizes:"+str(wonPrizes),True,(0,0,0));
    gameDisplay.blit(textHolder,(0,108));#draw score under that.

def showOnScreen():

    pygame.display.update();#update the display
    
###########################
### Game Loop #############
###########################
while (1==1):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Rolling a "+diceOutcomes[diceLevel][0]+" die...");
                result=getRoll(random.random())#roll the dice
                print(result) #show me what you got
                showResults(); #draw dice on screen.
                executeResults(result); #act on the game's rules (do this after the draw so the color is right on the dice)
                showText();#tell the user about what they got.
                showOnScreen(); #slap it on the screen.

            if event.key == pygame.K_RETURN:
                totalScore=totalScore+currentScore
                currentScore=0;
                diceLevel=0;
                wonPrizes=[];
                result="nothing"
                textHolder=drawFont.render("CASH OUT!!! Total Score: "+str(totalScore),True,(0,0,0));
                showResults();
                showText();#tell the user about what they got.
                showOnScreen(); #slap it on the screen.

            
