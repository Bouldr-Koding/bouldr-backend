from fastapi import FastAPI
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to backend"}

@app.get("/get_items")
def get_items():
    return {"message": "Welcome to items"}

# @app.get("/database/insert")
# def db_ins():
#     return {"message": "Welcome to db/insert"}

# @app.get("/user/update/sends")
# def get_items():
#     return {"message": "Welcome to db/insert"}