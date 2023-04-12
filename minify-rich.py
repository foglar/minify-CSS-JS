#! /usr/bin/env python3

# CSS and JS minifier, by foglar
# More information about it on https://www.github.com/foglar/minify-CSS-JS

import sys, os
from rich.console import Console

c = Console()

def main():
    """Main function"""
    c.print("CSS and JS minifier, by foglar", style="bold cyan")
    c.print('More info at: https://www.github.com/foglar/minify-CSS-JS')
    c.print("-------------------")

    while True:
        forced, onefile = cmd_arguments()
        # Check if path to file is provided
        if len(sys.argv) == 2:
            path_to_file = sys.argv[1]
            # Check if path is to a folder or a file
            if os.path.exists(path_to_file):
                if is_folder(path_to_file) == True:
                    try:
                        minify_folder(path_to_file, forced, onefile)
                    except KeyboardInterrupt:
                        c.print("Files are not converted succesfully!", style="bold red")
                        sys.exit()
                else:
                    minify(path_to_file, forced, onefile)
                break
            else:
                c.print("File not found!", style="bold red")
                sys.argv.remove(sys.argv[1])
        # Check if multiple paths to files are provided
        elif len(sys.argv) > 2:
            for i in range(1, len(sys.argv)):
                path_to_file = sys.argv[i]
                if os.path.exists(path_to_file):
                    if is_folder(path_to_file) == True:
                        c.print(f"Folder {os.path.abspath(path_to_file)}")
                        try:
                            minify_folder(path_to_file, forced, onefile)
                        except KeyboardInterrupt:
                            c.print("Files are not converted succesfully!", style="bold red")
                        sys.exit()
                    else:
                        c.print(f"File {os.path.abspath(path_to_file)}")
                        minify(path_to_file, forced, onefile)
                else:
                    c.print(f"File {os.path.abspath(path_to_file)} does not exist", style="bold red")
            c.print("All files minified!", style="bold green")
            break
        # Ask for path to file
        else:
            while True:
                c.print("Please provide a path to a file", style="yellow")
                path_to_file = input("> ")
                if os.path.exists(path_to_file):
                    break
                else:
                    c.print("This file does not exist. Enter valid path.")
                    c.print("")
                    continue
            minify(path_to_file, forced, onefile)

            break


def cmd_arguments():
    """Set up arguments from command line"""
    forced = False
    build_to_one_file = False

    for i in range(len(sys.argv)):
        # Check if forced flag is provided
        if sys.argv[i] == "-s" or sys.argv[i] == "--silent":
            forced = True
        # Check if build flag is provided
        elif sys.argv[i] == "-b" or sys.argv[i] == "--build":
            build_to_one_file = True

        elif sys.argv[i] == "-v" or sys.argv[i] == "--version":
            c.print("1.0.0")
            sys.exit()
        elif sys.argv[i] == "-l" or sys.argv[i] == "--license":
            c.print("MIT License")
            sys.exit()
        elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
            c.print("Minify CSS and JS files to smaller size for better performance")
            print('')
            c.print("Usage: minify.py [bold cyan][FILES][/bold cyan]... [bold cyan][OPTION][/bold cyan]...")
            c.print("[bold cyan]-s, --silent[/bold cyan]\t\tSilently minify files")
            c.print("[bold cyan]-b, --build[/bold cyan]\t\tBuild all files to one file")
            c.print("[bold cyan]-v, --version[/bold cyan]\t\tPrint version")
            c.print("[bold cyan]-l, --license[/bold cyan]\t\tPrint license")

            sys.exit()
        else:
            forced = False
            build_to_one_file = False

    # Remove flags from sys.argv
    try:
        sys.argv.remove("-f")
    except ValueError:
        pass
    try:
        sys.argv.remove("--forced")
    except ValueError:
        pass
    try:
        sys.argv.remove("-b")
    except ValueError:
        pass
    try:
        sys.argv.remove("--build")
    except ValueError:
        pass

    return forced, build_to_one_file


def minify(path, is_forced, is_onefile):
    """Minify file"""
    if path.endswith(".css"):
        css = minify_css(path)
        if is_onefile == True:
            folder = os.path.abspath(path)
            folder = os.path.split(folder)
            if os.path.exists(folder[0] + "/build") == False:
                c.print(folder[0] + "/build")
                try:
                    os.makedirs(folder[0] + "/build")
                except PermissionError:
                    c.print(
                        "Permission denied, please run as administrator or create build folder manually", style="bold red"
                    )
                    sys.exit()
            f = open(folder[0] + "/build/mini.css", "a")
            f.write(css)
            f.close()
        else:
            file_edit(path, is_forced)
    elif path.endswith(".js"):
        js = minify_js(path)
        if is_onefile == True:
            folder = os.path.abspath(path)
            folder = os.path.split(folder)
            if os.path.exists(folder[0] + "/build/mini.css") == False:
                try:
                    os.makedirs(folder[0] + "/build")
                except PermissionError:
                    c.print(
                        "Permission denied, please run as administrator or create build folder manually", style="bold red"
                    )
                    sys.exit()
            f = open(folder[0] + "/build/mini.css", "a")
            f.write(js)
            f.close()
        else:
            file_edit(path, is_forced)
    else:
        c.print("File type not supported", style="bold yellow")

    c.print("-------------------")


