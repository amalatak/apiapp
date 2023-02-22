from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.routers import post, user, auth, vote
from app.database import engine


"""

# Run this with uvicorn app.main:app --reload

# For heroku help run

heroku apps:info 

heroku login
heroku run "alembic upgrade head"
heroku ps:restart to restart the app

git push heroku main to update heroku if basic changes made. Run the 'upgrade head' if DB updates

"""

# Connect to database
# Optional line of code
# models.Base.metadata.create_all(bind=engine)

# What does this do
app = FastAPI()

# Allow specific HTTP methods and domains
# Can use * for all websites, bad for security if not needed
# In all other cases use specific websites
origins = ["*"]
 
# Middleware runs before every request 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def root():
    return {"message": "Welcome to my API!!!"}
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
