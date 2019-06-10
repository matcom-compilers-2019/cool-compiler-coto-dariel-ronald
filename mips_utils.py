from cil_hierarchy import CILTypeNode


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
        if node.parent_name in self.factory.keys() and node.parent is None:
            node.parent = self.factory[node.parent_name]

    def define_nodes_parent(self):
        for node in self.factory.values():
            self._define_node_parent(node)

    def update_methods_inheritence(self):
        def dfs_visit_topologicalsort(node: CILTypeNode):
            if node.parent is not None:

                if node.parent._visited:

                    # le quitamos el prefijo NombreDelTipo
                    node_canonical_list = [method_name.split('_',maxsplit=1)[1] for method_name in node.methods]
                    parent_canonical_list = [method_name.split('_',maxsplit=1)[1] for method_name in node.parent.methods]

                    node.methods += [node.parent.methods[i] for i, method_name in enumerate(parent_canonical_list)
                                    if method_name not in node_canonical_list]

                else:
                    dfs_visit_topologicalsort(node.parent)
            node._visited = True

        for type_node in self.factory.values():
            if not type_node._visited:
                dfs_visit_topologicalsort(type_node)
