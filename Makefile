all: libjtmlparser.dylib jtmlparser.so

libjtmlparser.dylib: JTMLVisitor.cpp JTMLElementParser/*.cpp
	g++ -std=c++17 \
	    -I/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.2/include/antlr4-runtime \
	    -I./JTMLElementParser \
	    -L/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.2/lib \
	    -lantlr4-runtime \
	    -shared -fPIC \
	    JTMLVisitor.cpp JTMLElementParser/*.cpp \
	    -o libjtmlparser.dylib

jtmlparser.so: jtml_parser_bindings.cpp libjtmlparser.dylib
	python3 setup.py build_ext --inplace

clean:
	rm -f libjtmlparser.dylib jtmlparser.so build/
