"""Shared educational enrichment for Learning Center lessons."""

from __future__ import annotations

from copy import deepcopy

from learn_center.types import CurriculumSection, Lesson, LessonSection

ReviewSummary = dict[str, list[str]]


SECTION_PERSPECTIVES: dict[str, list[str]] = {
    "Foundations of Number Systems": [
        "General concept",
        "- A number system is a representation method for quantities.",
        "- The quantity stays the same when the notation changes.",
        "",
        "Binary implementation",
        "- Base 2 uses the digit values 0 and 1.",
        "- Each place is a power of 2.",
        "",
        "Ternary implementation",
        "- Ordinary base 3 uses 0, 1, and 2.",
        "- Balanced ternary uses digit values -1, 0, and +1.",
        "",
        "TriCore connection",
        "- Practice these ideas in the Number System Converter.",
    ],
    "Number Representation": [
        "General concept",
        "- Computers represent information using agreed patterns of states.",
        "- The same pattern can mean different things under different rules.",
        "",
        "Binary implementation",
        "- A bit stores one of two states.",
        "- Signed binary integers commonly use formats such as two's complement.",
        "",
        "Ternary implementation",
        "- A trit stores one of three states.",
        "- Balanced ternary can encode sign through the digit values themselves.",
        "",
        "TriCore connection",
        "- Use the converters to compare how the same value is represented.",
    ],
    "Number System Conversion": [
        "General concept",
        "- Conversion changes notation while preserving value.",
        "- A correct conversion can always be checked by converting back.",
        "",
        "Binary implementation",
        "- Binary conversion uses powers of 2 and division by 2.",
        "",
        "Ternary implementation",
        "- Ordinary ternary uses powers of 3 and division by 3.",
        "- Balanced ternary also uses powers of 3, but its digits may be negative.",
        "",
        "TriCore connection",
        "- Practice the methods in the Number System Converter.",
    ],
    "Ternary Arithmetic": [
        "General concept",
        "- Arithmetic algorithms depend on place value and base.",
        "- Carrying, borrowing, shifting, and remainders are base rules.",
        "",
        "Binary implementation",
        "- Binary carries when a column total reaches 2.",
        "",
        "Ternary implementation",
        "- Ternary carries when a column total reaches 3.",
        "- A borrow into a ternary column is worth 3 of that column.",
        "",
        "TriCore connection",
        "- Try these rules in the Ternary Arithmetic Engine.",
    ],
    "Digital Logic": [
        "General concept",
        "- Digital logic processes information using a finite set of signal levels.",
        "- A gate is a rule that maps input states to an output state.",
        "",
        "Binary implementation",
        "- Binary logic uses two states, commonly written 0 and 1.",
        "",
        "Ternary implementation",
        "- Ordinary ternary logic uses 0, 1, and 2.",
        "- Balanced ternary logic can use negative, zero, and positive states.",
        "",
        "TriCore connection",
        "- Explore gate rules in the Digital Logic Laboratory.",
    ],
    "Logic Circuit Simulator": [
        "General concept",
        "- A circuit connects components so signals move from inputs to outputs.",
        "- Simulation evaluates those connections without physical hardware.",
        "",
        "Binary implementation",
        "- Binary circuits propagate two-state signals through gates.",
        "",
        "Ternary implementation",
        "- Ternary circuits propagate three-state signals through gates.",
        "- More states mean more truth-table rows and more validation work.",
        "",
        "TriCore connection",
        "- Build and test examples in the Logic Circuit Simulator.",
    ],
    "Computer Architecture": [
        "General concept",
        "- Computer architecture organizes representation, logic, memory, and control.",
        "- Different architectures can implement the same computing ideas differently.",
        "",
        "Binary implementation",
        "- Modern industry mostly uses binary because two-state electronics are reliable and standardized.",
        "",
        "Ternary implementation",
        "- Ternary architectures use three-state digits and can use balanced ternary arithmetic.",
        "- Setun is a historical example of a balanced ternary computer.",
        "",
        "TriCore connection",
        "- Use the Learning Center with the logic and arithmetic modules to compare designs.",
    ],
    "Extras": [
        "General concept",
        "- Reference material should connect vocabulary, examples, and common mistakes.",
        "",
        "Binary implementation",
        "- Binary examples show the dominant modern implementation.",
        "",
        "Ternary implementation",
        "- Ternary examples show TriCore's primary alternative model.",
        "",
        "TriCore connection",
        "- Return to these pages when using the converter, arithmetic, logic, and circuit modules.",
    ],
}


