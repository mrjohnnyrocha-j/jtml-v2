#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <memory>
#include <chrono>
#include <iomanip>
#include <ctime>
#include <cstdio>
#include <cstdlib>

// jtml engine
#include "jtml_lexer.cpp"
#include "jtml_parser.cpp"
#include "jtml_interpreter.cpp"
#include "jtml_transpiler.cpp"

/**
 * A test input can be either inline text or a file reference.
 * 'shouldSucceed' indicates expected parse success/failure.
 */
struct TestCase {
    std::string name;          // name of the test (for reporting)
    std::string input;         // jtml code or file path
    bool isFile;               // true => 'input' is a file path
    bool shouldSucceed;
};

/// Read file content into a string
static std::string readFile(const std::string &path) {
    std::ifstream ifs(path);
    if (!ifs.is_open()) {
        throw std::runtime_error("Cannot open file: " + path);
    }
    std::ostringstream oss;
    oss << ifs.rdbuf();
    return oss.str();
}

/**
 * Run a single test case:
 *  - If isFile is true, 'input' is a path -> read from file
 *  - Otherwise, 'input' is the raw jtml code
 */
bool runTest(const TestCase &tc) {
    std::cout << "\n==============================\n";
    std::cout << "[TEST]: " << tc.name << "\n";

    // 1) Gather jtml code
    std::string jtmlCode;
    try {
        if (tc.isFile) {
            jtmlCode = readFile(tc.input);
        } else {
            jtmlCode = tc.input;
        }
    } catch (const std::exception &ex) {
        // If we can't read file but expected success, that’s a failure.
        if (tc.shouldSucceed) {
            std::cout << "FAIL: Unable to read file: " << tc.input
                      << " => " << ex.what() << "\n";
            return false;
        } else {
            // Possibly we expected a fail, so let's consider it pass
            std::cout << "PASS: File read failed as expected. " << ex.what() << "\n";
            return true;
        }
    }

    // 2) Attempt to parse, interpret, transpile
    try {
        Lexer lexer(jtmlCode);
        auto tokens = lexer.tokenize();
        Parser parser(std::move(tokens));
        auto root = parser.parseJtmlElement();

        // If parse succeeded but we expected a fail:
        if (!tc.shouldSucceed) {
            std::cout << "FAIL: Expected parse to fail, but it succeeded.\n";
            return false;
        }

        // If parse is successful, interpret & transpile
        Interpreter interp;
        interp.interpret(*root);

        // If your transpiler needs a symbol table, pass it. 
        // For simplicity, assume a single-arg version:
        JtmlTranspiler transpiler;
        std::string html = transpiler.transpileHTML(*root);

        std::cout << "PASS: " << tc.name << " => jtml parsed & transpiled successfully.\n";
        return true;

    } catch (const std::exception &ex) {
        // If we expected success but got an error
        if (tc.shouldSucceed) {
            std::cout << "FAIL: Unexpected error in " << tc.name << ": " << ex.what() << "\n";
            return false;
        } else {
            // We expected fail, so parse error => pass
            std::cout << "PASS: " << tc.name << " failed as expected. Error: " << ex.what() << "\n";
            return true;
        }
    }
}

/**
 * Generate a minimal HTML report from the results of running each test case.
 */
void generateHtmlReport(const std::vector<TestCase>& tests,
                        const std::vector<bool>& results,
                        const std::string& outPath) {
    std::ofstream ofs(outPath);
    if (!ofs.is_open()) {
        std::cerr << "Cannot open HTML report file: " << outPath << "\n";
        return;
    }

    // current time for the report
    auto now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    ofs << "<html><head><title>jtml Test Report</title></head><body>\n";
    ofs << "<h1>jtml Engine Test Report</h1>\n";
    ofs << "<p>Generated on: " << std::put_time(std::localtime(&now), "%c %Z") << "</p>\n";
    ofs << "<table border='1' cellspacing='0' cellpadding='5'>\n";
    ofs << "<tr><th>Test Name</th><th>Expected</th><th>Result</th></tr>\n";

    for (size_t i = 0; i < tests.size(); i++) {
        const auto &tc = tests[i];
        bool pass = results[i];
        std::string color = pass ? "#cfc" : "#fcc";
        ofs << "<tr style='background:" << color << "'>\n"
            << "<td>" << tc.name << "</td>"
            << "<td>" << (tc.shouldSucceed ? "Success" : "Fail") << "</td>"
            << "<td>" << (pass ? "Pass" : "Fail") << "</td>\n"
            << "</tr>\n";
    }
    ofs << "</table></body></html>\n";
    ofs.close();

    std::cout << "Generated test report: " << outPath << "\n";
}

/**
 * main for test suite
 */
int main() {
    // Hard-coded tests, some inline, some from files:
    std::vector<TestCase> tests = {
        // 1) Minimal inline
        { "MinimalInline", "#hello \\#hello", false /*isFile*/, true },

        // 2) Attributes only
        { "AttributesInline", "#myTag class:\"container\",style:\"color:red;\"\\\\ \\#myTag", false, true },

        // 3) show statement
        { "ShowInline", "#myTag show \"Hello <World>!\"\\\\ \\#myTag", false, true },

        // 4) multiple statements
        { "MultiStatementsInline",
          "#myTag style:\"background:blue;\",onclick:\"alert('Clicked!')\"\\\\ "
          "show \"Testing\"\\\\ "
          "define x=\"someValue\"\\\\ "
          "\\#myTag",
          false, true
        },

        // 5) nested
        { "NestedInline",
          "#outer show \"Outer content\"\\\\ "
          "#h1 style:\"font-size:20px\" show \"Title\"\\\\ \\#h1 "
          "\\#outer",
          false, true
        },

        // 6) mismatch => fail
        { "MismatchedInline", "#mismatch \\#nope", false, false },

        // 7) missing => fail
        { "MissingInline", "#unclosed show \"No close\"\\\\ ", false, false },

        // 8) A file-based test (assuming tests/attributes_only.jtml exists)
        { "FileAttributesTest", "tests/attributes_only.jtml", true /*isFile*/, true },

        // 9) A file that we expect to fail?
        { "FileFailTest", "tests/mismatched_tags.jtml", true, false },
    };

    std::vector<bool> results(tests.size(), false);
    bool allPassed = true;

    for (size_t i = 0; i < tests.size(); ++i) {
        results[i] = runTest(tests[i]);
        if (!results[i]) {
            allPassed = false;
            std::cout << "[Test " << tests[i].name << " FAILED]\n";
        } else {
            std::cout << "[Test " << tests[i].name << " PASSED]\n";
        }
    }

    std::cout << "\n================================\n";
    if (allPassed) {
        std::cout << "ALL TESTS PASSED.\n";
    } else {
        std::cout << "SOME TESTS FAILED.\n";
    }

    // Optionally, produce an HTML test report
    generateHtmlReport(tests, results, "jtml_test_report.html");

    return allPassed ? 0 : 1;
}
