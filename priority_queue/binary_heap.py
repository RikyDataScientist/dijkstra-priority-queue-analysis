class BinaryHeap:

    def __init__(self):
        self._heap = []
        self._position = {}

    def insert(self, value, priority: float):
        idx = len(self._heap)
        self._heap.append([priority, value])
        self._position[value] = idx
        self._sift_up(idx)

    def extract_min(self):
        if self.is_empty():
            raise IndexError("extract_min dari heap yang kosong!")

        self._swap(0, len(self._heap) - 1)

        min_priority, min_value = self._heap.pop()
        del self._position[min_value]

        if not self.is_empty():
            self._sift_down(0)

        return min_priority, min_value

    def decrease_key(self, value, new_priority: float):

        if value not in self._position:
            raise KeyError(f"Elemen '{value}' tidak ditemukan di heap!")

        idx = self._position[value]

        if new_priority > self._heap[idx][0]:
            raise ValueError("decrease_key hanya bisa menurunkan priority!")

        self._heap[idx][0] = new_priority
        self._sift_up(idx)

    def contains(self, value) -> bool:
        return value in self._position

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def _sift_up(self, idx: int):
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[parent][0] > self._heap[idx][0]:
                self._swap(parent, idx)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int):
        n = len(self._heap)
        while True:
            smallest = idx
            left  = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < n and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right

            if smallest == idx:
                break

            self._swap(idx, smallest)
            idx = smallest

    def _swap(self, i: int, j: int):
        self._position[self._heap[i][1]] = j
        self._position[self._heap[j][1]] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def __len__(self):
        return len(self._heap)

    def __repr__(self):
        return f"BinaryHeap(size={len(self._heap)}, min={self._heap[0] if self._heap else None})"
