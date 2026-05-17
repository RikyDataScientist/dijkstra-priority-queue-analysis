import math


class FibNode:

    def __init__(self, key: float, value):
        self.key    = key
        self.value  = value
        self.degree = 0
        self.marked = False
        self.parent = None
        self.child  = None
        self.left   = self
        self.right  = self


class FibonacciHeap:

    def __init__(self):
        self._min_node  = None
        self._size      = 0
        self._node_map  = {}

    def insert(self, value, priority: float):
        node = FibNode(priority, value)
        self._node_map[value] = node
        self._add_to_root_list(node)

        if self._min_node is None or node.key < self._min_node.key:
            self._min_node = node

        self._size += 1

    def extract_min(self):
        z = self._min_node
        if z is None:
            raise IndexError("extract_min dari heap yang kosong!")

        if z.child:
            children = self._get_list(z.child)
            for child in children:
                self._add_to_root_list(child)
                child.parent = None

        self._remove_from_root_list(z)
        del self._node_map[z.value]

        if z == z.right:
            self._min_node = None
        else:
            self._min_node = z.right
            self._consolidate()

        self._size -= 1
        return z.key, z.value

    def decrease_key(self, value, new_key: float):
        node = self._node_map.get(value)
        if node is None:
            raise KeyError(f"Node '{value}' tidak ditemukan!")
        if new_key > node.key:
            raise ValueError("decrease_key hanya bisa menurunkan priority!")

        node.key = new_key
        parent = node.parent

        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self._min_node.key:
            self._min_node = node

    def contains(self, value) -> bool:
        return value in self._node_map

    def is_empty(self) -> bool:
        return self._min_node is None

    def _add_to_root_list(self, node: FibNode):
        if self._min_node is None:
            node.left = node
            node.right = node
        else:
            node.right = self._min_node.right
            node.left  = self._min_node
            self._min_node.right.left = node
            self._min_node.right      = node

    def _remove_from_root_list(self, node: FibNode):
        node.left.right = node.right
        node.right.left = node.left

    def _consolidate(self):
        max_degree = int(math.log2(self._size)) + 2 if self._size > 0 else 1
        degree_table = [None] * (max_degree + 1)

        roots = self._get_list(self._min_node)

        for root in roots:
            x = root
            d = x.degree
            while d < len(degree_table) and degree_table[d] is not None:
                y = degree_table[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                degree_table[d] = None
                d += 1

            if d >= len(degree_table):
                degree_table.extend([None] * (d - len(degree_table) + 1))
            degree_table[d] = x

        self._min_node = None
        for node in degree_table:
            if node:
                node.left = node
                node.right = node
                self._add_to_root_list(node)
                if self._min_node is None or node.key < self._min_node.key:
                    self._min_node = node

    def _link(self, child: FibNode, parent: FibNode):
        self._remove_from_root_list(child)
        child.parent = parent
        child.marked = False

        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.right = parent.child.right
            child.left  = parent.child
            parent.child.right.left = child
            parent.child.right      = child

        parent.degree += 1

    def _cut(self, node: FibNode, parent: FibNode):
        """Potong node dari parent dan pindahkan ke root list."""
        parent.degree -= 1

        if node.right == node:
            parent.child = None
        else:
            if parent.child == node:
                parent.child = node.right
            node.left.right = node.right
            node.right.left = node.left

        node.parent = None
        node.marked = False
        self._add_to_root_list(node)

    def _cascading_cut(self, node: FibNode):
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def _get_list(self, start: FibNode) -> list:
        result = []
        if start is None:
            return result
        current = start
        while True:
            result.append(current)
            current = current.right
            if current == start:
                break
        return result

    def __len__(self):
        return self._size

    def __repr__(self):
        min_val = (self._min_node.key, self._min_node.value) if self._min_node else None
        return f"FibonacciHeap(size={self._size}, min={min_val})"
