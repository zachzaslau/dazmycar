# 1. get all valid cars from B+ tree, 2. begin looping through car list and modify min heap based on score, return heap
# l-child = 2*i + 1
# r-child = 2*i + 2
# parent = (i-1)//2

from app.Compare import compare

def heap_sort( cars ):
    heap = []
    for car in cars:
        heap.append( car )
        heapify_up( heap, len( heap ) - 1 )

    result = []
    while len( heap ) > 0:
        result.append( extract_max( heap ) )

    return result

def extract_max( heap ):
    top = heap[0]
    last = heap.pop()

    if len( heap ) > 0:
        heap[0] = last
        heapify_down( heap, 0, len( heap ) )

    return top 

def heapify_up( heap, i ):
    while i > 0:
        parent = ( i - 1 ) // 2

        if compare( heap[i], heap[parent] ):
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            return

def heapify_down( heap, i, length ):
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        first = i 

        if left < length and compare( heap[left], heap[first] ):
            first = left
        if right < length and compare( heap[right], heap[first] ):
            first = right
        if first == i:
            return 

        heap[i], heap[first] = heap[first], heap[i]
        i = first