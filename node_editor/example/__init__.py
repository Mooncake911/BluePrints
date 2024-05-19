from .Add_node import Add_Node
from .Branch_node import Branch_Node
from .Event_node import Event_Node
from .Print_node import Print_Node
from .Speed_node import Speed_Node


from .Arithmetic_nodes import Arithmetic_Nodes
from .Data_Types_nodes import Data_Types_Nodes
from .Device_nodes import Device_Node
from .Logic_nodes import Logic_Nodes
from .Time_nodes import Time_Nodes

Root_Nodes = (Add_Node, Branch_Node, Event_Node, Print_Node, Speed_Node)

NODES_LIST = {
    "Arithmetic Nodes": Arithmetic_Nodes,
    "Data Types Nodes": Data_Types_Nodes,
    # "Device Nodes": Device_Nodes,
    "Logic Nodes": Logic_Nodes,
    "Time Nodes": Time_Nodes,
    "root": Root_Nodes
}
