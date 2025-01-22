from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment

app = FastAPI()
Jinja2 = Environment()

@app.get("/")
async def index():
    return {"text": "Welcome to the hall of fame!"}

@app.get("/welcome")
async def round(username="hacker"):
    output = Jinja2.from_string("Can you defeat me " + username).render()
    return HTMLResponse(content=output)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=9001)