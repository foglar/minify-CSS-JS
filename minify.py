#! /usr/bin/env python3

# CSS and JS minifier

import sys, os
import pyinputplus as pyip


def main():
    """Main function"""
    print("CSS and JS minifier")
    print("-------------------")

    while True:
        forced, onefile = cmd_arguments()
        # Check if path to file is provided
        if len(sys.argv) == 2:
            path_to_file = sys.argv[1]
            # Check if path is to a folder or a file
            if os.path.exists(path_to_file):
                if is_folder(path_to_file) == True:
                    minify_folder(path_to_file, forced, onefile)
                else:
                    minify(path_to_file, forced, onefile)
                break
        # Check if multiple paths to files are provided
        elif len(sys.argv) > 2:
            for i in range(1, len(sys.argv)):
                path_to_file = sys.argv[i]
                if os.path.exists(path_to_file):
                    if is_folder(path_to_file) == True:
                        print(f"Folder {os.path.abspath(path_to_file)}")
                        minify_folder(path_to_file, forced, onefile)
                    else:
                        print(f"File {os.path.abspath(path_to_file)}")
                        minify(path_to_file, forced, onefile)
                else:
                    print(f"File {os.path.abspath(path_to_file)} does not exist")
            print("All files minified!")
            break
        # Ask for path to file
        else:
            print("Please provide a path to a file")
            path_to_file = pyip.inputFilepath("Path: ", mustExist=True)
            minify(path_to_file, forced, onefile)
            break


def cmd_arguments():
    forced = False
    build_to_one_file = False

    for i in range(len(sys.argv)):
        # Check if forced flag is provided
        if sys.argv[i] == "-f" or sys.argv[i] == "--forced":
            forced = True
        # Check if build flag is provided
        elif sys.argv[i] == "-b" or sys.argv[i] == "--build":
            build_to_one_file = True

        elif sys.argv[i] == "-v" or sys.argv[i] == "--version":
            print("1.0.0")
            sys.exit()
        elif sys.argv[i] == "-l" or sys.argv[i] == "--license":
            print("MIT License")
            sys.exit()
        elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print("Usage: minify.py [FILES]... [OPTION]...")
            print("-f, --forced\t\tForce minify files")
            print("-b, --build\t\tBuild all files to one file")
            print("-v, --version\t\tPrint version")
            print("-l, --license\t\tPrint license")

            print("Minify CSS and JS files to smaller size for better performance")
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
                print(folder[0] + "/build")
                try:
                    os.makedirs(folder[0] + "/build")
                except PermissionError:
                    print("Permission denied, please run as administrator or create build folder manually")
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
                    print("Permission denied, please run as administrator or create build folder manually")
                    sys.exit()
            f = open(folder[0] + "/build/mini.css", "a")
            f.write(js)
            f.close()
        else:
            file_edit(path, is_forced)
    else:
        print("File type not supported")

    print("-------------------")


def minify_folder(path, is_forced, is_onefile):
    """Minify all files in folder"""
    files = os.listdir(path)
    for file in files:
        if file.endswith(".css"):
            css = minify_css(path + "/" + file)
            print(f'File {os.path.abspath(path + "/" + file)}')
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
            print("File type not supported")
        print("-------------------")

def minify_js(path):
    """Minify JS file"""
    print(f"File size before: {os.path.getsize(path)} bites")

    with open(path, "r") as f:
        js = f.read()

    js = js.replace("\n", "")
    js = js.replace("\t", "")

    with open("minified.txt", "w") as f:
        f.write(js)

    print(f'File size after: {os.path.getsize("minified.txt")} bites')
    return js


def minify_css(path):
    """Minify CSS file"""

    size_before = os.path.getsize(path)
    print(f"File size before: {size_before} bites")

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

    size_after = os.path.getsize("minified.txt")
    print(f'File size after: {size_after} bites')

    percent = round((size_before - size_after) / size_before * 100)
    print(f"Minified by {percent}%")
    
    return css


def file_edit(path, confirm_question):
    if confirm_question == False:
        if confirm_dialog() == True:
            os.rename("minified.txt", path)
            print(f"File succesfully minified!")
        else:
            print("File not minified!")
    else:
        os.rename("minified.txt", path)
        print(f"File succesfully minified!")

def confirm_dialog():
    """Confirm action"""
    while True:
        confirm = input("Are you sure you want to continue? (y/n): ")
        if confirm.lower() == "y":
            return True
        elif confirm.lower() == "n":
            return False
        else:
            print("Please enter y or n")

def is_folder(path):
    """Check if path is a file or a folder"""
    if os.path.isfile(path) == True:
        return False
    elif os.path.isdir(path) == True:
        return True
    else:
        return None

if __name__ == "__main__":
    main()
    if os.path.exists('./minified.txt') == True:
        os.remove("./minified.txt")
