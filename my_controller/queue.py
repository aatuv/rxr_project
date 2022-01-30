class Queue:
    def __init__(self, maxlength=None):
        self.items = []
        self.maxlength = maxlength

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if len(self.items) == self.maxlength:
            self.items.pop()
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def hasItem(self, item):
        for itm in self.items:
            if itm == item:
                return True
        return False

    def removeItem(self, item):
        for i in range(len(self.items)):
            if self.items[i] == item:
                self.items.pop(i)
                return
        print("nothing was removed")

    def size(self):
        return len(self.items)
