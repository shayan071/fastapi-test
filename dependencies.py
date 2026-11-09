
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from security import decode_token


"""
This code handle authentication and authorization.
NOTEE: it is not the business/service logic.
This logic is in 

In simple words, it does two important things:
-Authentication: Checks whether the user is logged in and whether their JWT 
access token is valid.
-Authorization: Checks whether the authenticated user has permission to access
a particular resource, such as an admin-only endpoint.
"""

"""
OAuth2PasswordBearer automatically:
1. Looks for the Authorization header.
2. Checks for the Bearer scheme.
3. Extracts the token.
4. Passes the extracted token to your function.
"""
#OAuth2PasswordBearer tells FastAPI that your application uses bearer tokens for authentication.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"#It tells FastAPI where clients can obtain their authentication token.
)


# GET CURRENT USER: Checks whether a user has admin permissions.
def get_current_user(
    token: str = Depends(oauth2_scheme),#extracts JWT from request header
    db: Session = Depends(get_db)#db access to find the user associate with the token
):
    """
    You create an HTTP exception that will be used whenever authentication fails.
    For example:
    - Token is invalid.
    - Token has expired.
    - Token belongs to an inactive user.
    - Token doesn't contain a valid user ID.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        #JWT tokens contain information called a payload.
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise credentials_exception
        
        #Because the JWT subject (sub) is commonly stored as a string, while SQLAlchemy user ID is an integer
        user_id = int(payload.get("sub"))

    except Exception:

        raise credentials_exception

    #Now your backend uses the extracted user ID to find the actual user in the database.
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    #If the user doesn't exist or their account is inactive, access is denied.
    if not user or not user.is_active:

        raise credentials_exception

    return user#retunring user object, so other functions can use information


"""
FastAPI first executes get_current_user().
If authentication succeeds, it passes the returned user object into require_admin().
If authentication fails, execution stops before require_admin() runs.
"""

# ADMIN AUTHORIZATION: Checks whether a user has admin permissions.
def require_admin(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user