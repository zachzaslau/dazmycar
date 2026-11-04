# 1. get all valid cars from B+ tree, 2. begin looping through car list and modify min heap based on score, return heap
# l-child = 2*i + 1
# r-child = 2*i + 2
# parent = (i-1)//2


class min_heap():
    def __init__(self, prefCar):
        self.preferredCar = prefCar
        self.minheap = []

    def calculateScore(self, car):
        score = 0
        year_range = 2
        mileage_range_steps = 2
        if self.preferredCar.make is not None and car.make == self.preferredCar.make:
            score += 1
        if self.preferredCar.model is not None and car.model == self.preferredCar.model:
            score += 1
        if self.preferredCar.bodyType is not None and car.bodyType == self.preferredCar.bodyType:
            score += 1
        if self.preferredCar.color is not None and car.color == self.preferredCar.color:
            score += 1
        if self.preferredCar.year is not None:
            if abs(self.preferredCar.year - car.year) <= year_range:
                score += year_range - abs(self.preferredCar.year - car.year)
        if self.preferredCar.fuel_type is not None and car.fuel_type == self.preferredCar.fuel_type:
            score += 1
        if self.preferredCar.transmission is not None and car.transmission == self.preferredCar.transmission:
            score += 1
        if self.preferredCar.price is not None and car.price == self.preferredCar.price:
            score += 1
        if self.preferredCar.damage is not None and car.damage == self.preferredCar.damage:
            score += 1
        if self.preferredCar.mileage is not None and car.mileage == self.preferredCar.mileage:
            steps_off = abs(self.preferredCar.mileage - car.mileage) / 5000   
            if steps_off <= mileage_range_steps:                              
                score += 1 - steps_off / (mileage_range_steps + 1)
        if self.preferredCar.drivetrain is not None and car.drivetrain == self.preferredCar.drivetrain:
            score += 1
        if self.preferredCar.seating_capacity is not None and car.seating_capacity == self.preferredCar.seating_capacity:
            score += 1
        return score

    def returnTopSuggestions(self, n, btree, minPrice, maxPrice):
        self.minheap = [] 
        cars = self.searchBtree(btree, minPrice, maxPrice)
        for car in cars:
            score = self.calculateScore(car)
            if len(self.minheap) < n:
                self.insertHeap(car)
            else:
                if score > self.calculateScore(self.minheap[0]):
                    self.popHeap()
                    self.insertHeap(car)
        return self.minheap 

    def popHeap(self):
        if len(self.minheap) > 0:
            self.minheap[0] = self.minheap[-1]
            self.minheap.pop()
            i = 0  
            while 2*i + 1 < len(self.minheap):
                left = 2*i + 1
                right = 2*i + 2
                smallest = i
                if left < len(self.minheap) and self.calculateScore(self.minheap[left]) < self.calculateScore(self.minheap[smallest]):
                    smallest = left
                if right < len(self.minheap) and self.calculateScore(self.minheap[right]) < self.calculateScore(self.minheap[smallest]):
                    smallest = right
                if smallest != i:
                    self.minheap[i], self.minheap[smallest] = self.minheap[smallest], self.minheap[i]
                    i = smallest
                else:
                    break

    def insertHeap(self, car):
        self.minheap.append(car)
        index = len(self.minheap) - 1
        while index > 0:
            parent = (index - 1) // 2
            if self.calculateScore(self.minheap[parent]) > self.calculateScore(self.minheap[index]):
                self.minheap[parent], self.minheap[index] = self.minheap[index], self.minheap[parent]
                index = parent
            else:
                break

    def searchBtree(self, btree, minPrice, maxPrice):

        start = btree.search_min(minPrice)
        return btree.search_range(start, minPrice, maxPrice)