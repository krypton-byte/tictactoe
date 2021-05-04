import colorama
import asyncio
async def Choose():
    while True:
        print("""
1. Multiplayer
2. BOT [BETA]""")
        pil=int(input("Mode: "))
        if pil == 1:
            await run()
            break
        elif pil == 2:
            await withAI()
            break
    
async def run():
    tik = tictactoe()
    while True:
        for i in ["X", "O"]:
            print("X SCORE:{:<10}O_SCORE:{:<15}".format(tik.x_score, tik.o_score))
            print(tik.print())
            while True:
                try:
                    if await tik.add(i, int(input(f"{i}-Index: "))):
                        break
                    else:
                        pass
                except IndexError:
                    tik.board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                except Exception as e:
                    pass
            print(tik.BestMove())
            await tik.check(i)

async def withAI():
    player = {
        "X":None,
        "O":None
    }           
    tik = tictactoe()
    while True:
        pil=str(input("Choose X/O : "))
        if pil in player.keys():
            break
    player[pil]="player"
    while True:
        for i in player.keys():
            print("X SCORE:{:<10}O_SCORE:{:<15}".format(tik.x_score, tik.o_score))
            if player[i]:
                tik.print()
                while True:
                    try:
                        if await tik.add(i, int(input(f"{i} Index: "))):
                            break
                        else:
                            pass
                    except IndexError:
                        tik.board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                    except Exception as e:
                        pass
            else:
                await tik.add(i, tik.Attack(i)[i][0][0] if i=="X" else tik.BestMove()[i][0][0])
                tik.print()
            await tik.check(i)

         
    
class tictactoe:
    pattern = [
    [0, 1, 2], 
    [3, 4, 5], 
    [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    def __init__(self):
        self.board = [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ]
        self.x_score = 0
        self.o_score = 0
    def BestMove(self):
        playermove = {"X":[], "O":[]}
        allboard=list(map(lambda x:self.board[x], range(9)))
        for play in ["X", "O"]:
            cor = []
            for i in enumerate(allboard):
                if i[1]==play:
                    cor.append(i[0])
            for pat in self.pattern:
                if len(cor)<4:
                    if not set([self.board[z] for z in pat]) & set(["O" if play == "X" else "X"]):
                        playermove[play].append(list(set(pat)-set(cor)))

        return playermove
    def Attack(self,player):
        playermove = {"X":[], "O":[]}
        allboard=list(map(lambda x:self.board[x], range(9)))
        for play in ["X", "O"]:
            cor = []
            for i in enumerate(allboard):
                if i[1]==play:
                    cor.append(i[0])
            for pat in self.pattern:
                if len(cor)<4:
                    if not set([self.board[z] for z in pat]) & set(player):
                        playermove[ "O" if play=="X" else "X"].append(list(set(pat)-set(cor)))

        return playermove
    def scoreboard(self, player, amount):
        if player == "X":
            self.x_score+=amount
        elif player == "O":
            self.o_score+=amount
    def print(self):
        warna = []
        for i in self.board:
            if i=="X":
                warna.append(colorama.Fore.RED+"X"+colorama.Fore.RESET)
            elif i == "O":
                warna.append(colorama.Fore.GREEN+"O"+colorama.Fore.RESET)
            else:
                warna.append(i)
        print("""
\t=================
\t|  {:<2}  |  {:<2}  |  {:<2}  |
\t|  {:<2}  |  {:<2}  |  {:<2}  |
\t|  {:<2}  |  {:<2}  |  {:<2}  |
\t=================
        """.format(*warna))
    async def add(self, player:str, index:int):
        assert len(self.board)-1 >= index
        if isinstance(self.board[index], int):
            self.board.__setitem__(index, player)
            return True
        else:
            return False
    async def check(self, player):
        for i in self.pattern:
            data = []
            for x in i:
                if self.board[x] == player:
                    data.append(player)
            if len(data) == 3:
                print(f"{player}: WIN")
                self.board = [0,1,2,3,4,5,6,7,8]
                self.scoreboard(player, 10)
asyncio.run(Choose())