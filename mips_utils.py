class TypeNode:
    def __init__(self, name, parent_name, methods_names):
        self.name = name
        self.parent_name = parent_name
        self.methods = methods_names
        self.parent = None
        self._visited = False


class MipsTypeContext:
    def __init__(self):
        self.factory = {}
        self.topological_order = []

    def add_node(self,node):
        self.factory[node.name] = node

    def add_nodes(self,nodes):
        for node in nodes:
            self.add_node(node)

    def _define_node_parent(self, node):
        if node.parent_name in self.factory.keys():
            node.parent = self.factory[node.parent_name]

    def define_nodes_parent(self):
        for node in self.factory.values():
            self._define_node_parent(node)

    def dfs_topologicalsort(self):
        def dfs_visit_topologicalsort(node):
            if node.parent is None:
                node._visited = True
            elif node.parent._visited:
                node.methods += node.parent.methods
            else:
                dfs_visit_topologicalsort(node.parent)
            node._visited = True

        for type_node in self.factory.values():
            if not type_node._visited:
                dfs_visit_topologicalsort(type_node)
