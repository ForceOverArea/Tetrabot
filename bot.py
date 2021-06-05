import asyncio, dbl, discord, random
from tetris import *
from discord.ext import commands, tasks

# set prefix
bot = commands.AutoShardedBot(command_prefix= "T!")
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
                    ).set_footer(text=f"Score: {thisGame.score}  Hold: {thisGame.hold_piece.shape}")
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
                        ).set_footer(text=f"Score: {thisGame.score}  Hold: {thisGame.hold_piece.shape}")
                    )
            
            except:
                try:
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
                
                except:
                    # This is a sh*tty fix. Games will be frozen roughly once ev. 24 hrs as a result.
                    # as of right now, I'm going to assume that the bot lock-up bug is a cache issue and 
                    # that clearing all games from memory fixes it.
                    games.clear()
                    
        else: # executes when no game exists in RAM
            pass


@bot.command()
@commands.check(commands.is_owner())
async def _view_games(ctx):
    await ctx.message.delete()
    await ctx.author.send(
        content=games, 
        delete_after=60
    )


bot.remove_command("help")
@bot.command(aliases=["info"])
async def help(ctx):
    helpMessage = """
    **:video_game: How to Play:**
    The game is controlled via 6 different reaction 'buttons':
    :point_left:/:point_right: - Move the piece left/right
    :left_fist:/:right_fist: - Rotate the piece counter-clockwise/clockwise
    :point_down: - Drop the piece to the bottom of the board instantly
    :punch: - Hold the current piece and save it for later
    
    **:space_invader: Scoring:**
    Fill lines from left to right to clear them!

        1 line clear ---------- 10 points
        2 line clear ---------- 100 points
        3 line clear ---------- 1000 points
        4 line clear (Tetris) - 10000 points

        T-spin single --------- 1000 points
        T-spin double --------- 10000 points
        T-spin triple --------- 100000 points

        Perfect clear --------- 10000000 points

    **:arrow_forward: To Start a Game:**
    Just type "T!play" in chat and the bot will let you know that the game is starting. The game ends automatically when you lose. (i.e. when the top of the board is blocked)
    
    **:link: Links:**
    Report a bug on GitHub here: https://github.com/ForceOverArea/Tetrabot/issues
    Invite (and vote for) me on the Discord Bot List! https://top.gg/bot/735948673212481736
    """


    await ctx.send(
        embed = discord.Embed(
            title="Tetra - Tetris in Discord",
            description=helpMessage,
            color=discord.Colour.purple()
        ).set_footer(
            text="Created by ForceOverArea#5766",
            icon_url="https://avatars1.githubusercontent.com/u/70045551?s=460&u=0f8845c56ebdfb1f24e1c43d8f4db7259b8824e5&v=4"
        )
    )   


@bot.command()
async def play(ctx):
    """Starts a game of Tetris in text chat."""
    assert(ctx.guild) #prevents games from starting in DMs
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
        ).set_footer(text=f"Score: {thisGame.score}  Hold: {thisGame.hold_piece.shape}")
    )
    # add appropriate reactions as buttons 
    # in order: hold, rotccw, left, right, rotc, hard-drop
    for emoji in ["\U0001F44A", "\U0001F91B","\U0001F448","\U0001F449","\U0001F91C","\U0001F447"]:
        await thisGame.instance.add_reaction(emoji)
        
    
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

        if thisGame.piece.shape == "T": # try to do a t-spin if the piece is a T
            try:
                print("Attempting T-spin (CCW)")
                thisGame.tspin_ccw()
                return
            except:
                pass
        thisGame.ccw() #NOTE thrown errors appear to be automatically handled "\_('u' )_/"

    if reaction.emoji == "\U0001F91C": # cw rotation
        await reaction.remove(user)

        if thisGame.piece.shape == "T": # try to do a t-spin if the piece is a T
            try:
                print("Attempting T-spin (CW)")
                thisGame.tspin_cw()
                return
            except:
                pass
        thisGame.cw() #NOTE thrown errors appear to be automatically handled "\_('u' )_/"

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
    
    if reaction.emoji == "\U0001F447": # harddrop
        await reaction.remove(user)
        thisGame.harddrop()
    
    if reaction.emoji == "\U0001F44A": # hold
        await reaction.remove(user)
        if not thisGame.alreadyHeld: # prevent the user from spamming hold to stall
            thisGame.hold()

    else:
        return
    await games[str(user.id)].instance.edit(
        embed = discord.Embed(
            description=thisGame.display(),
            color=discord.Colour.purple()
        ).set_footer(text=f"Score: {thisGame.score}  Hold: {thisGame.hold_piece.shape}")
    )

#start the top.gg cog (commented out here because token posting tokens online is a bad idea)
#bot.load_extension("TopGG")
    
#run the bot script
with open("token.txt", "r") as file:
    bot.run(file.read())
