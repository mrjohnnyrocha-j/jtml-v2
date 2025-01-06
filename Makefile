# Makefile
CXX = g++
CXXFLAGS = -std=c++17 -Wall -O3
INCLUDES = -I/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.2/include/antlr4-runtime \
           -I./JTMLElementParser \
           -I$(shell python3 -m pybind11 --includes) \
           -I. \
           $(shell python3-config --includes | sed 's/-I//g')

LIBS = -L/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.2/lib -lantlr4-runtime

all: libjtmlparser.dylib

libjtmlparser.dylib: JTMLVisitor.o jtml_parser_bindings.o JTMLElementParser/*.o
	$(CXX) $(CXXFLAGS) -shared -fPIC JTMLVisitor.o jtml_parser_bindings.o JTMLElementParser/*.o $(LIBS) -o libjtmlparser.dylib

JTMLVisitor.o: JTMLVisitor.cpp JTMLVisitor.h ASTNodes.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c JTMLVisitor.cpp -o JTMLVisitor.o

jtml_parser_bindings.o: jtml_parser_bindings.cpp JTMLVisitor.h ASTNodes.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c jtml_parser_bindings.cpp -o jtml_parser_bindings.o

JTMLElementParser/JTMLElementParser.o: JTMLElementParser/JTMLElementParser.cpp JTMLElementParser/JTMLElementParser.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c JTMLElementParser/JTMLElementParser.cpp -o JTMLElementParser/JTMLElementParser.o

# Add similar rules for other JTMLElementParser source files if needed

clean:
	rm -rf libjtmlparser.dylib build/ jtmlparser.so *.o JTMLElementParser/*.o
