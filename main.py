from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import link_token, accounts, fields
from db.db_init import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the database when the app starts
init_db()

app.include_router(link_token.router)
app.include_router(accounts.router)
app.include_router(fields.router)
