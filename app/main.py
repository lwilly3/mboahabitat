
from functools import lru_cache
from fastapi import FastAPI
# import app.table_models 
# import app.database 
from routeur import posts,users,auth, votes
from app.config import settings
# import os

# implementation du middleware pour autoriser des requettes exterieurs 11h22
# demarrage du serveur uvicorn maintest:app --reload  
# print (os.path)
# @lru_cache est utilisé pour décorer la fonction get_settings().
# Cela permettra de mettre en cache le résultat retourné par la fonction, 
# de sorte que si la fonction est appelée à nouveau avec les mêmes arguments, 
# le résultat précédemment calculé sera renvoyé à la place de recalculer le résultat. 
# Cela améliorera les performances en évitant de charger les paramètres à chaque appel.
@lru_cache  #https://fastapi.tiangolo.com/yo/advanced/settings/#__tabbed_5_1     mise a jour python 3.9
def get_settings():
    return settings()
# settings = Settings()
 
#  11h14
# vue que nous utilisons alembic nous navons plus besoin de cette comende que demandait a sql alchemy de dexecuter la creation des table
# table_models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

# permet d'inclure toutes le liens de post dans la liste des lien de mon app 6h26
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)   
app.include_router(votes.router)


