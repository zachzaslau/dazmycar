from Load import load_cars
from Score import score
from MergeSort import merge_sort
from HeapSort import heap_sort
from Results import write_results

try:
    tree = load_cars( "../data/data.csv", 64 )
    print( "Successfully loaded cars!" )
    dataset_status = "loaded"

except Exception as error:
    tree = None
    dataset_status = "not_loaded"
    print( "Failed to load cars!" )
    print( error )

###

while True:
    price_range = input( "Enter the maximum price for your car search (Ex. $35000 [NO COMMAS] ).\nMax Price: $" )
    try:
        price_range = int( price_range )
        break
    except Exception as e:
        print("\nInvalid Input. Pick Again." )
        continue

while True:
    min_year = input( "\nEnter the starting year for your car suggestions between 1986 and 2021 (Ex. '2015' will show results from 2015 to present).\nMinimum Year: " )
    try:
        min_year = int( min_year )
        if 1986 <= min_year <= 2021:
            break
        else:
            print( "\nInput not in range. Pick Again.")
            continue
    except Exception as e:
        print( "Invalid Input. Pick Again." )
        continue

mileage_map = { 1: 5000, 2: 10000, 3: 25000, 4: 50000, 5: 75000, 6: 100000, 7: 1000000}
while True: 
    max_mileage = input( "\nEnter the number corresponding to the mileage range of cars you want to search:\n\t1. < 5,000 miles\n\t2. 5,000 - 10,000 miles\n\t3. 10,000 - 25,000 miles\n\t4. 25,000 - 50,000 miles\n\t5. 50,000 - 75,000 miles\n\t6. 75,000 - 100,000 miles\n\t7. 100,000+ miles\nMileage Range: " )
    try:
        max_mileage = int( max_mileage )
        if max_mileage < 1 or max_mileage > 7:
            raise ValueError
        break
    except Exception as e:
        print( "\nInvalid Option. Pick Again" )
        continue
max_mileage = mileage_map[max_mileage]

colors = []
colors_map = { 1: "WHITE", 2: "BLACK", 3: "SILVER", 4: "GRAY", 5: "RED", 6: "BLUE", 7: "GREEN", 8: "ORANGE", 9: "YELLOW", 10: "BROWN", 11: "GOLD", 12: "PURPLE" }
while True:
    color = input( "\nEnter the number corresponding to the color of cars you want to search. When finished, enter 0 (at least 1 color must be selected).\n\t0. Exit\n\t1. White\n\t2. Black\n\t3. Silver\n\t4. Gray\n\t5. Red\n\t6. Blue\n\t7. Green\n\t8. Orange\n\t9. Yellow\n\t10. Brown\n\t11. Gold\n\t12. Purple\nColor Choice: " )
    try:
        color = int( color )
        if color < 0 or color > 12:
            raise ValueError
        if color == 0 and len(colors) < 1:
            raise ValueError
    except Exception as e:
        print( "\nInvalid Option. Pick Again." )
        continue
    if color == 0:
        break
    colors.append( colors_map[color] )

body_map = { 
    1: "SUV / Crossover",
    2: "Sedan",
    3: "Pickup Truck",
    4: "Hatchback",
    5: "Minivan",
    6: "Coupe",
    7: "Van",
    8: "Wagon",
    9: "Convertible"
}

while True:
    body_type = input( "\nEnter the number corresponding to the body type you want.\n\t1. SUV / Crossover\n\t2. Sedan\n\t3. Truck\n\t4. Hatchback\n\t5. Minivan\n\t6. Coupe\n\t7. Van\n\t8. Wagon\n\t9. Convertible\nBody Type: " )
    try:
        body_type = int( body_type )
        if body_type < 1 or body_type > 9:
            raise ValueError
        break
    except Exception as e:
        print( "\nInvalid Option. Pick Again." )
        continue
body_type = body_map[body_type]

fuel_types = {
    "GAS": "Gasoline",
    "HYBRID": "Hybrid",
    "ELECTRIC": "Electric",
    "DIESEL": "Diesel"
} 

while True:
    fuel_type = input( "\nEnter the fuel type you want from the choices below:\n\tGas\n\tHybrid\n\tElectric\n\tDiesel\nFuel Type: " )
    if fuel_type.upper() not in fuel_types: 
        print( "\nInvalid Option. Pick Again." )
        continue
    break
fuel_type = fuel_types[ fuel_type.upper() ]
    

transmissions = {
    "A": "Automatic",
    "M": "Manual"
}

while True:
    transmission = input( "\nEnter 'A' for Automatic or 'M' for Manual\nTransmission: " )
    if transmission.upper() not in transmissions:
        print( "\nInvalid Option. Pick Again." )
        continue
    break
transmission = transmissions[ transmission.upper() ]

drivetrains = [ "AWD", "FWD", "RWD", "4WD" ]
while True:
    drivetrain = input( "\nEnter the drivetrain you want from the choices below:\n\tAWD\n\tRWD\n\tFWD\n\t4WD\nDrivetrain: " )
    if drivetrain.upper() not in drivetrains: 
        print( "\nInvalid Option. Pick Again." )
        continue
    break
drivetrain = drivetrain.upper()

while True:
    seating = input( "\nEnter one of the following numbers for the amount of seating you want your car to have:\n\t4\n\t5\n\t6\n\t7\n\t8\nSeats: " )
    try:
        seating = int( seating )
        if seating < 4 or seating > 8:
            raise ValueError
        break
    except Exception as e:
        print( "\nInvalid Option. Pick Again." )
        continue

preferences = {
    "year_min": min_year,
    "year_max": 2021,
    "mileage_max": max_mileage,
    "seating": seating,
    "body_types": body_type,
    "fuel_types": fuel_type,
    "transmissions": transmission,
    "drivetrains": drivetrain,
    "colors": colors
}

max_price = price_range * 100

cars = tree.search_range( tree.search_min( 0 ), 0, max_price )
results = score( preferences, cars )

merge_sorted = merge_sort( results )
heap_sorted = heap_sort( results )

###

write_results( merge_sorted )
