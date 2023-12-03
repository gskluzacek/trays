from __future__ import annotations
import sys
from queue import Queue
from queue import PriorityQueue
from itertools import count
from typing import List, Optional


class Graph:
    def __init__(self):
        self.matrix = []
        self.matrix_copy = []
        self.node_cnt = 0
        self.edge_cnt = 0
        self.node_to_index = {}
        self.index_to_node = []

    def read_graph(self, file_name):
        with open(file_name, "r") as gfh:
            self.process_nodes(gfh)
            self.initialize_matrix()
            self.process_edges(gfh)

    def process_nodes(self, gfh):
        self.node_cnt = int(gfh.readline().rstrip())
        for i in range(self.node_cnt):
            node_name = gfh.readline().rstrip()
            self.node_to_index[node_name] = i
            self.index_to_node.append(node_name)

    def initialize_matrix(self):
        self.matrix = [[0 for _ in range(self.node_cnt)] for _ in range(self.node_cnt)]

    def process_edges(self, gfh):
        self.edge_cnt = int(gfh.readline().rstrip())
        for i in range(self.edge_cnt):
            edge = gfh.readline().rstrip()
            node_from, node_to, edge_weight = edge.split()
            index_from = self.node_to_index[node_from]
            index_to = self.node_to_index[node_to]
            self.matrix[index_from][index_to] = int(edge_weight)

    def print_graph(self, file_name):
        with open(file_name, 'w') as gfh:
            self.write_nodes(gfh)
            self.wright_edges(gfh)

    def print_graph_stdout(self):
        self.write_nodes(sys.stdout)
        self.wright_edges(sys.stdout)

    def wright_edges(self, gfh):
        gfh.write(f"{self.edge_cnt}\n")
        for i, row in enumerate(self.matrix):
            for j, weight in enumerate(row):
                if weight > 0:
                    gfh.write(f"{self.index_to_node[i]} {self.index_to_node[j]} {weight}\n")

    def write_nodes(self, gfh):
        gfh.write(f"{self.node_cnt}\n")
        for node in self.index_to_node:
            gfh.write(f"{node}\n")

    # def write_nodes(self):
    #     print(f"{self.node_cnt}")
    #     for node in self.index_to_node:
    #         print(f"{node}")
    #     print(f"{self.edge_cnt}")
    #     for i in range(self.node_cnt):
    #         for j in range(self.node_cnt):
    #             if self.matrix[i][j]:
    #                 print(f"{self.index_to_node[i]} {self.index_to_node[j]} {self.matrix[i][j]}")

    def compute_topological_sort(self):
        print("Topological Sort:")
        top_sort = []
        node_queue = Queue()
        self.copy_matrix()
        self.get_starting_nodes(node_queue)
        while not node_queue.empty():
            row = node_queue.get()
            top_sort.append(row)
            self.process_out_going_edges(row, node_queue)
        if self.is_matrix_empty():
            print(" --> ".join([self.index_to_node[i] for i in top_sort]))
        else:
            print("This graph cannot be topologically sorted.")

    def copy_matrix(self):
        self.matrix_copy = [[self.matrix[j][i] for i in range(self.node_cnt)] for j in range(self.node_cnt)]

    def get_starting_nodes(self, node_queue):
        for col in range(self.node_cnt):
            self.process_in_coming_edges(col, node_queue)

    def process_out_going_edges(self, row, node_queue):
        for col in range(self.node_cnt):
            if self.matrix_copy[row][col] > 0:
                self.matrix_copy[row][col] = 0
                self.process_in_coming_edges(col, node_queue)

    def process_in_coming_edges(self, col, node_queue):
        no_incoming = True
        for row in range(self.node_cnt):
            if self.matrix_copy[row][col]:
                no_incoming = False
                break
        if no_incoming:
            node_queue.put(col)

    def is_matrix_empty(self):
        for row in self.matrix_copy:
            for weight in row:
                if weight:
                    return False
        return True

    def get_linked_items(self, from_index):
        return [(index, cost) for index, cost in enumerate(self.matrix[from_index]) if cost]

    def add_linked_items(self, prev_index: int, pq: PriorityQueue):
        for curr_index, cost in self.get_linked_items(prev_index):
            QueueItem(curr_index, prev_index, cost).add_to_queue(pq)

    def compute_shortest_paths(self, node_name):
        print(f"Shortest paths from {node_name}:")
        node_index = self.node_to_index[node_name]

        prev_list: List[Optional[int]] = [None] * self.node_cnt
        cost_list = [0] * self.node_cnt
        node_list = [False] * self.node_cnt
        node_list[node_index] = True        # set the source vertices to true as we will never have a path to ourselves

        pq = PriorityQueue()
        self.add_linked_items(node_index, pq)

        while not pq.empty() and not all(node_list):
            item = QueueItem.get_from_queue(pq)
            if not node_list[item.curr_ndx]:
                node_list[item.curr_ndx] = True
                prev_list[item.curr_ndx] = item.prev_ndx
                cost_list[item.curr_ndx] = item.cost
                for next_index, cost in self.get_linked_items(item.curr_ndx):
                    if not node_list[next_index]:
                        QueueItem(next_index, item.curr_ndx, item.cost + cost).add_to_queue(pq)

        for i in range(self.node_cnt):
            path = []
            if i == node_index:
                continue
            if not node_list[i]:
                print(f"No path from {self.index_to_node[node_index]} to {self.index_to_node[i]} found.")
                continue
            total_cost = cost_list[i]
            j = i
            while j != node_index:
                path.append(self.index_to_node[j])
                j = prev_list[j]
            path.append(self.index_to_node[node_index])
            path.reverse()
            string_path = ' --> '.join(path)
            string_path = f"{string_path} || {total_cost}"
            print(string_path)

        # v1 --> v3 --> v6 --> v4 || Weight: 13
        # No path from {node_name} to {unreachable_node} found.


class QueueItem:
    seq = count(1)

    def __init__(self, curr_ndx: int, prev_ndx: int, cost: int):
        self.curr_ndx: int = curr_ndx
        self.prev_ndx: int = prev_ndx
        self.cost: int = cost

    def add_to_queue(self, pq: PriorityQueue):
        queue_element = (self.cost, next(self.seq), self)
        pq.put(queue_element)

    @staticmethod
    def get_from_queue(pq: PriorityQueue) -> QueueItem:
        cost, nbr, item = pq.get()
        return item

def main():
    g = Graph()
    g.read_graph("graph1.txt")
    # g.print_graph_stdout()
    g.compute_shortest_paths("LAX")
    # print('  ', ', '.join(g.index_to_node))
    # for i, row in enumerate(g.matrix):
    #     print(g.index_to_node[i], row)
    # g.print_graph("output.txt")
    # g.compute_topological_sort()
    # print("-"*100)
    # print('  ', ', '.join(g.index_to_node))
    # for i, row in enumerate(g.matrix):
    #     print(g.index_to_node[i], row)

if __name__ == "__main__":
    main()