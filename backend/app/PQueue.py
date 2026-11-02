# 1. get all valid cars from B+ tree, 2. begin looping through car list and modify min heap based on score, return heap
# l-child = 2*i + 1
# r-child = 2*i + 2
# parent = (i-1)//2

class min_heap():
    preferredCar = Car("Toyota", "RAV3", "", "", 2050, "", "", 200, False, 0, "", 0)
    minheap = []
    def __init__(self, prefCar):
        self.preferredCar = prefCar

    def calculateScore(self, car):
        score = 0
        if car.make == self.preferredCar.make:
            score += 1
        if car.model == self.preferredCar.model:
            score += 1
        if car.bodyType == self.preferredCar.bodyType:
            score += 1
        if car.color == self.preferredCar.color:
            score += 1
        if car.year == self.preferredCar.year:
            score += 1
        if car.fuel_type == self.preferredCar.fuel_type:
            score += 1
        if car.transmission == self.preferredCar.transmission:
            score += 1
        if car.price == self.preferredCar.price:
            score += 1
        if car.damage == self.preferredCar.damage:
            score += 1
        if car.mileage == self.preferredCar.mileage:
            score += 1
        if car.drivetrain == self.preferredCar.drivetrain:
            score += 1
        if car.seating_capacity == self.preferredCar.seating_capacity:
            score += 1
        return score

    def returnTopSuggestions(self,n):
        cars = self.searchBtree()
        for car in cars:
            score = self.calculateScore(car)
            if len(minheap) < n:
                self.insertHeap(car)
            else:
                if score > self.calculateScore(minheap[0]):
                    self.popHeap()
                    self.insertHeap(car)
                
        

    def popHeap(self):
        if len(minheap) > 0:
            minheap[0] = minheap[-1]
            minheap.pop()
            while 2*i+ 1 < len(minheap):
                left = 2*i + 1
                right = 2*i + 2
                smallest = i
                if left < len(minheap) and self.calculateScore(minheap[left]) < self.calculateScore(minheap[smallest]):
                    smallest = left
                if right < len(minheap) and self.calculateScore(minheap[right]) < self.calculateScore(minheap[smallest]):
                    smallest = right
                if smallest != i:
                    minheap[i], minheap[smallest] = minheap[smallest], minheap[i]
                    i = smallest
                else:
                    break

    def insertHeap(self, car):
        minheap.append(car)
        index = len(minheap) - 1
        while index > 0:
            parent = (index - 1) // 2
            if self.calculateScore(minheap[parent]) > self.calculateScore(minheap[index]):
                minheap[parent], minheap[index] = minheap[index], minheap[parent]
                index = parent
            else:
                break
    

    def searchBtree(self, btree):
        # get all valid cars from B+ tree
        return [Car("Lambo", "Daniels", "", "", 2050, "", "", 200, False, 0, "", 0), Car("Hyundai", "RAV3", "", "", 2050, "", "", 200, False, 0, "", 0), Car("Toyota", "RAV4", "", "", 2050, "", "", 300, False, 0, "", 0)])]
        


