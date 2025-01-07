#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstring>
#include <cstdlib>

// All your jtml headers:
#include "jtml_lexer.cpp"
#include "jtml_parser.cpp"
#include "jtml_interpreter.cpp"
#include "jtml_transpiler.cpp"

// For the HTTP server:
#include "httplib.h"

static void usage() {
    std::cout << "Usage:\n"
              << "  jtml interpret <input.jtml>\n"
              << "  jtml transpile <input.jtml> -o <output.html>\n"
              << "  jtml serve <input.jtml> [--port <num>]\n";
    std::exit(1);
}

std::string readFile(const std::string &path) {
    std::ifstream ifs(path);
    if (!ifs.is_open()) {
        throw std::runtime_error("Cannot open file: " + path);
    }
    std::ostringstream oss;
    oss << ifs.rdbuf();
    return oss.str();
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        usage();
    }

    std::string command   = argv[1];  // "interpret", "transpile", or "serve"
    std::string inputFile = argv[2];

    std::string outputFile;
    int port = 8080; // default port

    // Parse extra args
    for (int i = 3; i < argc; ++i) {
        if ((std::strcmp(argv[i], "-o") == 0 || std::strcmp(argv[i], "--out") == 0) && i + 1 < argc) {
            outputFile = argv[++i];
        } else if (std::strcmp(argv[i], "--port") == 0 && i + 1 < argc) {
            port = std::atoi(argv[++i]);
        } else {
            // unrecognized argument
        }
    }

    try {
        // 1) Read the .jtml file
        std::string inputText = readFile(inputFile);

        // 2) Lex + Parse
        Lexer lexer(inputText);
        auto tokens = lexer.tokenize();

        const auto& errors = lexer.getErrors();
        if (!errors.empty()) {
            for (const auto& error : errors) {
            std::cerr << error << std::endl;
            }
        } else {
            std::cout << "Lexing completed successfully!" << std::endl;
        }

        Parser parser(std::move(tokens));
        auto root = parser.parseJtmlElement();

        if (command == "interpret") {
            // Just interpret server-side
            Interpreter interp;
            interp.interpret(*root);

        } else if (command == "transpile") {
            // Generate HTML
            JtmlTranspiler transpiler;
            std::string html = transpiler.transpileHTML(*root);

            if (!outputFile.empty()) {
                std::ofstream ofs(outputFile);
                if (!ofs.is_open()) {
                    throw std::runtime_error("Cannot open output file: " + outputFile);
                }
                ofs << html;
                ofs.close();
                std::cout << "Wrote transpiled HTML to " << outputFile << "\n";
            } else {
                std::cout << html << "\n";
            }

        } else if (command == "serve") {
            // Generate HTML
            JtmlTranspiler transpiler;
            std::string html = transpiler.transpileHTML(*root);

            // Start http server
            httplib::Server svr;
            svr.Get("/", [html](const httplib::Request &, httplib::Response &res) {
                res.set_content(html, "text/html");
            });

            std::cout << "Serving jtml on http://localhost:" << port << "\n";
            svr.listen("0.0.0.0", port);

        } else {
            usage();
        }

    } catch (const std::exception &e) {
        std::cerr << "ERROR: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
