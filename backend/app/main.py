from fastapi import FastAPI

app = FastAPI( title = "DAZ MY CAR! API", version = "0.1.0" )

@app.get( "/api/v1/health" )
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "dataset_status": "not_loaded"
    }
"""
import random
import time
from Car import Car
from BplusTree import BPlusTree
from PQueue import min_heap


NUM_CARS = 200000
TREE_ORDER = 16
 
# ----------------------------------------------------------------------
# Mock data options
# ----------------------------------------------------------------------
MODELS = {
    "Toyota": ["Corolla", "Camry", "RAV4", "Tacoma"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
    "Ford": ["F-150", "Mustang", "Explorer", "Escape"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Kona"],
    "BMW": ["3 Series", "X5", "M4", "i4"],
    "Tesla": ["Model 3", "Model Y", "Model S"],
    "Chevrolet": ["Malibu", "Equinox", "Silverado", "Camaro"],
    "Nissan": ["Altima", "Rogue", "Sentra", "Leaf"],
}
BASE_PRICE = {
    "Toyota": 30000, "Honda": 28000, "Ford": 32000, "Hyundai": 24000,
    "BMW": 55000, "Tesla": 50000, "Chevrolet": 30000, "Nissan": 26000,
}
MAKES = list(MODELS.keys())
BODY_TYPES = ["Sedan", "SUV", "Truck", "Coupe", "Hatchback"]
COLORS = ["Black", "White", "Silver", "Gray", "Red", "Blue", "Green"]
FUEL_TYPES = ["Gasoline", "Hybrid", "Diesel", "Electric"]
TRANSMISSIONS = ["Automatic", "Manual"]
DRIVETRAINS = ["FWD", "RWD", "AWD", "4WD"]
SEATING = [2, 4, 5, 7]
MIN_YEAR = 2010
MAX_YEAR = 2025
MILEAGE_STEP = 5000   # mileage is generated in steps so an exact-match preference can actually hit
MAX_MILEAGE = 150000
 
 
# ----------------------------------------------------------------------
# Building the database
# ----------------------------------------------------------------------
def make_database(count):
    cars = []
    for _ in range(count):
        make = random.choice(MAKES)
        model = random.choice(MODELS[make])
        year = random.randint(MIN_YEAR, MAX_YEAR)
        mileage = random.randint(0, MAX_MILEAGE // MILEAGE_STEP) * MILEAGE_STEP
        damage = random.random() < 0.15
        if make == "Tesla":
            fuel = "Electric"
        else:
            fuel = random.choice(["Gasoline", "Gasoline", "Gasoline", "Hybrid", "Diesel", "Electric"])
 
        price = BASE_PRICE[make] * (1 - 0.05 * (MAX_YEAR - year)) * random.uniform(0.85, 1.15)
        price = price - mileage * 0.03
        if damage:
            price = price * 0.6
        price = int(price / 100) * 100          # round down to the nearest 100 (lots of duplicate prices)
        if price < 1500:
            price = 1500
 
        cars.append(Car(make, model, random.choice(BODY_TYPES), random.choice(COLORS), year,
                        fuel, random.choice(TRANSMISSIONS), price, damage, mileage,
                        random.choice(DRIVETRAINS), random.choice(SEATING)))
    return cars
 
 
# ----------------------------------------------------------------------
# Console input helpers (pressing Enter on a preference means "don't care" -> None)
# ----------------------------------------------------------------------
def ask_choice(label, options):
    print("\n" + label + ": " + ", ".join(options))
    while True:
        answer = input("  > (Enter to skip) ").strip().lower()
        if answer == "":
            return None
        for option in options:
            if option.lower() == answer:
                return option
        print("  Not one of the options, try again.")
 
 
def ask_int(label, low, high, step=1, required=False):
    print("\n" + label + " (" + str(low) + " to " + str(high) +
          (", multiples of " + str(step) if step != 1 else "") + ")")
    while True:
        if required:
            answer = input("  > ").strip().replace(",", "").replace("$", "")
        else:
            answer = input("  > (Enter to skip) ").strip().replace(",", "")
        if answer == "" and not required:
            return None
        if answer.lstrip("-").isdigit():
            value = int(answer)
            if value >= low and value <= high and (value - low) % step == 0:
                return value
        print("  Invalid, try again.")
 
 
def ask_preferences():
    print("\n=== Your preferences (press Enter to skip any of them) ===")
    make = ask_choice("Make", MAKES)
    if make is not None:
        model = ask_choice("Model", MODELS[make])
    else:
        all_models = []
        for m in MAKES:
            for name in MODELS[m]:
                all_models.append(name)
        model = ask_choice("Model", all_models)
    body = ask_choice("Body type", BODY_TYPES)
    color = ask_choice("Color", COLORS)
    year = ask_int("Year", MIN_YEAR, MAX_YEAR)
    fuel = ask_choice("Fuel type", FUEL_TYPES)
    transmission = ask_choice("Transmission", TRANSMISSIONS)
 
    damage_answer = ask_choice("Prior damage?", ["Yes", "No"])
    if damage_answer == "Yes":
        damage = True
    elif damage_answer == "No":
        damage = False
    else:
        damage = None
 
    mileage = ask_int("Exact mileage", 0, MAX_MILEAGE, MILEAGE_STEP)
    drivetrain = ask_choice("Drivetrain", DRIVETRAINS)
 
    seats_answer = ask_choice("Seating capacity", [str(s) for s in SEATING])
    seats = int(seats_answer) if seats_answer is not None else None
 
    # price is not a preference here: the price range below is what pulls cars out of the tree
    return Car(make, model, body, color, year, fuel, transmission, None, damage, mileage, drivetrain, seats)
 
 
# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------
def count_specified(pref):
    values = [pref.make, pref.model, pref.bodyType, pref.color, pref.year, pref.fuel_type,
              pref.transmission, pref.price, pref.damage, pref.mileage, pref.drivetrain,
              pref.seating_capacity]
    count = 0
    for v in values:
        if v is not None:
            count += 1
    return count
 
 
def print_results(ranked, heap, pref):
    specified = count_specified(pref)
    print("\n" + "-" * 118)
    print(f"{'#':>2}  {'Score':<7} {'Make':<10} {'Model':<10} {'Body':<10} {'Color':<7} {'Year':<5} "
          f"{'Fuel':<9} {'Trans':<10} {'Price':>8}  {'Dmg':<4} {'Miles':>8}  {'Drive':<5} {'Seats':>5}")
    print("-" * 118)
    for rank in range(len(ranked)):
        c = ranked[rank]
        score_text = str(heap.calculateScore(c)) + "/" + str(specified)
        print(f"{rank + 1:>2}  {score_text:<7} {c.make:<10} {c.model:<10} {c.bodyType:<10} {c.color:<7} "
              f"{c.year:<5} {c.fuel_type:<9} {c.transmission:<10} {'$' + format(c.price, ','):>8}  "
              f"{'Yes' if c.damage else 'No':<4} {format(c.mileage, ','):>8}  {c.drivetrain:<5} {c.seating_capacity:>5}")
    print("-" * 118)
 
 
# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    random.seed(42)
    print("DAZ MY CAR! console demo")
    print(f"Generating {NUM_CARS:,} random cars...")
    start = time.time()
    cars = make_database(NUM_CARS)
    print(f"  done in {time.time() - start:.2f}s")
 
    print(f"Inserting into the B+ tree (order {TREE_ORDER})...")
    tree = BPlusTree(TREE_ORDER)
    start = time.time()
    for car in cars:
        tree.insert(car)
    print(f"  done in {time.time() - start:.2f}s")
 
    # tree height and price span, read straight off the tree
    height = 1
    node = tree.root
    while not node.is_leaf:
        node = node.children[0]
        height += 1
    cheapest = node.keys[0]
    node = tree.root
    while not node.is_leaf:
        node = node.children[len(node.children) - 1]
    priciest = node.keys[len(node.keys) - 1]
    print(f"  tree height: {height} levels | prices run from ${cheapest:,} to ${priciest:,}")
 
    while True:
        pref = ask_preferences()
 
        print(f"\n=== Price range (database spans ${cheapest:,} to ${priciest:,}) ===")
        low = ask_int("Minimum price", 0, 10**7, required=True)
        high = ask_int("Maximum price", low, 10**7, required=True)
        n = ask_int("How many suggestions?", 1, 100, required=True)
 
        heap = min_heap(pref)
        found = len(tree.search_range(tree.search_min(low), low, high))   # just for the count shown below
        start = time.time()
        heap.returnTopSuggestions(n, tree, low, high)
        elapsed = time.time() - start
 
        # the heap hands back the worst of the top n at index 0, so pop it
        # repeatedly and reverse to list the best match first
        ranked = []
        while len(heap.minheap) > 0:
            ranked.append(heap.minheap[0])
            heap.popHeap()
        ranked.reverse()
 
        print(f"\n{found:,} cars priced ${low:,} to ${high:,}; showing the top {len(ranked)} "
              f"(tree search + heap took {elapsed:.2f}s)")
        if len(ranked) == 0:
            print("No cars in that price range.")
        else:
            print_results(ranked, heap, pref)
 
        again = input("\nSearch again? (y/n) ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
 
 
if __name__ == "__main__":
    main()
 """