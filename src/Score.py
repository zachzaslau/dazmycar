def score( preferences, cars ):

    year_min = preferences[ "year_min" ]
    year_max = preferences[ "year_max" ]
    mileage_max = preferences[ "mileage_max" ]
    seating = preferences[ "seating" ]
    body_types = preferences[ "body_types" ]
    fuel_types = preferences[ "fuel_types" ]
    transmissions = preferences[ "transmissions" ]
    drivetrains = preferences[ "drivetrains" ]
    colors = preferences[ "colors" ]

    results = []

    for car in cars: 
        car_score = 0

        if year_min <= car.year <= year_max:
            car_score += 1

        if car.mileage <= mileage_max:
            car_score += 1

        if car.bodyType == body_types:
            car_score += 1

        if car.fuel_type == fuel_types:
            car_score += 1

        if car.transmission == transmissions:
            car_score += 1

        if car.drivetrain == drivetrains:
            car_score += 1

        if car.color in colors:
            car_score += 1

        if car.seating_capacity == seating:
            car_score += 1

        car.score = car_score

        if car_score >= 6:
            results.append( car )

    return results