SECTION_COMPARISONS: dict[str, list[str]] = {
    "Foundations of Number Systems": [
        "System             Base  Digit values        Digit name",
        "Decimal            10    0 through 9         digit",
        "Binary             2     0, 1                bit",
        "Ordinary Ternary   3     0, 1, 2             trit",
        "Balanced Ternary   3     T, 0, 1             trit",
    ],
    "Number Representation": [
        "Idea               Binary example       Ternary example",
        "Smallest unit      bit                  trit",
        "State count        2                    3",
        "Unsigned digits    0, 1                 0, 1, 2",
        "Signed approach    two's complement     balanced digits",
    ],
    "Number System Conversion": [
        "Conversion task    Binary method        Ternary method",
        "Read to decimal    powers of 2          powers of 3",
        "Write from decimal divide by 2          divide by 3",
        "Check result       expand places        expand places",
        "TriCore module     converters           converters",
    ],
    "Ternary Arithmetic": [
        "Arithmetic idea    Binary               Ternary",
        "Carry threshold    2                    3",
        "Borrow value       2 of lower place     3 of lower place",
        "Left shift         multiply by 2        multiply by 3",
        "TriCore module     arithmetic engine    arithmetic engine",
    ],
    "Digital Logic": [
        "Logic idea         Binary               Ternary",
        "Signal states      2                    3",
        "One-input rows     2                    3",
        "Two-input rows     4                    9",
        "TriCore module     logic laboratory     logic laboratory",
    ],
    "Logic Circuit Simulator": [
        "Circuit idea       Binary circuit       Ternary circuit",
        "Signal alphabet    two states           three states",
        "Gate table size    smaller              larger",
        "Propagation        through connections  through connections",
        "TriCore module     simulator            simulator",
    ],
    "Computer Architecture": [
        "Architecture idea  Binary               Ternary",
        "Digit unit         bit                  trit",
        "Common status      industry standard    historical/research use",
        "Hardware issue     two stable states    three stable states",
        "TriCore focus      comparison           ternary exploration",
    ],
    "Extras": [
        "Reference area     Binary view          Ternary view",
        "Vocabulary         bit, base 2          trit, base 3",
        "Logic              two-valued           three-valued",
        "Arithmetic         carry at 2           carry at 3",
        "Architecture       modern standard      alternative model",
    ],
}


