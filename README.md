# Stump Block
Convert C# code to Block Diagram

# How it works
A .cs file gets passed as input to the program, then it gets parsed and represented as a tree of flow-chart blocks, which then is getting rendered

# Supported language constructions
1. Variables
2. Methods
3. If-statements
4. While loops
5. Do-while loops
6. Input through `Console.ReadLine()`
7. Output through `Console.WriteLine()`

# Supported blocks for rendering
1. Box
2. Subroutine
3. Input / Output
4. Branching

# Installation
1. Clone the repo `git clone <url> --recursive`
2. Install all the dependencies by running command `pip install -r requirements.txt`
3. Install c/c++ compiler (gcc on unix, or msvc for windows)
4. Run main.py script

# How to use
## Input blocks
```c#
//input-start
type x = type.Parse(Console.ReadLine())
//input-end
```
Any variable definition inside `//input-start` `input-end` blocks will be recognized as input
## Output blocks
```c#
Console.WriteLine("string")
```
To denote output you have to use `Console.WriteLine()`. If argument of this function is a string literal (exception is interpolated string), then its quotes will be stripped, otherwise output will be as is

## Methods
Declarations of another methods will be detected automatically and rendered as a separate SVG file.

## Others
Works as-is

**Note** The program will generate file in **SVG** format. Use other tools to convert it to your preferred format.



# TODO
## For language constructions
1. Switch-statement as type of branching [-]
2. Iterator loops [+]
3. For-each loops [+]

## For rendering
1. Block resizing to contain labels [+]
2. Add support for loops [+]
3. Add support for iterator loops [+]
4. Add offset for input anchor for data block [-]
5. Add formatting settings [-]

## For client
1. Add pycairo to render to png [-]
