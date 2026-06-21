from converters.binary_vs_ternary import (
    display_header as display_binary_vs_ternary_header,
    display_results as display_binary_vs_ternary_results,
    explain_comparison,
)
from converters.balanced_ternary import main as run_balanced_ternary_module
from converters.decimal_to_ternary import (
    display_header as display_decimal_to_ternary_header,
    display_results as display_decimal_to_ternary_results,
    explain_conversion as explain_decimal_to_ternary,
    get_decimal_input,
)
from converters.ternary_to_decimal import (
    display_header as display_ternary_to_decimal_header,
    display_results as display_ternary_to_decimal_results,
    explain_conversion as explain_ternary_to_decimal,
    get_ternary_input,
)


PROJECT_NAME = "TriCore"


def show_header() -> None:
    """Display the project title."""
    print("=" * 40)
    print(f"{PROJECT_NAME:^40}")
    print("Ternary Computing Learning Project".center(40))
    print("=" * 40)


def show_menu() -> None:
    """Display the main menu options."""
    print("\nChoose a topic:")
    print("1. Decimal to Ordinary Ternary")
    print("2. Ternary to Decimal")
    print("3. Binary vs Ternary Comparison")
    print("4. Balanced Ternary")
    print("5. Exit")


def show_coming_soon(topic: str) -> None:
    """Display a temporary message for features not connected yet."""
    print(f"\n{topic} will be added here soon.")
    print("For now, build and test each converter step by step.")


def get_menu_choice() -> str:
    """Read the user's menu choice."""
    try:
        return input("\nEnter your choice: ").strip()
    except EOFError:
        return "5"


def get_decimal_number() -> int:
    """Read a decimal integer from the user with validation."""
    return get_decimal_input()


def run_decimal_to_ternary() -> None:
    """Run the educational decimal-to-ordinary-ternary lesson."""
    display_decimal_to_ternary_header()
    explain_decimal_to_ternary()
    number = get_decimal_number()
    display_decimal_to_ternary_results(number)


def run_ternary_to_decimal() -> None:
    """Run the educational ordinary-ternary-to-decimal lesson."""
    display_ternary_to_decimal_header()
    explain_ternary_to_decimal()
    ternary = get_ternary_input()
    display_ternary_to_decimal_results(ternary)


def run_binary_vs_ternary() -> None:
    """Run the educational binary-vs-ternary comparison lesson."""
    display_binary_vs_ternary_header()
    explain_comparison()
    number = get_decimal_number()
    display_binary_vs_ternary_results(number)


def run_balanced_ternary() -> None:
    """Run the educational balanced ternary module."""
    run_balanced_ternary_module()


def main() -> None:
    """Run the TriCore starting UI."""
    show_header()

    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == "5":
            print("\nExiting TriCore.")
            break

        if choice == "1":
            run_decimal_to_ternary()
        elif choice == "2":
            run_ternary_to_decimal()
        elif choice == "3":
            run_binary_vs_ternary()
        elif choice == "4":
            run_balanced_ternary()
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