REVIEW_AND_SUMMARY: dict[str, ReviewSummary] = {
    "What is a Number System?": {
        "review": [
            "1. What is the difference between a number and a numeral?",
            "2. Why does a digit's position change its value?",
            "3. How can 17, 10001, and 122 describe the same quantity?",
        ],
        "summary": [
            "- Defined a number system as symbols plus rules.",
            "- Separated quantity from representation.",
            "- Connected positional notation to decimal, binary, and ternary.",
        ],
    },
    "Decimal Number System": {
        "review": [
            "1. Why is decimal called base 10?",
            "2. What place values are used in the number 2048?",
            "3. Why do computers not have to use decimal internally?",
        ],
        "summary": [
            "- Reviewed decimal digits and powers of 10.",
            "- Expanded decimal numbers by place value.",
            "- Distinguished human familiarity from hardware suitability.",
        ],
    },
    "Binary Number System": {
        "review": [
            "1. What digit values are allowed in binary?",
            "2. Why does binary 10001 equal decimal 17?",
            "3. Why is binary practical for electronic circuits?",
        ],
        "summary": [
            "- Defined binary as base 2.",
            "- Converted binary by powers of 2.",
            "- Connected bits to reliable two-state hardware.",
        ],
    },
    "Ternary Number System": {
        "review": [
            "1. What is a trit?",
            "2. Why does ternary 122 equal decimal 17?",
            "3. Why can ternary sometimes use fewer digits than binary?",
        ],
        "summary": [
            "- Defined ordinary ternary as base 3.",
            "- Used powers of 3 to read ternary numerals.",
            "- Compared binary and ternary representations of the same value.",
        ],
    },
    "Balanced Ternary": {
        "review": [
            "1. What value does T represent in TriCore?",
            "2. How do you negate a balanced ternary number?",
            "3. Why is balanced ternary different from ordinary ternary?",
        ],
        "summary": [
            "- Defined balanced ternary digit values T, 0, and 1.",
            "- Evaluated balanced ternary with powers of 3.",
            "- Saw how signs can be represented inside the digits.",
        ],
    },
    "Positional Number Systems": {
        "review": [
            "1. What makes a number system positional?",
            "2. Why is 102 in ternary not the same value as 102 in decimal?",
            "3. How do place values change when the base changes?",
        ],
        "summary": [
            "- Explained position as a digit's weight.",
            "- Compared decimal, binary, and ternary place values.",
            "- Identified a common error when reading non-decimal numerals.",
        ],
    },
    "Bits vs Trits": {
        "review": [
            "1. What is the difference between a bit and a trit?",
            "2. How many patterns can three trits represent?",
            "3. Why does more states per digit not automatically mean better hardware?",
        ],
        "summary": [
            "- Compared two-state bits with three-state trits.",
            "- Counted patterns using powers of the base.",
            "- Balanced information density against hardware reliability.",
        ],
    },
    "How Computers Store Numbers": {
        "review": [
            "1. What does a memory cell physically store?",
            "2. Why do leading zeros matter in fixed-width storage?",
            "3. How can the same bit pattern have different meanings?",
        ],
        "summary": [
            "- Described storage as physical states plus interpretation.",
            "- Introduced fixed-width number fields.",
            "- Connected representation rules to numbers, text, and formats.",
        ],
    },
    "Signed Number Representation": {
        "review": [
            "1. Why do computers need a rule for negative numbers?",
            "2. How can binary and ternary systems represent signed values differently?",
            "3. Why is two's complement a binary implementation rather than the only possible signed format?",
        ],
        "summary": [
            "- Explained why signed values need an interpretation rule.",
            "- Compared binary signed formats with balanced ternary digits.",
            "- Related balanced ternary to symmetric signed representation.",
        ],
    },
    "Why Balanced Ternary is Special": {
        "review": [
            "1. Why is balanced ternary symmetric around zero?",
            "2. How does swapping 1 and T negate a value?",
            "3. What hardware challenge remains even with elegant notation?",
        ],
        "summary": [
            "- Focused on the symmetry of -1, 0, and +1.",
            "- Practiced negation by digit swapping.",
            "- Separated mathematical elegance from engineering difficulty.",
        ],
    },
    "Decimal to/from Binary": {
        "review": [
            "1. What general rule lets any positional base convert to decimal?",
            "2. How do binary conversion steps differ from ternary conversion steps?",
            "3. Where can you practice binary and ternary conversion in TriCore?",
        ],
        "summary": [
            "- Treated binary conversion as one case of positional conversion.",
            "- Compared division by 2 with the base-3 method used for ternary.",
            "- Connected conversion skills to the Number System Converter.",
        ],
    },
    "Decimal to/from Ternary": {
        "review": [
            "1. What place values are used in ternary 2012?",
            "2. Why does dividing by 3 produce ternary digits?",
            "3. How can you check a ternary conversion?",
        ],
        "summary": [
            "- Converted ternary to decimal using powers of 3.",
            "- Converted decimal to ternary using repeated division by 3.",
            "- Verified answers by converting back to decimal.",
        ],
    },
    "Binary to/from Ternary": {
        "review": [
            "1. Why is decimal a reliable bridge between binary and ternary?",
            "2. Why does fixed bit grouping work for hexadecimal but not ternary?",
            "3. Convert binary 10001 to ternary and explain the steps.",
        ],
        "summary": [
            "- Used decimal as an intermediate representation.",
            "- Explained why base 2 and base 3 do not group neatly.",
            "- Practiced a full binary-to-ternary conversion.",
        ],
    },
    "Balanced Ternary Conversion": {
        "review": [
            "1. What does T contribute to a place-value sum?",
            "2. Why can remainder 2 be written as T with a carry?",
            "3. How do you verify 1T0T as decimal 17?",
        ],
        "summary": [
            "- Read balanced ternary with signed digit values.",
            "- Converted decimal values using carry adjustment.",
            "- Checked balanced ternary by expanding place values.",
        ],
    },
    "Common Conversion Mistakes": {
        "review": [
            "1. Why is reading 102 as one hundred two a base error?",
            "2. What happens if you read division remainders in the wrong order?",
            "3. Which digits are valid in binary, ordinary ternary, and balanced ternary?",
        ],
        "summary": [
            "- Identified common base-conversion errors.",
            "- Reinforced valid digit sets for each system.",
            "- Practiced checking conversions by reversing the process.",
        ],
    },
    "Ternary Addition": {
        "review": [
            "1. When does a ternary addition column carry?",
            "2. Why is 2 + 1 written as 10 in ternary?",
            "3. Add 12 and 2 in ternary and explain the carry.",
        ],
        "summary": [
            "- Applied ordinary addition using base-3 digits.",
            "- Carried when a column total reached 3.",
            "- Checked a ternary sum against decimal arithmetic.",
        ],
    },
    "Ternary Subtraction": {
        "review": [
            "1. How much is one borrow worth in a ternary column?",
            "2. Why does 0 - 1 require borrowing?",
            "3. How can decimal checking confirm a ternary subtraction?",
        ],
        "summary": [
            "- Used borrowing in base 3.",
            "- Worked through a subtraction with a zero in the top number.",
            "- Verified the result by comparing decimal values.",
        ],
    },
    "Ternary Multiplication": {
        "review": [
            "1. Why is 2 x 2 written as 11 in ternary?",
            "2. What does appending one zero do to a ternary value?",
            "3. Why should partial products be shifted by powers of 3?",
        ],
        "summary": [
            "- Used ternary single-digit multiplication facts.",
            "- Tracked carries during multiplication.",
            "- Connected left shifts to multiplying by 3.",
        ],
    },
    "Ternary Division": {
        "review": [
            "1. What digit values can appear in a ternary quotient?",
            "2. Why does 101 divided by 2 produce quotient 12?",
            "3. What role does the remainder play in long division?",
        ],
        "summary": [
            "- Treated ternary division as ordinary long division in base 3.",
            "- Followed quotient digits one step at a time.",
            "- Used decimal meaning to check the result.",
        ],
    },
    "Carry and Borrow in Base-3": {
        "review": [
            "1. Why is a carry worth 3 in ternary?",
            "2. How is 2 + 2 handled in one ternary column?",
            "3. What changes in arithmetic circuits when the base changes?",
        ],
        "summary": [
            "- Defined carry and borrow as place-value actions.",
            "- Compared base-3 carrying with decimal carrying.",
            "- Connected arithmetic rules to circuit design.",
        ],
    },
    "What is Digital Logic?": {
        "review": [
            "1. What makes a signal digital?",
            "2. Why are discrete signal ranges useful in noisy hardware?",
            "3. How do gates support larger computer systems?",
        ],
        "summary": [
            "- Defined digital logic as operations on discrete states.",
            "- Connected symbolic values to physical signals.",
            "- Positioned gates as building blocks of computation.",
        ],
    },
    "Logic Gates": {
        "review": [
            "1. What does a logic gate do?",
            "2. How does the number of signal states affect a gate's rule?",
            "3. Why must both binary and ternary gates define their input-output behavior exactly?",
        ],
        "summary": [
            "- Defined logic gates as input-output rules.",
            "- Compared binary two-state gates with ternary three-state gates.",
            "- Connected gate rules to the Digital Logic Laboratory.",
        ],
    },
    "Truth Tables": {
        "review": [
            "1. What information does a truth table contain?",
            "2. Why does a two-input ternary gate have 9 rows?",
            "3. How can truth tables help debug circuits?",
        ],
        "summary": [
            "- Used truth tables to list every input case.",
            "- Compared binary and ternary table sizes.",
            "- Treated truth tables as a verification tool.",
        ],
    },
    "Binary Logic vs Ternary Logic": {
        "review": [
            "1. What general idea do binary and ternary logic share?",
            "2. How does changing from two states to three states change the design work?",
            "3. Why is a ternary computer not just a renamed binary computer?",
        ],
        "summary": [
            "- Treated binary and ternary as finite-state logic systems.",
            "- Counted how input combinations grow.",
            "- Connected logic choices to storage, gates, and arithmetic.",
        ],
    },
    "Universal Gates": {
        "review": [
            "1. What does it mean for a gate to be universal?",
            "2. Why does universality depend on the chosen logic system?",
            "3. Why can a binary universal-gate fact not simply be copied into ternary logic?",
        ],
        "summary": [
            "- Defined universal gates.",
            "- Used binary NAND as one implementation example.",
            "- Avoided assuming binary facts automatically transfer to ternary logic.",
        ],
    },
    "Signal Levels in Ternary Logic": {
        "review": [
            "1. What are three possible physical signal states for ternary logic?",
            "2. What is a noise margin?",
            "3. Why can a middle signal level be difficult to maintain?",
        ],
        "summary": [
            "- Connected ternary values to physical signal levels.",
            "- Explained noise margins in plain language.",
            "- Identified reliability as a central hardware challenge.",
        ],
    },
    "What is a Logic Circuit?": {
        "review": [
            "1. What parts make up a logic circuit?",
            "2. How does an AND gate example produce an output?",
            "3. Why is simulation useful before building hardware?",
        ],
        "summary": [
            "- Defined a logic circuit as connected components.",
            "- Followed inputs through a simple gate.",
            "- Used simulation as a learning and testing tool.",
        ],
    },
    "Signal Propagation": {
        "review": [
            "1. What is signal propagation?",
            "2. Why must some gates wait for other gates to produce outputs?",
            "3. How does propagation relate to real circuit delay?",
        ],
        "summary": [
            "- Traced signals through dependent gates.",
            "- Explained evaluation order in a simulator.",
            "- Connected simulated propagation to physical timing.",
        ],
    },
    "Series vs Parallel Gates": {
        "review": [
            "1. What is a series-style logic path?",
            "2. How does a parallel structure differ?",
            "3. Why can circuit shape affect delay?",
        ],
        "summary": [
            "- Compared series and parallel circuit structures.",
            "- Connected structure to dependency and timing.",
            "- Emphasized careful wiring in the simulator.",
        ],
    },
    "Circuit Evaluation": {
        "review": [
            "1. What does circuit evaluation compute?",
            "2. Why are dependencies important during evaluation?",
            "3. Name two circuit problems a simulator should report.",
        ],
        "summary": [
            "- Defined circuit evaluation.",
            "- Listed a practical evaluation sequence.",
            "- Identified validation errors that prevent reliable output.",
        ],
    },
    "Combinational Circuits": {
        "review": [
            "1. What defines a combinational circuit?",
            "2. How is a combinational circuit different from memory?",
            "3. Name two examples of combinational circuits.",
        ],
        "summary": [
            "- Defined outputs that depend only on current inputs.",
            "- Contrasted combinational logic with memory circuits.",
            "- Connected combinational circuits to CPU building blocks.",
        ],
    },
    "Building a Ternary Circuit": {
        "review": [
            "1. Why must the signal encoding be chosen first?",
            "2. How many rows does a two-input ternary gate need?",
            "3. Why should small circuit pieces be tested before full systems?",
        ],
        "summary": [
            "- Planned ternary circuits from encodings and gate rules.",
            "- Emphasized complete truth tables.",
            "- Used incremental testing to reduce design errors.",
        ],
    },
    "Why Computers Use Binary": {
        "review": [
            "1. Why do two signal states support reliable electronics?",
            "2. What engineering factors helped binary become dominant?",
            "3. Why does an ecosystem matter in computer architecture?",
        ],
        "summary": [
            "- Explained binary's hardware reliability.",
            "- Connected binary dominance to manufacturing and tools.",
            "- Distinguished practical success from mathematical necessity.",
        ],
    },
    "Why Ternary Computers Exist": {
        "review": [
            "1. Why is ternary mathematically interesting?",
            "2. What did Setun demonstrate?",
            "3. Why do engineers study alternatives to binary?",
        ],
        "summary": [
            "- Explained motivations for ternary computing.",
            "- Identified Setun as a real balanced ternary computer.",
            "- Treated ternary as both historical and educationally valuable.",
        ],
    },
    "Advantages of Ternary Computing": {
        "review": [
            "1. How many patterns can three trits represent?",
            "2. What advantage does balanced ternary give signed values?",
            "3. Why do representation advantages not settle hardware design?",
        ],
        "summary": [
            "- Reviewed information density in trits.",
            "- Highlighted balanced arithmetic notation.",
            "- Kept representation benefits separate from total system costs.",
        ],
    },
    "Challenges of Ternary Hardware": {
        "review": [
            "1. Why is a stable middle state hard to engineer?",
            "2. How can smaller noise margins affect reliability?",
            "3. What parts of the binary ecosystem would ternary hardware need to replace or integrate with?",
        ],
        "summary": [
            "- Identified physical challenges in three-state hardware.",
            "- Explained noise margin pressure.",
            "- Connected hardware feasibility to tools and manufacturing.",
        ],
    },
    "Historical Ternary Computers": {
        "review": [
            "1. What was Setun?",
            "2. Why is Setun historically important?",
            "3. What claim about ternary computers should be avoided?",
        ],
        "summary": [
            "- Located Setun in real computing history.",
            "- Connected balanced ternary to an actual machine.",
            "- Avoided exaggerated claims about modern ternary adoption.",
        ],
    },
    "Future of Ternary Computing": {
        "review": [
            "1. What would need to improve for ternary computing to become practical?",
            "2. Why might ternary remain useful in education and research?",
            "3. Why is elegance alone not enough for a new architecture to win?",
        ],
        "summary": [
            "- Considered realistic future roles for ternary computing.",
            "- Listed engineering requirements for adoption.",
            "- Balanced research interest with binary's practical strength.",
        ],
    },
    "Frequently Asked Questions": {
        "review": [
            "1. What is the difference between ternary notation and a ternary computer?",
            "2. Why is balanced ternary still base 3?",
            "3. What makes Setun relevant to this course?",
        ],
        "summary": [
            "- Revisited common beginner questions.",
            "- Corrected misunderstandings about ternary and balanced ternary.",
            "- Connected the answers back to the main course themes.",
        ],
    },
    "Fun Facts": {
        "review": [
            "1. Why are powers of three important in ternary notation?",
            "2. What makes balanced ternary negation memorable?",
            "3. Why should radix-economy facts be interpreted carefully?",
        ],
        "summary": [
            "- Collected memorable facts without overstating them.",
            "- Reinforced powers of 3 and balanced negation.",
            "- Connected historical facts to accurate engineering judgment.",
        ],
    },
    "Glossary of Terms": {
        "review": [
            "1. What is the difference between base and place value?",
            "2. What is the difference between a bit and a trit?",
            "3. How are truth tables used in logic design?",
        ],
        "summary": [
            "- Reviewed vocabulary for number systems, logic, and architecture.",
            "- Grouped terms by topic.",
            "- Built a reference for returning to earlier lessons.",
        ],
    },
}


