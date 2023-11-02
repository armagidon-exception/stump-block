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

# How to use
1. To denote that following variables are input variables you have to wrap them in `//input-start` `//input-end` comments (Case and punctuation matters)
2. To denote output you have to use `Console.WriteLine()`. If argument of this function is a string literal (exception is interpolated string), then its quotes will be stripped, otherwise output will be as is
3. Every other supported block is rendered normally
4. Run the program passing input file as first argument and output file as second.
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
