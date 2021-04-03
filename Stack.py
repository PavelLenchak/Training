class MyStack:
    def __init__(self):
        self.array = []

    def push(self, item):
        self.array.append(item)

    def peek(self):
        return self.array[len(self.array)-1]

    def pop(self):
        popped_item = self.array.pop(len(self.array) - 1)
        return popped_item

    def __iter__(self):
        self.index = len(self.array) - 1
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration()
        result = self.array[self.index]
        self.index -= 1
        return result

stack = MyStack()
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(5)

print(stack.peek())
print(stack.pop())
print('"For" operator:')
for item in stack:
    print(item)