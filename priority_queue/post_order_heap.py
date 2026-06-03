class PostOrderHeap:

    def __init__(self):
        self._data = []
        self._sizes = []

        self.comparisons   = 0
        self.insert_ops    = 0
        self.extract_ops   = 0

    def is_empty(self):
        return len(self._data) == 0

    def insert(self, value):
        self.insert_ops += 1
        data = self._data
        sizes = self._sizes
        data.append(value)
        if len(sizes) >= 2 and sizes[-1] == sizes[-2]:
            size = 1 + sizes.pop() + sizes.pop()
            sizes.append(size)
            self._heapify(
                len(data) - 1,
                size
            )
        else:
            sizes.append(1)

    def extract_min(self):
        if self.is_empty():
            raise IndexError("empty heap")
        self.extract_ops += 1
        data = self._data
        sizes = self._sizes

        i = len(data) - 1
        size = sizes[-1]

        minimum = data[i]
        i_ = i - size
        for size_ in sizes[-2::-1]:
            value = data[i_]
            self.comparisons += 1
            if value < minimum:
                minimum = value
                i = i_
                size = size_
            i_ -= size_
        size_ = sizes.pop() // 2
        if size_:
            sizes.extend((size_, size_))
        last = data.pop()
        if i < len(data):
            data[i] = last
            self._heapify(i, size)
        return minimum

    def _heapify(self, i, size):
        data = self._data
        value = data[i]
        while size > 1:
            size //= 2
            right = i - 1
            left = right - size
            self.comparisons += 1
            smallest = (
                right
                if data[right] < data[left]
                else left
            )
            self.comparisons += 1
            if not data[smallest] < value:
                break
            data[i] = data[smallest]
            i = smallest
        data[i] = value

    def get_stats(self) -> dict:
        return {
            "comparisons"  : self.comparisons,
            "insert_ops"   : self.insert_ops,
            "extract_ops"  : self.extract_ops,
        }

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return (f"PostOrderHeap(size={len(self._data)}, "
                f"comparisons={self.comparisons})")
