from pydantic import BaseModel, EmailStr, ConfigDict, Field

#each schema validates something, can use multple schema in single api
# to return back info to request. Example; Registration, it sends id back 

# Registration schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=4)


# Login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# User response schema
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


# JWT response schema
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Refresh request schema

class RefreshRequest(BaseModel):
    refresh_token: str


# Note creation schema
class NoteCreate(BaseModel):
    title: str
    content: str


# Note update schema
class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


# Note response schema
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)