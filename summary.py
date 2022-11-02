class Summary:
    def __init__(self, failed, checker_results):
        self.failed = failed
        self.checker_results = checker_results
    
    def markdown(self):
        markdown = []
        markdown.append("# Template Checker Findings 🔎")
        if self.failed:
            markdown.append("🔴 Some errors were found rendering and linting your templates")
        else:
            markdown.append("✅ No rendering or linting errors were found 🥳")
        markdown.append("## Warnings and Errors")
        for checker_result in self.checker_results:
            markdown.append(f"### {checker_result.path}")
            for result in checker_result.linter_results:
                if result.rule.severity == "error":
                    markdown.append(f" * 🔴 line {result.linenumber} __{result.rule.shortdesc}__")
                    markdown.append(f"   * Rule {result.rule.id} `{result.message}`")
                elif result.rule.severity == "warning":
                    markdown.append(f" * ⚠️ line {result.linenumber} __{result.rule.shortdesc}__")
                    markdown.append(f"   * Rule {result.rule.id} `{result.message}`")
            if checker_result.jinja_errors is not None:
                markdown.append(f" * 🔴 line {checker_result.jinja_errors.lineno} __Jinja parsing exception__")
                markdown.append(f"   * `{checker_result.jinja_errors.message}`")
            if checker_result.unknown_error != "":
                markdown.append(f" * 🔴 {checker_result.unknown_error}")

        markdown.append("## Rendered Templates")
        for checker_result in self.checker_results:
            if checker_result.rendered_template != "":
                markdown.append(f"<details><summary> {checker_result.path} </summary>")
                markdown.append("")
                markdown.append("```yaml")
                markdown.append(checker_result.rendered_template)
                markdown.append("```")
                markdown.append("</detail>")
                markdown.append("")
        return "\n".join(markdown)