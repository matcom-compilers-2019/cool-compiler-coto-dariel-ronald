import cil_hierarchy as cil
import visitor

class CILWriterVisitor(object):
    def __init__(self):
        self.output = []

    def emit(self, msg):
        self.output.append(msg)

    def black(self):
        self.output.append('')

    def get_value(self, value):
        return value if isinstance(value, int) else value.name

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.CILProgramNode)
    def visit(self, node:cil.CILProgramNode):
        self.emit('.TYPES')
        for x in node.dottypes:
            self.visit(x)
        self.black()

        self.emit('.DATA')
        for x in node.dotdata:
            self.visit(x)
        self.black()

        self.emit('.CODE')
        for x in node.dotcode:
            self.visit(x)


    @visitor.when(cil.CILTypeNode)
    def visit(self, node:cil.CILTypeNode):
        self.emit(f'    type {node.name}')
        self.black()
        self.emit("{")
        self.black()
        for x in node.attributes:
            self.emit(f'    attribute {x}')
            self.black()
        for x in node.methods:
            self.emit(f'    method {x}')
            self.black()
        self.emit('}')

    @visitor.when(cil.CILCodeNode)
    def visit(self, node:cil.CILCodeNode):
        for x in node.functions:
            self.visit(x)

    @visitor.when(cil.CILDataNode)
    def visit(self, node:cil.CILDataNode):
        self.emit(f'{node.vname} = {node.value}')

    @visitor.when(cil.CILFunctionNode)
    def visit(self, node:cil.CILFunctionNode):
        self.black()

        self.emit(f'function {node.fname} {{')
        for x in node.params:
            self.visit(x)
        if node.params:
            self.black()

        for x in node.localvars:
            self.visit(x)
        if node.localvars:
            self.black()

        for x in node.instructions:
            self.visit(x)
        self.emit('}')

    @visitor.when(cil.CILParamNode)
    def visit(self, node:cil.CILParamNode):
        pass

    @visitor.when(cil.CILLocalNode)
    def visit(self, node:cil.CILLocalNode):
        self.emit(f'    LOCAL {node.vinfo.name}')

    @visitor.when(cil.CILAssignNode)
    def visit(self, node:cil.CILAssignNode):
        dest = node.dest.name
        source = self.get_value(node.source)
        self.emit(f'    {dest} = {source}')

    @visitor.when(cil.CILPlusNode)
    def visit(self, node:cil.CILPlusNode):
        dest = node.dest.name
        left = self.get_value(node.left)
        right = self.get_value(node.right)
        self.emit(f'    {dest} = {left} + {right}')

    @visitor.when(cil.CILMinusNode)
    def visit(self, node:cil.CILMinusNode):
        dest = node.dest.name
        left = self.get_value(node.left)
        right = self.get_value(node.right)
        self.emit(f'    {dest} = {left} - {right}')

    @visitor.when(cil.CILStarNode)
    def visit(self, node:cil.CILStarNode):
        dest = node.dest.name
        left = self.get_value(node.left)
        right = self.get_value(node.right)
        self.emit(f'    {dest} = {left} * {right}')

    @visitor.when(cil.CILDivNode)
    def visit(self, node:cil.CILDivNode):
        dest = node.dest.name
        left = self.get_value(node.left)
        right = self.get_value(node.right)
        self.emit(f'    {dest} = {left} / {right}')

    @visitor.when(cil.CILGetAttribNode)
    def visit(self, node:cil.CILGetAttribNode):
        pass

    @visitor.when(cil.CILSetAttributeNode)
    def visit(self, node:cil.CILSetAttributeNode):
        pass

    @visitor.when(cil.CILGetIndexNode)
    def visit(self, node:cil.CILGetIndexNode):
        pass

    @visitor.when(cil.CILSetIndexNode)
    def visit(self, node:cil.CILSetIndexNode):
        pass
        

    @visitor.when(cil.CILAllocateNode)
    def visit(self, node:cil.CILAllocateNode):
        pass

    @visitor.when(cil.CILArrayNode)
    def visit(self, node:cil.CILArrayNode):
        pass

    @visitor.when(cil.CILTypeOfNode)
    def visit(self, node:cil.CILTypeOfNode):
        pass

    @visitor.when(cil.CILLabelNode)
    def visit(self, node:cil.CILLabelNode):
        self.emit(f'    {node.label}')

    @visitor.when(cil.CILGotoNode)
    def visit(self, node:cil.CILGotoNode):
        self.emit(f'    GOTO {node.label}')

    @visitor.when(cil.CILGotoIfNode)
    def visit(self, node: cil.CILGotoIfNode):
        self.emit(f'    GOTO {node.label} IF {node.holder.name}')

    @visitor.when(cil.CILStaticCallNode)
    def visit(self, node:cil.CILStaticCallNode):
        pass

    @visitor.when(cil.CILDinamicCallNode)
    def visit(self, node:cil.CILDinamicCallNode):
        self.emit(f'    VCALL {node.id}')

    @visitor.when(cil.CILArgNode)
    def visit(self, node:cil.CILArgNode):
        pass

    @visitor.when(cil.CILReturnNode)
    def visit(self, node:cil.CILReturnNode):
        value = self.get_value(node.value)
        value = "" if value is None else str(value)
        self.emit(f'    RETURN {value}')

    @visitor.when(cil.CILLoadNode)
    def visit(self, node: cil.CILLoadNode):
        dest = node.dest.name
        self.emit(f'    {dest} = LOAD {node.msg.vname}')

    @visitor.when(cil.CILLengthNode)
    def visit(self, node:cil.CILLengthNode):
        pass

    @visitor.when(cil.CILConcatNode)
    def visit(self, node:cil.CILConcatNode):
        self.emit(f'    CONCAT { node.first} {node.second}')

    @visitor.when(cil.CILPrefixNode)
    def visit(self, node:cil.CILPrefixNode):
        self.emit(f'    PREFIX { node.sub_string} {node.full_string}')

    @visitor.when(cil.CILSubstringNode)
    def visit(self, node:cil.CILSubstringNode):
        self.emit(f'    SUBSTRING { node.sub_string} {node.full_string}')

    @visitor.when(cil.CILToStrNode)
    def visit(self, node:cil.CILToStrNode):
        dest = node.dest.name
        ivalue = self.get_value(node.ivalue)
        self.emit(f'    {dest} = STR {ivalue}')

    @visitor.when(cil.CILReadNode)
    def visit(self, node:cil.CILReadNode):
        dest = node.dest.name
        self.emit(f'    {dest} = READ')

    @visitor.when(cil.CILPrintNode)
    def visit(self, node:cil.CILPrintNode):
        self.emit(f'    PRINT {node.str_addr.name}')