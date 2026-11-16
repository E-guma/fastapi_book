from fastapi import Depends, FastAPI, params

app = FastAPI()

# Dependency provider.
def user_dep(name: str=params, password: str=params):
    return {"name": name, "valid": True}

# Endpoint using the dependency.
@app.get("/user")
def get_user(user: dict=Depends(user_dep)) -> dict:
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dependency:app", reload=True)