def compare( a, b ):
    if a.score != b.score:
        return a.score > b.score  
    if a.price != b.price:
        return a.price < b.price
    if a.mileage != b.mileage:
        return a.mileage < b.mileage
    return a.car_id < b.car_id