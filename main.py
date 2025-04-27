import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        from cli import main
        main()
    else:
        from gui import start_gui
        start_gui()
