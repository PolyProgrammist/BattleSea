from django.apps import AppConfig

class RiddlesConfig(AppConfig):
    name = 'riddles'
    def ready(self):
        from .models import SeaState, GameModel
        SeaState.objects.all().delete()
        GameModel.objects.all().delete()