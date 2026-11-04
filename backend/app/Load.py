import csv

from app.BplusTree import BPlusTree
from app.Car import Car

transmissions = {
    "A": "Automatic",
    "CVT": "Automatic",
    "Dual Clutch": "Automatic",
    "M": "Manual"
}

fuel_types = {
    "Flex Fuel Vehicle": "Gasoline",
    "Biodiesel": "Diesel"
}

def load_cars( data_path, order ):

    tree = BPlusTree( order )

    with open( data_path, newline = "" ) as file:
        read = csv.DictReader( file )

        for car_id, row in enumerate( read ):

            car = Car( 
                row["make"], 
                row["model"], 
                row["body_type"], 
                row["color"], 
                int( row["year"] ), 
                fuel_types.get( row["fuel_type"], row["fuel_type"]), 
                transmissions.get( row["transmission"], row["transmission"] ), 
                int( row["price_cents"] ), 
                row["has_accidents"] == "true",
                int( row["mileage"] ),
                row[ "drivetrain" ],
                int( row["seating"] ),
                car_id
            )

            tree.insert( car )

    return tree