class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]   

    def hash_function(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def search(self, key):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]  
        return None   
    
    def delete(self, key):
        index = self.hash_function(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]   
                return
        print("....not found")

    def display(self):
        for i, k in enumerate(self.table):
            print(f"Bucket {i}: ", end="")
            if not k:
                print("Empty")
            else:
                pairs = [f"{k}:{v}" for k, v in k]
                print(" → ".join(pairs))

# Test Cases
if __name__ == "__main__":
    ht = HashTable()
    # Insert 
    ht.insert("name", "Alice")
    ht.insert("age", 25)
    ht.insert("city", "New York")

    ht.display()
    
    # Search  
    print(ht.search("name"))  # Alice
    print(ht.search("age"))   # 25
    # Delete  
    ht.delete("age")
    print(ht.search("age"))   # None
    # Update 
    ht.insert("name", "Bob")
    print(ht.search("name"))  # Bob
