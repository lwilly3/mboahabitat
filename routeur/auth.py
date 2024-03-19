from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
# import app.database as database, app.schemas as schemas, app.table_models as table_models, app.utils as utils, app.oauth2 as oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import schemas, table_models,  oauth2, utils,database

# pour la creation du token, intallation du package  pip install python-jose[cryptography]  7h01
# 6h05 installation des librairie pour hacher le pass pip install passlib[bcrypt]

router=APIRouter(
     tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
# 7h10
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
# sur la solution au on accede par user_credentials.email ..  pour la deuxieme solution il retourne un dict avec username et password
# la cle du dict username retourner peux soscker nimporte quoi email, id... en fonction de cequi a ete envoye par lutilisateur
# les info ne seront plus en voye en json par le body clien mais en form-date 7h12
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)): 
# username contien le mail
   user_to_log= db.query(table_models.User).filter(table_models.User.email== user_credentials.username).first() 

   if not user_to_log:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"authentification invalide")
   
#    virification si le pass hacher et sauver en base de donnee est similaire a la version hash de celui fourni par lutilisateur
   if not utils.verify(user_credentials.password, user_to_log.password ):
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"authentification invalide")
 
    
# creation du token
#    le data contien ce que je veux inclure dans le  payloard
#    le token peut etre visualiser dans https://jwt.io/  9h09
   access_token= oauth2.create_acces_token(data={'user_id':user_to_log.id})
   
   return{"access_token" :access_token, "token_type":"bearer"}