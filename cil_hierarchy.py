class CILNode:
    pass


class CILProgramNode(CILNode):
    def __init__(self, dottypes, dotdata, dotcode, static_functions):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode
        self.static_functions = static_functions


class CILTypeNode(CILNode):
    def __init__(self, name, parent_name,attributes = None, methods = None):
        self.name = name

        if attributes is None:
            self.attributes = []
        else:
            self.attributes = attributes

        if methods is None:
            self.methods = []
        else:
            self.methods = methods

        self.parent_name = parent_name
        self.parent = None
        self._visited = False

class CILDataNode(CILNode):
    def __init__(self):
        self.data = []


# estos seran los elementos que iran dentro de la propiedad data del tipo CILDataNode
class CILDataElementNode(CILNode):
    def __init__(self, vname, value):
        self.vname = vname
        self.value = value


class CILAllocateNode(CILNode):
    def __init__(self, type_id):
        self.type_id = type_id


class CILCodeNode(CILNode):
    def __init__(self, functs = None):
        if functs is None:
            self.functions = []
        else:
            self.functions = functs


class CILFunctionNode(CILNode):
    def __init__(self, fname, params = None, localvars = None, instructions = None):
        self.fname = fname
        if params is None:
            self.params = []
        else:
            self.params = params

        if localvars is None:
            self.localvars = []
        else:
            self.localvars = localvars

        if instructions is None:
            self.instructions = []
        else:
            self.instructions = instructions


class CILParamNode(CILNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILLocalNode(CILNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILInstructionNode(CILNode):
    pass


class CILAssignNode(CILInstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class CILArithmeticNode(CILInstructionNode):
    def __init__(self, left = None, right = None):
        self.left = left
        self.right = right


class CILPlusNode(CILArithmeticNode):
    pass


class CILMinusNode(CILArithmeticNode):
    pass


class CILStarNode(CILArithmeticNode):
    pass


class CILDivNode(CILArithmeticNode):
    pass


class CILGetAttributeNode(CILInstructionNode):
    def __init__(self, attrName, localv):
        self.attrName = attrName
        self.localv = localv


class CILSetAttributeNode(CILInstructionNode):
    def __init__(self, attrName, localv, value):
        self.attrName = attrName
        self.value = value
        self.localv = localv


class CILGetIndexNode(CILInstructionNode):
    def __init__(self, localv, index):
        self.localv = localv
        self.index = index


class CILSetIndexNode(CILInstructionNode):
    def __init__(self, localv, index, value):
        self.localv = localv
        self.index = index
        self.value = value


class CILArrayNode(CILInstructionNode):
    def __init__(self, size):
        self.size = size


class CILTypeOfNode(CILInstructionNode):
    def __init__(self, source):
        self.source = source


class CILLabelNode(CILInstructionNode):
    def __init__(self, label):
        self.label = label


class CILGotoNode(CILInstructionNode):
    def __init__(self, label):      
        self.label = label


class CILGotoIfNode(CILInstructionNode):
    def __init__(self, compare, label):   
        self.compare = compare
        self.label = label


class CILDynamicCallNode(CILInstructionNode):
    def __init__(self, fid, instance):
        self.fid = fid
        self.instance = instance
        self.params = []


class CILStaticCallNode(CILInstructionNode):
    def __init__(self, fid, parent_type, instance):
        self.fid = fid
        self.parent_type = parent_type
        self.instance = instance
        self.params = []


class CILBuiltInCallNode(CILInstructionNode):
    def __init__(self, fid):
        self.fid = fid
        self.params = []


class CILGetParentNode(CILInstructionNode):
    def __init__(self, parent_label):
        self.parentLabel = parent_label


class CILArgNode(CILInstructionNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILReturnNode(CILInstructionNode):
    def __init__(self, value = None):
        self.value = value


class CILLoadNode(CILInstructionNode):
    def __init__(self, msg):
        self.msg = msg


class CILLengthNode(CILInstructionNode):
    def __init__(self, localv):
        self.localv = localv


class CILConcatNode(CILInstructionNode):
    def __init__(self, s1, s2):
        self.str1 = s1
        self.str2 = s2


class CILPrefixNode(CILInstructionNode):
    def __init__(self, s1, s2):
        self.sub_string = s1
        self.full_string = s2


class CILSubstringNode(CILInstructionNode):
    def __init__(self, str1, index, length):
        self.str1 = str1
        self.index = index
        self.length = length


class CILToStrNode(CILInstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class CILReadStringNode(CILInstructionNode):
    pass


class CILReadIntNode(CILInstructionNode):
    pass


class CILPrintIntNode(CILInstructionNode):
    def __init__(self, int_addr):
        self.int_addr = int_addr


class CILPrintStringNode(CILInstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class CILIsVoidNode(CILInstructionNode):
    def __init__(self,is_void_value):
        self.is_void = is_void_value


class CILIntegerComplementNode(CILInstructionNode):
    def __init__(self,value):
        self.complement = value


class CILNewTypeNode(CILInstructionNode):
    def __init__(self,type):
        self.type = type


class CILErrorMessageNode(CILInstructionNode):
    def __init__(self,msg):
        self.msg = msg


class CILAbortNode(CILInstructionNode):
    pass


class CILTypeNameNode(CILInstructionNode):
    def __init__(self, type_to_get):
        self.type_to_get = type_to_get


# class CILNegationNode(CILInstructionNode):
#     def __init__(self, localv):
#         self.localv = localv


class CILLowerThanNode(CILInstructionNode):
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr


class CILLowerEqualThanNode(CILInstructionNode):
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr


class CILEqualThanNode(CILInstructionNode):
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr


class CILCopyNode(CILInstructionNode):
    def __init__(self, localv):
        self.localv = localv
