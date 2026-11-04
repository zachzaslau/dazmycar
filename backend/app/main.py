from fastapi import FastAPI

from app.Load import load_cars
from app.Score import score
from app.Car import Car

try:
    tree = load_cars( "../data/prepared/data.csv", 64 )
    print( "Successfully loaded cars!" )
    dataset_status = "loaded"

except Exception as error:
    tree = None
    dataset_status = "not_loaded"
    print( "Failed to load cars!" )
    print( error )

app = FastAPI( title = "DAZ MY CAR! API", version = "0.1.0" )

@app.get( "/api/v1/health" )
def health() -> dict[str, str]:

    return {
        "status": "ok",
        "dataset_status": dataset_status
    }