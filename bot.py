import asyncio, discord, random
from tetris import *
from discord.ext import commands, tasks

# set prefix
bot = commands.Bot(command_prefix= "T!")
games = {
#   str(user.id):game_obj
}


@bot.event
async def on_ready():
    print("TetraBot: ready for action!")
    print(f"Logged in as: {bot.user.name}")

    # set bot presence
    game = discord.Game(name=f"Tetris || T!help for info")
    await bot.change_presence(status=discord.Status.online, activity=game)


@tasks.loop(seconds=2.5)
async def clock():
    """Clock in charge of dropping pieces every couple seconds."""
    
    global games
    
    for thisGameID in games.keys():
        thisGame=games[thisGameID]
        try:
            thisGame.drop()
            
            await thisGame.instance.edit(
                embed=discord.Embed(
                    description=thisGame.display(),
                    color=discord.Colour.purple()
                ).set_footer(text=f"Score: {thisGame.score}")
            )
        
        except: 
            try:
                # executes when a teramino drop fails: merge the tetramino to the background
                thisGame.merge()
                # clear any filled lines
                print("Attempting to clear line.")
                thisGame.clear()
                # give the player a new tetramino
                thisGame.grab()
                
                # reset cursor position to default 
                thisGame.x = 3
                thisGame.y = 0
                await thisGame.instance.edit(
                    embed=discord.Embed(
                        description=thisGame.display(), #this line is in charge of updating the current frame displayed in chat
                        color=discord.Colour.purple()
                        ).set_footer(text=f"Score: {thisGame.score}")
                    )
            
            except:
                await thisGame.instance.edit(
                    embed=discord.Embed(
                        description=":space_invader: **Game Over** :space_invader:\nThanks for playing!",
                        color=discord.Colour.purple()
                    ).set_footer(text=f" Final score: {thisGame.score} points")
                )
                print("Deleting Game data... ",games)
                games.pop(thisGameID)
                print("Done ",games)
                return
        else: # executes when no game exists in RAM
            pass
        
        
@bot.command()
async def play(ctx):
    """Starts a game of Tetris in text chat."""
    global games
    if str(ctx.author.id) in games:
        print("Removing leftover game data...")
        games.pop(str(ctx.author.id))
        print("Done.")
    
    # start the game clock if possible
    try:
        clock.start()
    except:
        pass
    instance = await ctx.send(f"Get ready, {ctx.author.mention}!")
    await asyncio.sleep(3)
    # create thisGame instance
    thisGame = game(
        player=ctx.author, 
        instance=instance, 
        board=board(), 
        x=3, # initial x value that pieces spawn at
        y=0
        )
    
    #reset score and state attributes
    thisGame.score = 0
    thisGame.board.state = new_board()
    
    # add this game obj to the global dict
    games[str(ctx.author.id)] = thisGame
    # display the message to discord
    await thisGame.instance.edit(
        content=f"{ctx.author.mention}'s Tetris Game:",
        embed=discord.Embed(
            description=thisGame.display(),
            color=discord.Colour.purple()
        ).set_footer(text=f"Score: {thisGame.score}")
    )
    # add appropriate reactions as buttons 
    # in order, rotccw, left, right, rotc, hard-drop(wip), hold(wip) 
    for emoji in ["\U0001F91B","\U0001F448","\U0001F449","\U0001F91C","\U0001F447"]:
        await thisGame.instance.add_reaction(emoji)
        
        
@bot.command()
async def inv(ctx):
    await ctx.send("Invite me to another server at: https://discord.com/oauth2/authorize?client_id=735948673212481736&scope=bot&permissions=1073753104")
    
    
@bot.event
async def on_reaction_add(reaction, user):
    global games
    
    try:
        user_isnt_player = bool(games[str(user.id)].player.id != user.id)
        #ignores the bot's reactions as well as users who aren't the player
        if user_isnt_player:
            print("non-player reaction")
            await reaction.remove(user)
            return # when the user's id does'nt belong to the current game
    except:
        return # when the user's id doesn't exist in the global dict
    thisGame = games[str(user.id)]
    if reaction.emoji == "\U0001F91B": # ccw rotation
        await reaction.remove(user)
        thisGame.ccw() #NOTE thrown error appears to be automatically handled "\_('u' )_/"
    if reaction.emoji == "\U0001F91C": # cw rotation
        await reaction.remove(user)
        thisGame.cw() #NOTE thrown error appears to be automatically handled "\_('u' )_/"
    if reaction.emoji == "\U0001F448": # translate left
        try:
            thisGame.left()
        except:
            pass
        await reaction.remove(user)
    if reaction.emoji == "\U0001F449": # translate right
        try:
            thisGame.right()
        except:
            pass
        await reaction.remove(user)
    
    if reaction.emoji == "\U0001F447":
        await reaction.remove(user)
        thisGame.harddrop()
        
    else:
        return
    await games[str(user.id)].instance.edit(
        embed = discord.Embed(
            description=thisGame.display(),
            color=discord.Colour.purple()
        ).set_footer(text=f"Score: {thisGame.score}")
    )
    
    
#run the bot script
with open("token.txt", "r") as file:
    bot.run(file.read())
