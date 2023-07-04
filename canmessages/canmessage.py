class CanMessage:
    id: int
    count: int

    def __init__(self):
        self.id = 0x001
        self.data = b'adafrui'
        self.count = 65

    def next(self):
        self.data = b'adafrui'
        self.data = int.from_bytes(self.data, 'big') << 8
        self.data |= self.count
        if self.count == 90:
            self.count = 65
            self.id += 1
        else:
            self.count += 1
        self.data = self.data.to_bytes(8, 'big')

    def reset(self):
        self.data = b'adafrui'

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"id: {self.id}, data:{self.data} count:{self.count}"


if __name__ == "__main__":
    a = CanMessage()
    print(a)
    for i in range(100):
        a.next()
        print(a)
        a.reset()
