class PostOrderHeap:

    def __init__(self):
        self._heap     = []
        self._position = {}
        self.comparisons   = 0
        self.decrease_ops  = 0
        self.insert_ops    = 0
        self.extract_ops   = 0

    def insert(self, value, priority: float):
        self.insert_ops += 1

        idx = len(self._heap)
        self._heap.append([priority, value])
        self._position[value] = idx

        self._sift_up(idx)

    def extract_min(self):
        if self.is_empty():
            raise IndexError("extract_min dari heap yang kosong!")

        self.extract_ops += 1

        self._swap(0, len(self._heap) - 1)

        min_priority, min_value = self._heap.pop()
        del self._position[min_value]

        if not self.is_empty():
            self._post_order_sift_down(0)

        return min_priority, min_value

    def decrease_key(self, value, new_priority: float):
        if value not in self._position:
            raise KeyError(f"Elemen '{value}' tidak ditemukan!")

        self.decrease_ops += 1
        idx = self._position[value]

        if new_priority > self._heap[idx][0]:
            raise ValueError("decrease_key hanya bisa menurunkan priority!")

        self._heap[idx][0] = new_priority

        self._post_order_sift_up(idx)

    def contains(self, value) -> bool:
        return value in self._position

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def _post_order_sift_up(self, idx: int):
        while idx > 0:
            parent_idx = (idx - 1) // 2

            self.comparisons += 1
            if self._heap[parent_idx][0] <= self._heap[idx][0]:
                break

            sibling_idx = self._get_sibling(idx)
            if (sibling_idx is not None and
                    self._heap[sibling_idx][0] < self._heap[idx][0]):
                self.comparisons += 1
                if self._heap[parent_idx][0] > self._heap[sibling_idx][0]:
                    self._swap(parent_idx, sibling_idx)
                    self._swap(sibling_idx, idx)
                    idx = parent_idx
                    continue

            self._swap(parent_idx, idx)
            idx = parent_idx

    def _post_order_sift_down(self, idx: int):
        n = len(self._heap)
        while True:
            smallest = idx
            left  = 2 * idx + 1
            right = 2 * idx + 2

            if left < n:
                self.comparisons += 1
                if self._heap[left][0] < self._heap[smallest][0]:
                    smallest = left

            if right < n:
                self.comparisons += 1
                if self._heap[right][0] < self._heap[smallest][0]:
                    smallest = right

            if smallest == idx:
                break

            self._swap(idx, smallest)
            idx = smallest

    def _sift_up(self, idx: int):
        while idx > 0:
            parent = (idx - 1) // 2
            self.comparisons += 1
            if self._heap[parent][0] > self._heap[idx][0]:
                self._swap(parent, idx)
                idx = parent
            else:
                break

    def _get_sibling(self, idx: int):
        if idx == 0:
            return None

        parent = (idx - 1) // 2
        left   = 2 * parent + 1
        right  = 2 * parent + 2
        n      = len(self._heap)

        if idx == left:
            return right if right < n else None
        else:
            return left if left < n else None

    def _swap(self, i: int, j: int):
        self._position[self._heap[i][1]] = j
        self._position[self._heap[j][1]] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def get_stats(self) -> dict:
        return {
            "comparisons"  : self.comparisons,
            "decrease_ops" : self.decrease_ops,
            "insert_ops"   : self.insert_ops,
            "extract_ops"  : self.extract_ops,
        }

    def __len__(self):
        return len(self._heap)

    def __repr__(self):
        return (f"PostOrderHeap(size={len(self._heap)}, "
                f"comparisons={self.comparisons})")
