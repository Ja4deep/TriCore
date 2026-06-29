from learn_center.curriculum import CURRICULUM


def test_learning_center_curriculum_shape_matches_course_outline() -> None:
    assert [section["menu_title"] for section in CURRICULUM] == [
        "Foundations of Number Systems",
        "Number Representation",
        "Number System Conversion",
        "Ternary Arithmetic",
        "Digital Logic",
        "Logic Circuit Simulator",
        "Computer Architecture",
        "Extras",
    ]
    assert [len(section["lessons"]) for section in CURRICULUM] == [
        6,
        4,
        5,
        5,
        6,
        6,
        6,
        3,
    ]


def test_every_learning_center_lesson_has_course_features() -> None:
    for section in CURRICULUM:
        for lesson in section["lessons"]:
            headings = [heading for heading, _lines in lesson["sections"]]

            assert headings[0] == "Concept Across Systems"
            assert headings[1] == "Binary and Ternary Comparison"
            assert headings[-3:] == [
                "Course Links",
                "Review Questions",
                "Summary",
            ]

            review = lesson["sections"][-2][1]
            summary = lesson["sections"][-1][1]
            systems_page = lesson["sections"][0][1]
            comparison_page = lesson["sections"][1][1]

            assert "General concept" in systems_page
            assert "Binary implementation" in systems_page
            assert "Ternary implementation" in systems_page
            assert "TriCore connection" in systems_page
            assert any("Binary" in line for line in comparison_page)
            assert any("Ternary" in line for line in comparison_page)
            assert 2 <= len(review) <= 5
            assert all(line[0].isdigit() for line in review)
            assert 2 <= len(summary) <= 5
            assert all(line.startswith("- ") for line in summary)
