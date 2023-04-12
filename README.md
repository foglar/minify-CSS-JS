# Minify CSS/JS

![Czech][czechLangBadge]
![Lines of code](https://img.shields.io/tokei/lines/github/foglar/minify-CSS-JS?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/foglar/minify-CSS-JS?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/foglar/minify-CSS-JS?style=for-the-badge)

Simple script to minify CSS and JS files.

[![CodeFactor](https://www.codefactor.io/repository/github/foglar/minify-css-js/badge)](https://www.codefactor.io/repository/github/foglar/minify-css-js)
![GitHub top language](https://img.shields.io/github/languages/top/foglar/minify-CSS-JS)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/foglar/minify-CSS-JS)
![GitHub Repo stars](https://img.shields.io/github/stars/foglar/minify-CSS-JS?style=social)

## Usage

There are 2 files in the repository, **minify.py** and **minify-rich.py**. The first one is the lighter version of my script (don't have to install any libraries), the second one is the same script, but with [rich][rich] library.
You can add alias in the bashrc file to run the script from anywhere. With opening it and adding **alias minify="python3 /path/to/minify.py"** you can run the script with **minify** command.

### Install

```bash
git clone https://github.com/foglar/minify-CSS-JS.git
cd minify-CSS-JS
pip3 install rich.console # if you want to use rich version
```

### Run

```bash
python3 minify.py [files/folders...] [options...]
```

### Options

Before options you should print files or folders, which you want to minify.
It cannot scan folders recursively, so you should print all files and folders.
If you select build mode, it will minify all files in the one file into the build folder (if you pick js and css files it sort them into **mini.css** and **mini.js**).

```text
[-s] [--silent] : Silent mode - don't show any messages and questions

[-b] [--build] : Build mode - minify all files in the one file

[-h] [--help] : Show help message

[-v] [--version] : Show version

[-l] [--license] : Show license
```

## License

Minify CSS/JS is licensed under the MIT License - see the LICENSE file for details

[czechLangBadge]: https://img.shields.io/badge/MADE%20IN-CZECH-red?style=for-the-badge
[rich]: https://github.com/Textualize/rich
