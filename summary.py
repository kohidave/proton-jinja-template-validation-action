class Summary:
    def __init__(self, failed, linting_findings, rendered_templates_by_path):
        self.failed = failed
        self.findings = linting_findings
        self.rendered_templates_by_path = rendered_templates_by_path
    
    def markdown(self):
        markdown = []
        markdown.append("# Template Checker Findings 🕵️‍♀️")
        if self.failed:
            markdown.append("❌ some errors were found linting your templates")
        else:
            markdown.append("✅ no linting errors were found 🥳")
        markdown.append("## Linting Results")
        for result in self.findings:
            if result.rule.severity == "error":
                markdown.append(f" * ❌ {result.filename}:{result.linenumber} __{result.message}__")
            elif result.rule.severity == "warning":
                markdown.append(f" * ⚠️ {result.filename}:{result.linenumber} __{result.message}__")
        markdown.append("## Rendered Templates")
        for path in self.rendered_templates_by_path:
            markdown.append(f"<details><summary> {path} </summary>")
            markdown.append("```yaml")
            markdown.extend(self.rendered_templates_by_path[path].splitlines())
            markdown.append("```")
            markdown.append("</detail>")
        return "\n".join(markdown)