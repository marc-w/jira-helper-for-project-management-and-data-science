"""Main run"""
from lib.setup import Setup


def main() -> None:
    """
    Main loop

    return: None
    """
    # Set up, checks, output, skips if config found to support readiness
    Setup().setup()

if __name__ == "__main__":
    main()
