class Summary:
    def __init__(self, failed, checker_results):
        self.failed = failed
        self.checker_results = checker_results
    
    def markdown(self):
        markdown = []
        markdown.append("# Template Checker Findings 🕵️‍♀️")
        if self.failed:
            markdown.append("❌ some errors were found linting your templates")
        else:
            markdown.append("✅ no linting errors were found 🥳")
        markdown.append("## Linting Results")
        for checker_result in self.checker_results:
            markdown.append(f"### {checker_result.path}")
            for result in checker_result.linter_results:
                if result.rule.severity == "error":
                    markdown.append(f" * ❌ line {result.linenumber} __{result.rule.shortdesc}__")
                    markdown.append(f"   * {result.message}")
                elif result.rule.severity == "warning":
                    markdown.append(f" * ⚠️ line {result.linenumber} __{result.rule.shortdesc}__")
                    markdown.append(f"   * {result.message}")
        markdown.append("## Template Rendering")
        for checker_result in self.checker_results:
            if checker_result.jinja_errors is not None:
                markdown.append(f"__{checker_result.path}__")
                markdown.append(f" ❌ Jinja error on line {checker_result.jinja_errors.lineno} __{checker_result.jinja_errors.message}__")
            else:
                markdown.append(f"<details><summary> {checker_result.path} </summary>")
                markdown.append("")
                markdown.append("```yaml")
                markdown.append(checker_result.rendered_template)
                markdown.append("```")
                markdown.append("</detail>")
        return "\n".join(markdown)