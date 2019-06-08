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
        for x in node.dotdata.data:
            self.visit(x)
        self.black()

        self.emit('.CODE')
        for x in node.dotcode:
            self.visit(x)

        self.emit('.STATIC FUNCTIONS')
        for x in node.static_functions:
            self.visit(x)


    @visitor.when(cil.CILTypeNode)
    def visit(self, node:cil.CILTypeNode):
        self.emit(f'    type {node.name}')
        self.emit("{")
        for x in node.attributes:
            self.emit(f'  attribute {x}')
            self.black()
        for x in node.methods:
            self.emit(f'  method {x}')
            self.black()
        self.emit('}')
        self.black()

    @visitor.when(cil.CILCodeNode)
    def visit(self, node:cil.CILCodeNode):
        for x in node.functions:
            self.visit(x)

    @visitor.when(cil.CILDataElementNode)
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
        self.emit(f'  PARAM {node.vinfo}')

    @visitor.when(cil.CILLocalNode)
    def visit(self, node:cil.CILLocalNode):
        self.emit(f'  LOCAL {node.vinfo}')

    @visitor.when(cil.CILAssignNode)
    def visit(self, node:cil.CILAssignNode):
        dest = None
        if type(node.dest) is cil.CILLocalNode:
            dest = node.dest.vinfo
        else:
            dest = node.dest
        source = node.source
        value = ""
        if type(node.source) is cil.CILLocalNode:
            value = node.source.vinfo
            self.emit(f'  {dest} = {value}')
        else:
            self.emit(f'  {dest} = {self.visit(source)}')

    @visitor.when(cil.CILPlusNode)
    def visit(self, node:cil.CILPlusNode):
        left = node.left
        right = node.right
        return f'  {left} + {right}'

    @visitor.when(cil.CILMinusNode)
    def visit(self, node:cil.CILMinusNode):
        left = node.left
        right = node.right
        return f'  {left} - {right}'

    @visitor.when(cil.CILStarNode)
    def visit(self, node:cil.CILStarNode):
        left = node.left
        right = node.right
        return f'  {left} * {right}'

    @visitor.when(cil.CILDivNode)
    def visit(self, node:cil.CILDivNode):
        left = node.left
        right = node.right
        return f'  {left} / {right}'

    @visitor.when(cil.CILGetAttributeNode)
    def visit(self, node:cil.CILGetAttributeNode):
        return f'  GET_ATTR {node.id}'

    @visitor.when(cil.CILSetAttributeNode)
    def visit(self, node:cil.CILSetAttributeNode):
        self.emit(f'  SET_ATTR {node.id} {node.value}')

    @visitor.when(cil.CILGetIndexNode)
    def visit(self, node: cil.CILGetIndexNode):
        return f'  GET_INDEX {node.id} {node.index}'

    @visitor.when(cil.CILSetIndexNode)
    def visit(self, node: cil.CILSetIndexNode):
        self.emit(f'  SET_INDEX {node.id} {node.index} {node.value}')

    @visitor.when(cil.CILAllocateNode)
    def visit(self, node: cil.CILAllocateNode):
        return f'  ALLOCATE {node.type_id}'

    @visitor.when(cil.CILArrayNode)
    def visit(self, node: cil.CILArrayNode):
        return f'  ARRAY {node.size}'

    @visitor.when(cil.CILTypeOfNode)
    def visit(self, node: cil.CILTypeOfNode):
        return f'  TYPE_OF {node.source}'

    @visitor.when(cil.CILLabelNode)
    def visit(self, node:cil.CILLabelNode):
        self.emit(f'LABEL {node.label}')

    @visitor.when(cil.CILGotoNode)
    def visit(self, node:cil.CILGotoNode):
        self.emit(f'  GOTO {node.label}')

    @visitor.when(cil.CILGotoIfNode)
    def visit(self, node:cil.CILGotoIfNode):
        self.emit(f'  GOTO {node.label} IF {self.visit(node.compare)}')

    @visitor.when(cil.CILStaticCallNode)
    def visit(self, node: cil.CILStaticCallNode):
        for x in node.params:
            self.emit(f'  PARAM {x}')
        return  f'  CALL {node.id}'

    @visitor.when(cil.CILDinamicCallNode)
    def visit(self, node: cil.CILDinamicCallNode):
        for x in node.params:
            self.emit(f'  PARAM {x}')
        if type(node.parent_type) is cil.CILLocalNode:
            value = node.parent_type.vinfo
            return f'  VCALL {node.id} {value}'
        else:
            return f'  VCALL {node.id} {self.visit(node.parent_type)}'

    @visitor.when(cil.CILBuiltInCallNode)
    def visit(self, node: cil.CILBuiltInCallNode):
        for x in node.params:
            self.emit(f'  PARAM {x}')
            return f'  BUILT_IN_CALL {node.id}'


    @visitor.when(str)
    def visit(self, node:str):
        return node

    @visitor.when(int)
    def visit(self, node: int):
        return node

    @visitor.when(cil.CILArgNode)
    def visit(self, node:cil.CILArgNode):
        self.emit(f'  ARG {node.id}')

    @visitor.when(cil.CILReturnNode)
    def visit(self, node:cil.CILReturnNode):
        value = ""
        if type(node.value) is cil.CILLocalNode:
            value = node.value.vinfo
        else:
            value = node.value
        self.emit(f'  RETURN {self.visit(value)}')

    @visitor.when(cil.CILLoadNode)
    def visit(self, node: cil.CILLoadNode):
        return f'  LOAD {node.msg}'

    @visitor.when(cil.CILLengthNode)
    def visit(self, node: cil.CILLengthNode):
        return f'  LENGTH {node.id}'

    @visitor.when(cil.CILConcatNode)
    def visit(self, node:cil.CILConcatNode):
        return f'  CONCAT { node.first} {node.second}'

    @visitor.when(cil.CILPrefixNode)
    def visit(self, node:cil.CILPrefixNode):
        self.emit(f'  PREFIX { node.sub_string} {node.full_string}')

    @visitor.when(cil.CILSubstringNode)
    def visit(self, node:cil.CILSubstringNode):
        return f'  SUBSTRING { node.s} {node.i} {node.l}'

    @visitor.when(cil.CILToStrNode)
    def visit(self, node:cil.CILToStrNode):
        dest = node.dest.name
        ivalue = self.get_value(node.ivalue)
        self.emit(f'  {dest} = STR {ivalue}')

    @visitor.when(cil.CILReadIntNode)
    def visit(self, node:cil.CILReadIntNode):
        self.emit(f'  READINT')

    @visitor.when(cil.CILReadStringNode)
    def visit(self, node: cil.CILReadStringNode):
        self.emit(f'  READSTRING')

    @visitor.when(cil.CILPrintIntNode)
    def visit(self, node:cil.CILPrintIntNode):
        self.emit(f'  PRINT {node.int_addr}')

    @visitor.when(cil.CILPrintStringNode)
    def visit(self, node: cil.CILPrintStringNode):
        self.emit(f'  PRINT {node.str_addr}')

    @visitor.when(cil.CILLowerEqualThanNode)
    def visit(self, node: cil.CILLowerEqualThanNode):
        return f'  {node.left_expr} <= {node.right_expr}'

    @visitor.when(cil.CILLowerThanNode)
    def visit(self, node: cil.CILLowerThanNode):
        return f'  {node.left_expr} < {node.right_expr}'

    @visitor.when(cil.CILEqualThanNode)
    def visit(self, node: cil.CILEqualThanNode):
        return f'  {node.left_expr} == {node.right_expr}'

    @visitor.when(cil.CILGetParentNode)
    def visit(self, node: cil.CILGetParentNode):
        return f'  GET_PARENT {node.id}'

    @visitor.when(cil.CILErrorMessageNode)
    def visit(self, node: cil.CILErrorMessageNode):
        self.emit(f'  ABORT {node.msg}')