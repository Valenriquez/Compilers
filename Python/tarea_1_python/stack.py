class Stack:
    """LIFO: Last In First Out"""
    def __init__(self):
        self.stack = []
    
    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack.append(item)
        print(f"pushed item: {item}")

    def pop(self):
        if self.is_empty():
            return "stack is empty"
        return self.stack.pop()
    
    def size(self):
        return len(self.stack)
    
    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]
    
    def print_stack(self):
       print(' '.join(str(item) for item in self.stack))
    
# Test Cases
if __name__ == "__main__":
    s = Stack()
    # add
    s.push(1)
    s.push(2)
    s.push(3)
    
    # show all  
    print(s.print_stack())           

    # remove 
    print(s.pop())  # 3
    print(s.pop())  # 2
        
    # show all  
    print(s.print_stack())  # shows only 1

    print(s.is_empty())  # False
    print(s.pop())  # 1
    print(s.is_empty())  # True
    print(s.pop())  # stack is empty

