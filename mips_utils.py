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
            if node.parent is None:
                node._visited = True

            elif node.parent._visited:
                min_len_list = node.methods if len(node.methods) < len(node.parent.methods) else node.parent.methods
                max_len_list = node.methods if len(node.methods) >= len(node.parent.methods) else node.parent.methods

                # le quitamos el prefijo NombreDelTipo
                min_canonical_list = [method_name.split('_',maxsplit=1)[1] for method_name in min_len_list]
                max_canonical_list = [method_name.split('_',maxsplit=1)[1] for method_name in max_len_list]

                node.methods = [min_len_list[i] for i, method_name in min_canonical_list
                                if method_name not in max_canonical_list]
                node.methods += max_len_list

            else:
                dfs_visit_topologicalsort(node.parent)
            node._visited = True

        for type_node in self.factory.values():
            if not type_node._visited:
                dfs_visit_topologicalsort(type_node)
