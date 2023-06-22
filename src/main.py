from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine

from . import services, models, schemas

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/queries", response_model=list[schemas.Query])
def get_queries(db: Session = Depends(get_db)):
    return services.get_queries(db)


@app.post("/queries", response_model=schemas.Query)
def create_query(query: schemas.QueryCreate, db: Session = Depends(get_db)):
    return services.create_query(db, query)


@app.delete("/queries/{hash}", response_model=schemas.Query)
def delete_query_by_hash(hash: str, db: Session = Depends(get_db)):
    return services.delete_query_by_hash(db, hash)


@app.post("/purge-tasks", status_code=204)
def purge_tasks():
    return services.purge_tasks()


@app.post("/query-data")
def get_query_data(query: schemas.QueryCreate):
    return services.get_query_data(query)
