from cil_hierarchy import *


def add_built_in(cool_to_cil):
        #OBJECT
        cool_to_cil.dottypes.append(CILTypeNode("Object", "None", [], ["Object_abort","Object_type_name","Object_copy"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("Object_abort",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "Object_abort"
        cool_to_cil.register_data("EXECUTION ABORTED")
        cool_to_cil.register_instruction(CILErrorMessageNode, cool_to_cil.dotdata.data[-1].vname)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("Object_type_name",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "Object_type_name"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo,  CILTypeNameNode("cool_to_cil"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("Object_copy",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "Object_copy"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILCopyNode("cool_to_cil"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        #IO
        cool_to_cil.dottypes.append(CILTypeNode("IO", "Object", [], ["IO_out_string","IO_out_int","IO_in_string","IO_in_int"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_out_string",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "IO_out_string"
        cool_to_cil.register_instruction(CILPrintStringNode, "cool_to_cil")
        cool_to_cil.register_instruction(CILReturnNode, "cool_to_cil")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_out_int",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "IO_out_int"
        cool_to_cil.register_instruction(CILPrintIntNode, "cool_to_cil") 
        cool_to_cil.register_instruction(CILReturnNode, "cool_to_cil")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_in_string",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "IO_in_string"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILReadStringNode())
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_in_int",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "IO_in_int"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILReadIntNode())
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        #Int
        cool_to_cil.dottypes.append(CILTypeNode("Int", "None"))
        cool_to_cil.dotcode.append(CILCodeNode())

        #String
        cool_to_cil.dottypes.append(CILTypeNode("String", "None", [], ["String_length","String_concat","String_substr"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("String_length",[CILArgNode("cool_to_cil")]))
        cool_to_cil.current_function_name = "String_length"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILLengthNode("cool_to_cil"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("String_concat",[CILArgNode("cool_to_cil"),CILArgNode("s")]))
        cool_to_cil.current_function_name = "String_concat"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILConcatNode("cool_to_cil", "s"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("String_substr",[CILArgNode("cool_to_cil"),CILArgNode("i"),CILArgNode("l")]))
        cool_to_cil.current_function_name = "String_substr"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILSubstringNode("cool_to_cil", "i", "l"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        #Bool
        cool_to_cil.dottypes.append(CILTypeNode("Bool", "None"))
        cool_to_cil.dotcode.append(CILCodeNode())
