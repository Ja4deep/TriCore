"""
Educational curriculum lessons for the Logic Circuit Simulator, matching TriCore's original structure.
"""

from __future__ import annotations

LESSONS_CHAMBER = [
    {
        "title": "What is a Logic Circuit?",
        "definition": "An interconnected network of ternary logic gates used to process and transform ternary information.",
        "explanation": [
            "Individual gates perform simple ternary logic operations, while complex tasks require many gates working together.",
            "Signals flow sequentially from inputs through gates to modify output lines.",
            "This structured flow forms the basis of all computer operations.",
        ],
        "hardware": "Modern processors contain vast networks of logic gates connected by signal pathways that process instructions and data.",
    },
    {
        "title": "Signal Flow in Ternary Circuits",
        "definition": "The unidirectional progression of signal transformations through path networks.",
        "explanation": [
            "Data pathways flow along clear, one-way paths in logic circuits.",
            "Outputs from early operations pass along connected copper paths to serve as the inputs for subsequent gates.",
            "This sequential data modification turns raw ternary streams into meaningful calculations.",
        ],
        "hardware": "Instruction decoders often use parallel evaluation networks so multiple logic decisions can be made simultaneously.",
    },
    {
        "title": "Series and Parallel Circuit Structures",
        "definition": "The arrangement of gates and signal paths that determines how ternary data moves through a circuit.",
        "explanation": [
            "Series linkages line up operations sequentially (like a MIN chain), requiring all elements to pass criteria consecutively.",
            "Parallel linkages evaluate paths simultaneously (like a MAX layout), offering alternative routing options.",
            "Modern processing engines mix these approaches to execute complex, multi-layered workflows smoothly.",
        ],
        "hardware": "Instruction decoders use parallel evaluation networks to unpack commands in a single clock tick.",
    },
]