DID_YOU_KNOW: dict[str, list[str]] = {
    "Balanced Ternary": [
        "Balanced ternary naturally represents negative values inside the digit string.",
        "No separate minus sign is needed for many signed values.",
    ],
    "Why Balanced Ternary is Special": [
        "Balanced ternary has been admired by computer scientists because negation is a simple digit swap.",
        "That elegance is mathematical; hardware still has to solve physical reliability problems.",
    ],
    "Historical Ternary Computers": [
        "Setun was developed at Moscow State University in the late 1950s.",
        "It is widely cited as a real balanced ternary computer.",
    ],
    "Why Ternary Computers Exist": [
        "Setun showed that balanced ternary computing could be implemented in real hardware.",
        "It did not become the dominant path for general-purpose computing.",
    ],
    "Advantages of Ternary Computing": [
        "Three trits provide 27 patterns, while four bits provide 16 and five bits provide 32.",
        "This is a representation advantage, not a complete hardware comparison.",
    ],
    "Signal Levels in Ternary Logic": [
        "A middle logic level must be detected reliably, not merely drawn between low and high.",
        "That engineering requirement is one reason binary remains simpler in many technologies.",
    ],
    "Fun Facts": [
        "Base 3 appears in radix-economy discussions because it is close to e, about 2.718.",
        "This is a theoretical observation, not a guarantee of faster computers.",
    ],
}


