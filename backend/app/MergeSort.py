def compare( a, b ):
    if a.score != b.score:
        return a.score > b.score  
    if a.price != b.price:
        return a.price < b.price
    if a.mileage != b.mileage:
        return a.mileage < b.mileage
    return a.car_id < b.car_id

def merge_sort( cars ):
    if len( cars ) <= 1:
        return cars

    middle = len( cars ) // 2
    left = cars[:middle]
    right = cars[middle:]

    sorted_left = merge_sort( left )
    sorted_right = merge_sort( right )

    return merge( sorted_left, sorted_right )

def merge( left, right ):
    result = []
    i = 0
    j = 0

    while i < len( left ) and j < len( right ):
        if not compare( right[j], left[i] ):
            result.append( left[i] )
            i += 1
        else:
            result.append( right[j] )
            j += 1

    result.extend( left[i:] )
    result.extend( right[j:] )

    return result