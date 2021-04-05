from sys import argv


class Box:
    def __init__(self, l, w, h):
        self.l = max(l, w, h)
        self.w = (l + w + h) - max(l, w, h) - min(l, w, h)
        self.h = min(l, w, h)

    def fit(self, box):
        if self.l < box.l and self.w < box.w and self.h < box.h:
            return True
        return False

    def __str__(self):
        return f"l: {self.l}, w: {self.w}, h: {self.h}"


class Graph:
    def __init__(self, n, boxes):
        self.graph = [[0] + [1] * n + [0] * (n + 1)]
        self.n = n * 2 + 2
        for i in range(n):
            matches = [0] * (n + 1)
            for box in boxes:
                if boxes[i].fit(box):
                    matches.append(1)
                else:
                    matches.append(0)
            matches.append(0)
            self.graph.append(matches)

        for i in range(n):
            self.graph.append([0] + [0] * (n * 2) + [1])

        self.graph.append([0] * (n * 2) + [0] * 2)

    def __str__(self):
        return str(self.graph)

    def BFS(self, s, t, parent):
        visited = [False] * self.n

        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    if ind == t:
                        parent[ind] = u
                        return True
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return False

    def FF(self, source, sink):
        parent = [-1] * self.n
        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


def main(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()

    boxes = []
    n = int(lines[0])
    for i in range(1, n + 1):
        dim = lines[i].split()
        boxes.append(Box(int(dim[0]), int(dim[1]), int(dim[2])))

    g = Graph(n, boxes)
    return n - g.FF(0, (n * 2 + 1))


if __name__ == "__main__":
    print(main(argv[1]))
