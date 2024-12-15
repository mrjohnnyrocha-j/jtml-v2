// JTMLElement.g4
grammar JTMLElement;

options {
  language = Cpp;
}

jtmlElement
    : HASH IDENTIFIER attributes? BACKSLASH content? HASH IDENTIFIER?
    ;

attributes
    : IDENTIFIER COLON STRING_LITERAL (COMMA IDENTIFIER COLON STRING_LITERAL)*
    ;

content
    : statement BACKSLASH*
    ;

statement
    : showStatement
    | defineStatement
    | // ... other statements
    ;

showStatement
    : SHOW STRING_LITERAL
    ;

defineStatement
    : DEFINE IDENTIFIER EQUALS expression
    ;

expression
    : IDENTIFIER
    | NUMBER_LITERAL
    | STRING_LITERAL
    | expression PLUS expression
    | expression MINUS expression
    | // ... other expressions
    ;

HASH          : '#';
COLON         : ':';
COMMA         : ',';
BACKSLASH     : '\\\\';
EQUALS        : '=';
PLUS          : '+';
MINUS         : '-';
SHOW          : 'show';
DEFINE        : 'define';
IDENTIFIER    : [a-zA-Z_][a-zA-Z0-9_]*;
STRING_LITERAL : '"' (~["\\] | '\\' .)* '"';
NUMBER_LITERAL : [0-9]+ ('.' [0-9]+)?;
WS            : [ \t\r\n]+ -> skip;
