from django.db import models


class GameModel(models.Model):
    player1 = models.IntegerField(default=0)
    player2 = models.IntegerField(default=0)
    turn = models.BooleanField(default=False)


class SeaState(models.Model):
    playing = models.BooleanField(default=False)
    customizing = models.BooleanField(default=False)
    gameid = models.IntegerField(default=0)
    field = models.CharField(max_length=255)

    @classmethod
    def plays(cls, playerid):
        return cls.objects.filter(pk=playerid, customizing=True).count() > 0
    @classmethod
    def createuser(cls):
        ss = cls()
        ss.save()
        return ss.pk
