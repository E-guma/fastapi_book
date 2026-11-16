from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic = HTTPBasic()


@app.get("/who")
def user_auth(creds: HTTPBasicCredentials = Depends(basic)):
    return {"user": creds.username, "password": creds.password}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic_auth:app")
