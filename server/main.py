from fastapi import FastAPI
from auth.routes import router as auth_router
from docs.routes import router as docs_router

app= FastAPI()

app.include_router(auth_router)
app.include_router(docs_router)

@app.get("/")
def hello():
    return {'hello' : 'patient'}

@app.get("/health")
def health_check():
    return {"message":"OK"}

# def main():
#     print("Hello from mediguide!")


# if __name__ == "__main__":
#     main()
