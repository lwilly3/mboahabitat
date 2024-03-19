from jose import JWTError, jwt
from datetime import datetime, timedelta
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
# import database as database, table_models as table_models
from .schemas import TokenData
from sqlalchemy.orm import Session
from .config import settings
from app import table_models,database


# 7h47 automatisasion sur postman des la destion des url et des token

# La variable oauth2_scheme déclare le schéma d'authentification 
# à utiliser pour protéger les routes de votre API avec OAuth2. 
# En particulier, dans ce cas, il utilise le schéma d'authentification
# OAuth2 Password Bearer (ou Resource Owner Password Credentials Grant),
# ce qui signifie que les utilisateurs doivent fournir leur nom d'utilisateur
# et leur mot de passe pour obtenir un jeton d'accès.
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


#SECRET_KEY cle secret cote serveur (doit etre bien long pour la robustesse) 7h03
#algorithme a utiliser
#temps d'expiration du token
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRATION_MINUTE


def create_acces_token(data: dict):
    # comme on va manipuler data en plusiers endroits, on fait une copie
    data_to_encode= data.copy()

    # creation du temps dexpiration du token
    expiration= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp':expiration})

    encoded_jwt=jwt.encode(data_to_encode, SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt 


# extrait l'id du token en vue deventuelle traitement a base de l'id de lutilisateur
def verify_access_token(token: str, credentials_exception):
    try:
        # decodage
        token_payload=jwt.decode(token, SECRET_KEY,algorithms= ALGORITHM )
        # extraction
        id:str=token_payload.get("user_id")

        if not id:
            raise credentials_exception 
        # donnee du token dans ce cas cest l'id
        token_data= TokenData(id=id)
    except JWTError:
        # print(e)
        raise credentials_exception
    # except AssertionError as e:
    #     print(e)
    return token_data

# chaques foie qu'un utilisateur devra avoir a acceder a une ressource qui a besoin d'authentification
#il devra fournir un token d'acces et 
 # on ajoutera dans le path operator de la rerquette : user_id: int= Depends(oauth2.get_current_user)

# ==============================
# token: str = Depends(oauth2_scheme): Cela signifie que la fonction get_current_user prend un paramètre token 
# de type chaîne de caractères (str) et utilise Depends(oauth2_scheme) pour dépendre du schéma
# d'authentification OAuth2 que vous avez défini précédemment. Cela signifie que pour appeler cette fonction,
# vous devez fournir un jeton d'authentification valide.

# credential_exception = HTTPException(...): Cette ligne crée une instance de HTTPException avec un code
# d'état HTTP 401 (non autorisé) et un message détaillant que l'identification n'est pas valide. 
# Cela indique qu'une exception sera levée si l'authentification échoue.

# return verify_access_token(token, credentials_exception=credential_exception): 
# Cette ligne appelle une fonction verify_access_token en lui passant le jeton
# d'authentification et l'exception à lever en cas d'échec de vérification du jeton. 
# La fonction verify_access_token vérifie la validité du jeton d'authentification et renvoie les informations
# de l'utilisateur associées à ce jeton s'il est valide.

# En résumé, cette fonction get_current_user vérifie la validité du jeton 
# d'authentification fourni et renvoie les informations de l'utilisateur associées à ce jeton si 
# l'authentification réussit. Si l'authentification échoue, elle lève une exception HTTP 401.
    
    #s'il ne rencontre aucune exeption au erreur il ne retourne l'id et l'acces est permis
def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"identification non valide,", headers={"WWW-Authentificate": "Bearer"})

    contenue_token=verify_access_token(token, credentials_exception=exception  )

    # reourne l'id du l'utilisateur courant
    current_user_info=db.query(table_models.User).filter(table_models.User.id==contenue_token.id).first()


    return current_user_info




     
