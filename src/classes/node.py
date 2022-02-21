class Node:
    # label is id
    # info is label
    def __init__(self, label: int, info=None):
        self.info: list[dict] = []
        self.out_nodes: list[Node] = []
        self.in_nodes: list[Node] = []
        self.label: int = label

        if isinstance(info, dict) and len(info) > 0:
            self.info = [info]
        elif isinstance(info, list) and len(info) > 0:
            self.info = info

    def add_in_nodes(self, node):
        if node not in self.in_nodes:
            self.in_nodes.append(node)
            
    def add_out_nodes(self, node):
        if node not in self.out_nodes:
            self.out_nodes.append(node)

    def add_info(self, information):
        self.info.append(information)

    def add_adjacent(self, node):
        self.add_out_nodes(node)
        node.add_in_nodes(self)

    def print_info(self):
        for info in self.info:
            print(info)

    def get_label(self):
        return self.label

    def get_info(self):
        return self.info

    def get_info_str(self):
        str_info = ''
        for info in self.get_info():
            if str_info == '':
                str_info += info
            else:
                str_info += f'\n{info}'
        return str_info

    def get_in_nodes(self):
        return self.in_nodes

    def get_out_nodes(self):
        return self.out_nodes

    def set_label(self, label):
        self.label = label

    def set_out_nodes(self, out_nodes):
        self.out_nodes = out_nodes

    def set_in_nodes(self, in_nodes):
        self.in_nodes = in_nodes

    def __str__(self):
        out_nodes = []
        for out_node in self.out_nodes:
            out_nodes.append((self.label, out_node.label))
        ret = f'{self.label : <7} label: {self.info}\n{"adj:" : <7} {out_nodes}'
        return ret

    # def traverse(self, is_visited, graph):
    #     is_visited[self.label] = True
    #     if self not in graph:
    #         graph[self] = self.out_nodes
    #     for adj in self.out_nodes:
    #         if not is_visited[adj.get_label()]:
    #             adj.traverse(is_visited, graph)
