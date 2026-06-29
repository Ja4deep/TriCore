"""Computer architecture lessons."""

from __future__ import annotations

from learn_center.types import CurriculumSection, page

SECTION: CurriculumSection = {
    "menu_title": "Computer Architecture",
    "title": "Computer Architecture",
    "lessons": [
        {
            "menu_title": "Why Computers Use Binary",
            "title": "Why Computers Use Binary",
            "question": "Why did binary become the standard for digital computers?",
            "sections": [
                page(
                    "Hardware Reason",
                    """
                    Binary fits electronic switching well. A transistor can be
                    used so that one range of voltages means 0 and another range
                    means 1.

                    Two states give circuits wide room for electrical noise
                    before a value is misread.
                    """,
                ),
                page(
                    "Engineering Reason",
                    """
                    Computer design is not decided by notation alone. Engineers
                    need reliable gates, dense memory, fast switching, low power
                    use, affordable manufacturing, and predictable testing.

                    Binary technology became excellent at all of these through
                    decades of research and industry investment.
                    """,
                ),
                page(
                    "Ecosystem Reason",
                    """
                    Modern computing has a huge binary ecosystem: processors,
                    memory chips, compilers, operating systems, file formats,
                    communication standards, and testing tools.

                    Replacing that ecosystem would be expensive even if an
                    alternative had attractive mathematical properties.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Binary is dominant because it is reliable, manufacturable,
                    and deeply standardized.

                    It is not the only possible computing model, but it is the
                    practical foundation of most modern digital hardware.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Why Ternary Computers Exist",
            "title": "Why Ternary Computers Exist",
            "question": "If binary is dominant, why build ternary machines at all?",
            "sections": [
                page(
                    "Mathematical Interest",
                    """
                    Ternary is attractive because each digit has three states.
                    This can make representations shorter than binary for some
                    values.

                    Balanced ternary is especially interesting because its digit
                    values are symmetric around zero.
                    """,
                ),
                page(
                    "Research Motivation",
                    """
                    Engineers and computer scientists explore alternatives to
                    learn what tradeoffs are possible. Ternary computing tests
                    ideas about information density, arithmetic design, logic
                    systems, and hardware representation.
                    """,
                ),
                page(
                    "Historical Reality",
                    """
                    Ternary computers have been built. The best-known example is
                    Setun, developed at Moscow State University in the late
                    1950s. It used balanced ternary logic.

                    Setun shows that ternary computing is a real part of
                    computing history, not just a classroom puzzle.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ternary computers exist because the idea has real theoretical
                    and engineering interest.

                    Binary dominance does not erase the value of studying other
                    architectures.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Advantages of Ternary Computing",
            "title": "Advantages of Ternary Computing",
            "question": "What makes ternary computing attractive?",
            "sections": [
                page(
                    "Information Density",
                    """
                    A trit has three possible values, while a bit has two. This
                    means n trits can represent 3^n patterns.

                    For example:

                    3 trits represent 27 patterns.
                    4 bits represent 16 patterns.
                    5 bits represent 32 patterns.
                    """,
                ),
                page(
                    "Balanced Arithmetic",
                    """
                    Balanced ternary can represent negative and positive values
                    with the same digit positions. Negation is simple: swap T
                    and 1.

                    This symmetry can make some arithmetic ideas cleaner on
                    paper and in certain theoretical designs.
                    """,
                ),
                page(
                    "Fewer Digit Positions",
                    """
                    Because base 3 grows faster than base 2, some values need
                    fewer ternary digits than binary digits.

                    Decimal 17:

                    Binary  : 10001
                    Ternary : 122
                    """,
                ),
                page(
                    "Careful Conclusion",
                    """
                    These advantages are real at the representation level. They
                    do not automatically prove that ternary hardware is better
                    overall.

                    A full computer must also win on reliability, speed, power,
                    cost, memory, tooling, and compatibility.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Challenges of Ternary Hardware",
            "title": "Challenges of Ternary Hardware",
            "question": "Why is ternary hardware difficult to build at scale?",
            "sections": [
                page(
                    "Three Stable States",
                    """
                    A ternary device must store and distinguish three states.
                    That sounds simple, but physical devices are affected by
                    noise, temperature, manufacturing variation, and aging.

                    The middle state must be just as dependable as the low and
                    high states.
                    """,
                ),
                page(
                    "Noise Margin",
                    """
                    If the same voltage range is divided into three states
                    instead of two, each state can have less separation from its
                    neighbors.

                    Less separation can make high-speed reliable detection more
                    difficult.
                    """,
                ),
                page(
                    "Tooling and Manufacturing",
                    """
                    Modern chip design tools, testing methods, memory designs,
                    and fabrication processes are heavily optimized for binary
                    CMOS technology.

                    A ternary system would need not only working gates, but a
                    complete practical design and manufacturing ecosystem.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    Ternary hardware is challenging because real machines are
                    physical systems, not just mathematical notation.

                    The hard questions are reliability, speed, energy, cost, and
                    compatibility with existing technology.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Historical Ternary Computers",
            "title": "Historical Ternary Computers",
            "question": "What real ternary computers have existed?",
            "sections": [
                page(
                    "Setun",
                    """
                    Setun is the most famous historical ternary computer. It was
                    developed at Moscow State University in the late 1950s under
                    the direction of Nikolay Brusentsov.

                    It used balanced ternary logic, which made it an important
                    example of a real three-valued computing machine.
                    """,
                ),
                page(
                    "Why It Matters",
                    """
                    Setun matters because it proves that ternary computing has
                    been engineered into working hardware. It was not merely a
                    mathematical note or a science fiction idea.

                    Its existence also reminds us that computing history
                    includes paths that did not become the mainstream standard.
                    """,
                ),
                page(
                    "Historical Context",
                    """
                    Early computing history included many competing approaches:
                    relay machines, vacuum tube machines, transistor machines,
                    analog computers, binary digital computers, and experimental
                    non-binary designs.

                    Binary became dominant, but the exploration of alternatives
                    helped shape computer science.
                    """,
                ),
                page(
                    "Careful Claims",
                    """
                    It is accurate to say that Setun was a real balanced ternary
                    computer from the Soviet era.

                    It is not accurate to claim that ternary computers replaced
                    binary computers, or that modern general-purpose computers
                    are secretly ternary. They are overwhelmingly binary.
                    """,
                ),
            ],
        },
        {
            "menu_title": "Future of Ternary Computing",
            "title": "Future of Ternary Computing",
            "question": "Could ternary computing become important again?",
            "sections": [
                page(
                    "Possibility",
                    """
                    Ternary computing remains an active idea in research and
                    education. Multi-valued logic, memory technologies, and
                    alternative device physics can make non-binary approaches
                    worth studying.
                    """,
                ),
                page(
                    "What Would Need to Change",
                    """
                    For ternary computing to become broadly practical, engineers
                    would need reliable three-state devices, efficient ternary
                    gates, dense memory, useful design tools, and strong reasons
                    to move away from binary compatibility.
                    """,
                ),
                page(
                    "Likely Role",
                    """
                    Ternary ideas may continue to be valuable in specialized
                    research, education, and theoretical computer science even
                    if everyday laptops and phones remain binary.

                    Studying ternary sharpens your understanding of why binary
                    works and what alternatives require.
                    """,
                ),
                page(
                    "Key Takeaways",
                    """
                    The future is not settled by elegance alone.

                    Ternary computing would need practical advantages that
                    outweigh the enormous success and infrastructure of binary
                    computing.
                    """,
                ),
            ],
        },
    ],
}