MISCONCEPTIONS: dict[str, list[str]] = {
    "Ternary Number System": [
        "Ternary is not a different quantity system. It is a different notation for quantities.",
        "The value 122 in ternary is 17 in decimal, not one hundred twenty-two.",
    ],
    "Balanced Ternary": [
        "Balanced ternary is not ordinary ternary with renamed digits.",
        "Its digit values are -1, 0, and +1, while ordinary ternary uses 0, 1, and 2.",
    ],
    "Bits vs Trits": [
        "More states per digit do not automatically make a computer faster.",
        "Circuit reliability, speed, power, and manufacturing also matter.",
    ],
    "Binary to/from Ternary": [
        "Binary-to-ternary conversion is not done by grouping a fixed number of bits per ternary digit.",
        "That shortcut works for bases like 8 and 16 because they are powers of 2.",
    ],
    "Ternary Addition": [
        "A carry is not always a carry of ten.",
        "In ternary, carrying one to the next place means three of the current place.",
    ],
    "Truth Tables": [
        "A truth table is not just a list of examples.",
        "It must include every possible input combination for the operation being described.",
    ],
    "Universal Gates": [
        "A gate that is universal in binary logic is not automatically universal in every ternary logic system.",
        "The chosen ternary operations must be defined and proved for that system.",
    ],
    "Why Computers Use Binary": [
        "Computers do not use binary because humans find it easiest to read.",
        "They use it because two-state electronics are practical and reliable.",
    ],
    "Advantages of Ternary Computing": [
        "Ternary computers are not automatically faster than binary computers.",
        "Architecture depends on complete systems, not only digit count.",
    ],
    "Future of Ternary Computing": [
        "Research interest does not mean ternary computers are about to replace binary machines.",
        "A new architecture must overcome technical and ecosystem barriers.",
    ],
}


