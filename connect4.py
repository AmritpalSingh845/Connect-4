import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

r = ["1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","\U000023EE","\U0000274C"]
s = ':white_circle:'

@client.command()
async def c4(ctx, p2: discord.User = None):
    list1 = []
    list2 = []
    p1 = ctx.author
    if p2 == None:
        p2 = p1
        await ctx.send(f"{p1.mention} is playing in single-player mode.")
    else:
        await ctx.send("{} has challenged {} to a connect-4 game. Good Luck!"
            .format(p1.mention,p2.mention))
    grid = [[s]*7 for i in range(6)]

    def retgrid(_move):
        x = '\n' + last_move(_move) + '\n'
        x += ':one: :two: :three: :four: :five: :six: :seven:\n'
        for _row in grid[::-1]:
            for elem in _row:
                x = x + str(elem) + ' '
            x = x + '\n'
        return x

    won = False
    onesturn = True
    move = 0
    msg = await ctx.send(':red_circle:  ' + p1.mention + "'s turn " + retgrid(7))
    await addrxn(msg)
    def check(reaction,user):
        return (user != client.user) and (p1 == user or p2 == user)
#-------------------------------------------------------------------------------------------------------
    while not won:
        rxn, usr = await client.wait_for('reaction_add', check=check)
        await msg.remove_reaction(rxn.emoji,usr)

        def get_move(rxn_emoji):
            for i in range(7):
                if rxn_emoji == r[i]:
                    return i
        move = get_move(rxn.emoji)

        if rxn.emoji == r[7]:
            try:
                if usr == p1 and not onesturn:
                    onesturn = True
                    move = list1[-1]
                    grid = emptyslot(grid,move)
                    list1.pop()
                    await msg.edit(content=" :red_circle: {}'s turn, Undo on {} by {}{}"
                        .format(p1.mention, str(move + 1), p1.name, retgrid(move)))    
                    continue
                if usr == p2 and onesturn:
                    onesturn = False
                    move = list2[-1]
                    grid = emptyslot(grid,move)
                    list2.pop()
                    await msg.edit(content=" :blue_circle: {}'s turn, Undo on {} by {}{}"
                        .format(p2.mention, str(move + 1), p2.name, retgrid(move)))
                    continue
            except:
                continue
            continue

        if rxn.emoji == r[8]:
            if usr == p1  or usr == p2 or usr == await client.fetch_user(294475761375510528):
                await msg.edit(content = usr.mention + " quit :flag_white:")
                await msg.clear_reactions()
                break

        if rxn.emoji == "😄":
            await msg.delete()
            msg = await ctx.send(':red_circle:  ' + p1.mention + "'s turn " + retgrid(7))
            await addrxn(msg)
            continue
#-----------------------------------------------------------------------------------------------------
        filled = False
        for row in range(6):
            if grid[row][move] == s and not filled:
                if onesturn and usr == p1:
                    grid[row][move] = ':red_circle:'
                    list1.append(move)
                    onesturn = not onesturn
                    lm = move

                elif (not onesturn) and usr == p2:
                    grid[row][move] = ':blue_circle:'
                    list2.append(move)
                    onesturn = not onesturn
                    lm = move
                filled = True
                
#-----------------------------------------------------------------------------------------------------
        if onesturn:
            await msg.edit(content = ':red_circle:  ' + p1.mention +"'s turn "+ retgrid(lm))
        else:
            await msg.edit(content = ':blue_circle:  ' + p2.mention +"'s turn "+ retgrid(lm))

        if checkwin(grid):
            won = True
            if onesturn:
                await msg.edit(content = f':blue_circle:  {p2.mention} won! :tada:' + retgrid(lm))
            else:
                await msg.edit(content = f':red_circle:  {p1.mention} won! :tada:' + retgrid(lm))
            await msg.clear_reactions()

        if checkdraw(grid):
            await msg.edit(content = 'Draw  ¯_༼ •́ ͜ʖ •̀ ༽_/¯' + retgrid(lm))
            won = True
            await msg.clear_reactions()
    
def last_move(pos):
    lm = [':black_large_square:']*8
    lm [pos] = ':small_red_triangle_down:'
    return ' '.join(lm[:7])

async def addrxn(msg):
    for i in r:
        await msg.add_reaction(i)

def emptyslot(grid,move):
    for row in range(6):
        if grid[row][move] == s:
            grid[row - 1][move] = s
            break
    else:
        grid[5][move] = s
    return grid

def checkwin(a):
    for i in range(6):
        for x in range(4):
            if (a[i][x] == a[i][x + 1] == a[i][x + 2] == a[i][x + 3]) and a[i][x] != s:
                return True
    for j in range(7):
        for x in range(3):
            if (a[x][j] == a[x + 1][j] == a[x + 2][j] == a[x + 3][j]) and a[x][j] != s:
                return True
    if checkdia(a):
        return True
    if checkdia(a[::-1]):
        return True

def checkdia(b):
    for i in range(6):
        for j in range(7):
            try:
                if (b[i][j] == b[i + 1][j + 1] == b[i + 2][j + 2] == b[i + 3][j + 3]) and b[i][j] != s:
                    return True
            except IndexError:
                continue

def checkdraw(ggrid):
    for i in ggrid[5]:
        if i == s:
            return False
    return True

@client.command()
async def HELP(ctx):
    with open("c4_help.txt","r") as f:
        await ctx.send(f.read())

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    msg = await client.get_channel(568546006095101993).send(client.user.mention + " Online 1.0.1")
    await client.change_presence(activity=discord.Activity(name=
        'Connect 4', type=discord.ActivityType.playing))

with open("token.txt","r") as f:
    client.run(f.readline())
