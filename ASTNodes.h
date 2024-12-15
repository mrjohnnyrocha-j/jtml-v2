// ASTNodes.h
#pragma once
#include <string>
#include <vector>
#include <map>
#include <memory>

class ASTNode {
public:
    virtual std::map<std::string, py::object> to_dict() = 0;
};

class JTMLElementNode : public ASTNode {
public:
    std::string tag_name;
    std::map<std::string, std::string> attributes;
    std::vector<std::shared_ptr<ASTNode>> content;

    JTMLElementNode(const std::string& tag, const std::map<std::string, std::string>& attrs, const std::vector<std::shared_ptr<ASTNode>>& cont)
        : tag_name(tag), attributes(attrs), content(cont) {}

    std::map<std::string, py::object> to_dict() override {
        std::map<std::string, py::object> dict;
        dict["type"] = "JTMLElement";
        dict["tag_name"] = tag_name;
        dict["attributes"] = attributes;
        std::vector<py::object> content_list;
        for (auto& stmt : content) {
            content_list.push_back(stmt->to_dict());
        }
        dict["content"] = content_list;
        return dict;
    }
};

// Similarly define other AST nodes with to_dict methods
