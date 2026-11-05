import csv

from BplusTree import BPlusTree
from Car import Car

transmissions = {
    "A": "Automatic",
    "M": "Manual"
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
                row["fuel_type"], 
                transmissions.get( row["transmission"], row["transmission"] ), 
                int( row["price_cents"] ), 
                row["has_accidents"] == "true",
                int( row["mileage"] ),
                row[ "drivetrain" ],
                int( row["seating"] ),
                row["image_url"],
                car_id
            )

            tree.insert( car )

    return tree