from .models import SeaState, GameModel
def creategames():
    q = SeaState.objects.filter(customizing=False)
    for i in range(len(q)):
        if i + 1 < len(q):
            create_one_game(q[i], q[i + 1])

def create_one_game(a, b):
    game = GameModel(player1=a.pk, player2=b.pk)
    game.save()
    a.customizing = True
    b.customizing = True
    a.save()
    b.save()

class FieldValidation:
    def __init__(self, ships):
        self.ships = ships
        for i in self.ships:
            print(i)
        print()

    def is_valid(self):
        self.was = [[False for i in range(10)] for j in range(10)]
        this_count = [0] * 4
        for i in range(10):
            for j in range(10):
                if self.ships[i][j] and not self.was[i][j]:
                    size = self.dfs(i, j)
                    print(i, j, size, sep=' ')
                    if size == -1 or size > 4:
                        print('sizes problem')
                        return False
                    this_count[size - 1] += 1
        print(self.shipcounts)
        print(this_count)
        return not any(t[0] != t[1] for t in list(zip(this_count, self.shipcounts)))

    okdi = [0, 1, 0, -1]
    okdj = [1, 0, -1, 0]
    wrdi = [1, 1, -1, -1]
    wrdj = [-1, 1, -1, 1]

    shipcounts = [4, 3, 2, 1]

    def okpos(self, i, j):
        return i >= 0 and j >= 0 and i < 10 and j < 10

    def dfs(self, i, j):
        self.was[i][j] = True
        for k in range(4):
            ni, nj = i + self.wrdi[k], j + self.wrdj[k]
            if self.okpos(ni, nj) and self.ships[ni][nj]:
                print('wrong')
                print(i, j, sep=' ')
                print(ni, nj, sep=' ')
                return -1
        res = 1
        for k in range(4):
            ni, nj = i + self.okdi[k], j + self.okdj[k]
            if self.okpos(ni, nj) and self.ships[ni][nj] and not self.was[ni][nj]:
                size = self.dfs(ni, nj)
                if size == -1:
                    print('suddenly -1, think of it')
                    return -1
                res += size
        return res

#[[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,1],[0,0,1,0,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,1],[0,0,1,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0]]