from fastapi import FastAPI
import uvicorn
import app.players.router as players

app = FastAPI(docs_url="/docs")

app.include_router(players.router)

if __name__ == "__main__":
    try:
        print("Clan Manager")
        uvicorn.run(app=app)
    except Exception as e:
        print(f"❌ FastAPI start filed: {e}")