QUICK_REFERENCES: dict[str, list[str]] = {
    "Bits vs Trits": [
        "System    States  Digit  Base",
        "Binary    2       bit    2",
        "Ternary   3       trit   3",
    ],
    "Binary Logic vs Ternary Logic": [
        "Logic type  States  Two-input rows",
        "Binary      2       4",
        "Ternary     3       9",
    ],
    "Decimal Number System": [
        "Place      10^3  10^2  10^1  10^0",
        "Value      1000  100   10    1",
    ],
    "Binary Number System": [
        "Place      2^4  2^3  2^2  2^1  2^0",
        "Value      16   8    4    2    1",
    ],
    "Ternary Number System": [
        "Place      3^4  3^3  3^2  3^1  3^0",
        "Value      81   27   9    3    1",
    ],
    "Balanced Ternary": [
        "Digit      T    0    1",
        "Value     -1    0   +1",
    ],
    "Signal Levels in Ternary Logic": [
        "Symbolic value  Possible meaning",
        "0               Low",
        "1               Middle",
        "2               High",
    ],
}


def _optional_page(title: str, lines: list[str]) -> LessonSection | None:
    """Return a lesson page only when content is available."""
    if not lines:
        return None
    return title, lines


def _course_links(previous_title: str | None, next_title: str | None) -> LessonSection:
    """Return cross references for a lesson."""
    prerequisite = previous_title or "None. This is a starting point for the course."
    next_lesson = next_title or "Course review and hands-on practice in TriCore."
    return (
        "Course Links",
        [
            "Prerequisites",
            f"- {prerequisite}",
            "",
            "Next Lesson",
            f"- {next_lesson}",
        ],
    )


