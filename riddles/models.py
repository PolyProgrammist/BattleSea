from django.db import models

class Game(models.Model):
    player1 = models.IntegerField
    player2 = models.IntegerField
    turn = models.BooleanField
    gameid = models.IntegerField(primary_key=True)

class SeaState(models.Model):
    gameid = models.IntegerField
    playerid = models.IntegerField(primary_key=True)
    field = models.CharField(max_length=255)

class Riddle(models.Model):
    riddle_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')

    def __str__(self): return self.riddle_text


class Option(models.Model):
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        if self.correct:
            value = "Correct"
        else:
            value = "Wrong"
        return "{} - ({}) [{}]".format(self.text, value, self.riddle.riddle_text)

class Hack(models.Model):
    hacker = models.TextField()

    def __str__(self):
        return self.hacker
