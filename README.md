# Simple interpreter

This is my first foray into coding an interpreter.  
I'm doing it using [this series](https://ruslanspivak.com/lsbasi-part1/) of articles by Ruslan Spivak.  
This repository is just to follow along and keep track of what I try.  

## Lexicon
 - **Token**: single component of a program, it has a type and a value. For example in the expression `2 * 5`, `2` is a token of type `Integer` and of value `2`. To be able to interpret a written program, the interpreter must be able to break it up into tokens. 
 - **lexical analyzer (lexer)**: it is a part of the interpreter that breaks the written instruction into tokens that can then be interpreted and form operations that can be executed. This part can also be called the **tokenizer**, or **scanner**.
 - **lexeme**: it is a string of characters in the written code that form the token. For example, `325` is the lexeme that will form an Integer token.
 - **parser**: this part takes a stream of tokens and parses it. This means that it decodes the stream of tokens and transforms it to an operation to execute. For example the parser will recognize the pattern `INTEGER -> TIMES -> INTEGER` in the token stream and return the multiplication of the two token values. 

