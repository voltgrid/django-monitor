from model_mommy.recipe import Recipe, foreign_key, seq

from .models import Config, Event, Host, Result


event = Recipe(Event)

host = Recipe(Host)

config = Recipe(Config, host=foreign_key(host), event=foreign_key(event))

result = Recipe(Result, host=foreign_key(host), event=foreign_key(event), description='"%s"' % seq("test"))