class Queue:
    """FIFO: First In First Out"""
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)
        return True  
    
    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)
    
    def front(self):
        if self.is_empty():
            return None
        return self.queue[0]
    
    def size(self):
        return len(self.queue)
    
    def is_empty(self):
        return len(self.queue) == 0

# Test Cases
if __name__ == "__main__":
    q = Queue()
    # add
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(2)   
    
    print(q)        #[1, 2, 3, 2]
       
    print(q.size())   # 4
    print(q.front())  # 1
    
    # remove
    print(q.dequeue())  # 1
    print(q.dequeue())  # 2
    print(q.dequeue())  # 3
    
    print(q.is_empty())  # No está vacío
    print(q.dequeue())   # 2
    print(q.is_empty())  # Vaciamos
 