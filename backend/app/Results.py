import html
import os
import webbrowser

app_folder = os.path.dirname( os.path.abspath( __file__ ) )
root_folder = os.path.dirname( os.path.dirname( app_folder ) )

css_path = os.path.join( app_folder, "Results.css" )
public_folder = os.path.join( root_folder, "frontend", "public" )
output_path = os.path.join( root_folder, "output", "results.html" )

def car_card( car ):
    title = html.escape( f"{car.year} {car.make} {car.model}" )
    image = html.escape( car.imageUrl )
    default_image = "file://" + os.path.join( public_folder, "default-car.png" )

    return f"""
    <div class="car-card">
        <div class="car-card-media">
            <img class="car-card-image" src="{image}" alt="{title}"
                onerror="this.onerror = null; this.src = '{default_image}'; this.classList.add( 'car-card-image-default' )">
        </div>
        <div class="car-card-body">
            <h2 class="car-card-title">{title}</h2>
            <p class="car-card-price">${car.price / 100:,.2f}</p>
            <p class="car-card-mileage">{car.mileage:,} miles</p>
            <div class="car-card-specs">
                <span><img src="file://{public_folder}/gearbox.svg" alt="">{html.escape( car.transmission )}</span>
                <span><img src="file://{public_folder}/fuel.svg" alt="">{html.escape( car.fuel_type )}</span>
                <span><img src="file://{public_folder}/wheel.svg" alt="">{html.escape( car.drivetrain )}</span>
            </div>
        </div>
    </div>
    """

def write_results( merge_sorted, limit = 50 ):
    exact = [ car for car in merge_sorted if car.score == 8 ]
    close = [ car for car in merge_sorted if car.score < 8 ]

    exact_cards = "".join( car_card( car ) for car in exact[:limit] )
    close_cards = "".join( car_card( car ) for car in close[:limit] )

    if len( exact ) == 0:
        exact_cards = "<p>None match all your preferences.</p>"

    page = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>DAZ MY CAR! Results</title>
    <link rel="stylesheet" href="file://{css_path}">
</head>
<body class="results">
    <h1 class="results-heading">Exact matches ({len( exact ):,})</h1>
    <div class="results-grid">{exact_cards}</div>

    <h1 class="results-heading">These don't meet all your preferences but are close matches ({len( close ):,})</h1>
    <div class="results-grid">{close_cards}</div>
</body>
</html>"""

    os.makedirs( os.path.dirname( output_path ), exist_ok = True )

    with open( output_path, "w" ) as file:
        file.write( page )

    webbrowser.open( "file://" + output_path )
