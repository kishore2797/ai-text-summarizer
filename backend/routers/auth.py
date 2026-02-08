from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os

router = APIRouter()
security = HTTPBearer()

# Simple in-memory user storage (in production, use a database)
users_db = {}

class User(BaseModel):
    username: str
    email: str
    password: str  # In production, this should be hashed

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserProfile(BaseModel):
    username: str
    email: str
    created_at: datetime
    last_login: Optional[datetime] = None

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=UserProfile)
async def register(user: User):
    """
    Register a new user
    
    - **username**: Unique username
    - **email**: User email address
    - **password**: User password (will be hashed in production)
    """
    try:
        # Check if user already exists
        if user.username in users_db:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        
        # Store user (in production, hash password and store in database)
        users_db[user.username] = {
            "username": user.username,
            "email": user.email,
            "password": user.password,  # In production, this should be hashed
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        
        return UserProfile(
            username=user.username,
            email=user.email,
            created_at=users_db[user.username]["created_at"],
            last_login=None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    Authenticate user and return access token
    
    - **username**: User username
    - **password**: User password
    """
    try:
        # Verify user credentials
        user = users_db.get(user_credentials.username)
        if not user or user["password"] != user_credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        users_db[user_credentials.username]["last_login"] = datetime.utcnow()
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_credentials.username}, expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/profile", response_model=UserProfile)
async def get_profile(username: str = Depends(verify_token)):
    """
    Get current user profile
    
    Requires authentication token
    """
    try:
        user = users_db.get(username)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return UserProfile(
            username=user["username"],
            email=user["email"],
            created_at=user["created_at"],
            last_login=user["last_login"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")

@router.post("/logout")
async def logout(username: str = Depends(verify_token)):
    """
    Logout user (in a real implementation, you might want to invalidate the token)
    
    Requires authentication token
    """
    try:
        # In a real implementation, you might want to:
        # 1. Add the token to a blacklist
        # 2. Remove the token from a whitelist
        # 3. Update user status
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

@router.get("/me")
async def get_current_user(username: str = Depends(verify_token)):
    """
    Get current authenticated user information
    
    Requires authentication token
    """
    try:
        user = users_db.get(username)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return {
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
            "last_login": user["last_login"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user info: {str(e)}")