def minify_folder(path, is_forced, is_onefile):
    """Minify all files in folder"""
    files = os.listdir(path)
    for file in files:
        if file.endswith(".css"):
            css = minify_css(path + "/" + file)
            c.print(f'File {os.path.abspath(path + "/" + file)}')
            if is_onefile == True:
                folder = os.path.abspath(path)
                folder = os.path.split(folder)
                if os.path.exists(folder[0] + "/build") == False:
                    os.makedirs(folder[0] + "/build")
                f = open(folder[0] + "/build/mini.css", "a")
                f.write(css)
                f.close()
            else:
                file_edit(path + "/" + file, is_forced)
        elif file.endswith(".js"):
            js = minify_js(path + "/" + file)
            if is_onefile == True:
                folder = os.path.dirname(path)
                if os.path.exists(folder + "/build") == False:
                    os.makedirs(folder + "/build")
                f = open(folder + "/build/mini.js", "a")
                f.write(js)
                f.close()
            else:
                file_edit(path + "/" + file, is_forced)
        else:
            c.print("File type not supported", style="bold yellow")
        c.print("-------------------")


def minify_js(path):
    """Minify JS file"""

    with open(path, "r") as f:
        js = f.read()

    # Remove comments
    i = 0
    while i < len(js):

        if js[i - 1] == "/" and js[i] == "/":
            start = i - 1
            for j in range(i, len(js)):
                if js[j] == "\n":
                    end = j
                    js = js.replace(js[start:end], "")
                    i = 0
                    break

        i = i + 1

    js = js.replace("\n", "")
    js = js.replace("\t", "")

    i = 0
    while i < len(js):
        if js[i - 1] == " " and js[i] == " ":
            js = js[: i - 1] + js[i + 1 :]
            i = 0

        i = i + 1

    with open("minified.txt", "w") as f:
        f.write(js)

    size_before = os.path.getsize(path)
    size_after = os.path.getsize("minified.txt")

    space_saved(size_before, size_after)
    return js


def minify_css(path):
    """Minify CSS file"""

    with open(path, "r") as f:
        css = f.read()

    css = css.replace("\n", "")
    css = css.replace("\t", "")

    # Remove comments
    i = 0
    while i < len(css):

        if css[i - 1] == "/" and css[i] == "*":
            start = i - 1
            for j in range(i, len(css)):
                if css[j - 1] == "*" and css[j] == "/":
                    end = j + 1
                    css = css.replace(css[start:end], "")
                    i = 0
                    break

        i = i + 1

    # Remove double spaces
    i = 0
    while i < len(css):
        if css[i - 1] == " " and css[i] == " ":
            css = css[: i - 1] + css[i + 1 :]
            i = 0

        i = i + 1

    with open("minified.txt", "w") as f:
        f.write(css)

    size_before = os.path.getsize(path)
    size_after = os.path.getsize("minified.txt")

    space_saved(size_before, size_after)

    return css


def file_edit(path, confirm_question):
    if confirm_question == False:
        if confirm_dialog() == True:
            os.rename("minified.txt", path)
            c.print(f"File succesfully minified!", style="bold green")
        else:
            c.print("File not minified!", style="bold red")
    else:
        os.rename("minified.txt", path)
        c.print(f"File succesfully minified!", style="bold green")


def confirm_dialog():
    """Confirm action"""
    while True:
        confirm = input("Are you sure you want to continue? (y/n): ")
        if confirm.lower() == "y":
            return True
        elif confirm.lower() == "n":
            return False
        else:
            c.print("Please enter y or n")


def is_folder(path):
    """Check if path is a file or a folder"""
    if os.path.isfile(path) == True:
        return False
    elif os.path.isdir(path) == True:
        return True
    else:
        return None


def space_saved(size_before, size_after):
    c.print(f"[bold blue]File size before:[/bold blue] {size_before} bites")
    c.print(f"[bold blue]File size after:[/bold blue] {size_after} bites")
    c.print("")
    percent_Saved = round((size_before - size_after) / size_before * 100)
    c.print(f"You save up {percent_Saved}[bold blue]%[/bold blue] of size of the file!", style="bold green")

    bits_Saved = size_before - size_after
    c.print(f"File is about {bits_Saved} [bold blue]bits[/bold blue] smaller now! :dart:", style="bold green")

    c.print("")
    return percent_Saved, bits_Saved


if __name__ == "__main__":
    main()
    if os.path.exists("./minified.txt") == True:
        os.remove("./minified.txt")
