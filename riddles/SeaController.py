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