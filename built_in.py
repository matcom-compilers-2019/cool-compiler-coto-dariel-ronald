from cil_hierarchy import *

def add_built_in(cool_to_cil):
        cool_to_cil.dottypes.append(CILTypeNode("Object", "None", [], ["abort","type_name","copy"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("abort",[CILArgNode("cool_to_cil")]))
        cool_to_cil.define_internal_local()
        cool_to_cil.register_instruction(CILErrorMessage, "EXECUTION ABORTED")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("type_name",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILReturnNode, CILTypeOfNode("cool_to_cil"))

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("copy",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILReturnNode, CILCopyNode("cool_to_cil"))

        cool_to_cil.dottypes.append(CILTypeNode("IO", "Object", [], ["out_string","int_string","out_int","in_int"]))
        cilcodenode = CILCodeNode()
        cool_to_cil.dotcode.append(cilcodenode)
        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("out_string",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILPrintStringNode, "cool_to_cil")
        cool_to_cil.register_instruction(CILReturnNode, "cool_to_cil")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("out_int",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILPrintIntNode, "cool_to_cil") 
        cool_to_cil.register_instruction(CILReturnNode, "cool_to_cil")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("in_string",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILReturnNode, CILReadStringNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("in_int",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILReturnNode, CILReadIntNode())

        cool_to_cil.dottypes.append(CILTypeNode("Int", "None"))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dottypes.append(CILTypeNode("String", "None", ["length","concat","substr"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("length",[CILArgNode("cool_to_cil")]))
        cool_to_cil.register_instruction(CILReturnNode, CILLengthNode("cool_to_cil"))

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("concat",[CILArgNode("cool_to_cil"),CILArgNode("s")]))
        cool_to_cil.register_instruction(CILReturnNode, CILConcatNode("cool_to_cil", "s"))

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("substr",[CILArgNode("cool_to_cil"),CILArgNode("i"),CILArgNode("l")]))
        cool_to_cil.register_instruction(CILReturnNode, CILSubstringNode("cool_to_cil", "i", "l"))

        cool_to_cil.dottypes.append(CILTypeNode("Bool", "None"))
        cool_to_cil.dotcode.append(CILCodeNode())