def _systems_perspective(section_title: str) -> LessonSection:
    """Return the binary/ternary framing page for a course section."""
    return "Concept Across Systems", SECTION_PERSPECTIVES[section_title]


def _systems_comparison(section_title: str) -> LessonSection:
    """Return a compact comparison table for a course section."""
    return "Binary and Ternary Comparison", SECTION_COMPARISONS[section_title]


def _review_page(title: str) -> LessonSection:
    """Return review questions for a lesson."""
    return "Review Questions", REVIEW_AND_SUMMARY[title]["review"]


def _summary_page(title: str) -> LessonSection:
    """Return the final summary for a lesson."""
    return "Summary", REVIEW_AND_SUMMARY[title]["summary"]


def _enrich_lesson(
    lesson: Lesson,
    section_title: str,
    previous_title: str | None,
    next_title: str | None,
) -> Lesson:
    """Return a lesson with course-wide educational support pages appended."""
    enriched = deepcopy(lesson)
    title = enriched["title"]
    sections = list(enriched["sections"])

    sections.insert(0, _systems_perspective(section_title))
    sections.insert(1, _systems_comparison(section_title))

    reference = _optional_page("Quick Reference", QUICK_REFERENCES.get(title, []))
    if reference:
        sections.append(reference)

    fact = _optional_page("Did You Know?", DID_YOU_KNOW.get(title, []))
    if fact:
        sections.append(fact)

    misconception = _optional_page(
        "Common Misconception",
        MISCONCEPTIONS.get(title, []),
    )
    if misconception:
        sections.append(misconception)

    sections.append(_course_links(previous_title, next_title))
    sections.append(_review_page(title))
    sections.append(_summary_page(title))
    enriched["sections"] = sections
    return enriched


def enrich_curriculum(sections: list[CurriculumSection]) -> list[CurriculumSection]:
    """Return curriculum sections with enriched lesson structure."""
    lesson_titles = [
        lesson["title"] for section in sections for lesson in section["lessons"]
    ]
    enriched_sections: list[CurriculumSection] = []

    lesson_index = 0
    for section in sections:
        enriched_section = deepcopy(section)
        enriched_lessons: list[Lesson] = []

        for lesson in section["lessons"]:
            previous_title = (
                lesson_titles[lesson_index - 1] if lesson_index > 0 else None
            )
            next_title = (
                lesson_titles[lesson_index + 1]
                if lesson_index + 1 < len(lesson_titles)
                else None
            )
            enriched_lessons.append(
                _enrich_lesson(lesson, section["title"], previous_title, next_title)
            )
            lesson_index += 1

        enriched_section["lessons"] = enriched_lessons
        enriched_sections.append(enriched_section)

    return enriched_sections
