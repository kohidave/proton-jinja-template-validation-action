import os
import sys
from tokenize import group
from cfnlint.api import lint_all
from summary import Summary
from template_checker.render import Renderer
from template_checker.schema_reader import SchemaReader
from template_checker.template_dir import TemplateDir
import jinja2

def print_group(group_name, content):
    print("::group::" + group_name)
    print(content)
    print("::endgroup::")

def print_warning(file_name, line, title, message):
    print("::warning file=%s,line=%s,title=%s::%s" % (file_name, line, title, message))

def print_error(file_name, line, title, message):
    print("::error file=%s,line=%s,title=%s::%s" % (file_name, line, title, message))

class JinjaError:
    def __init__(self, message, lineno = -1):
        self.message = message
        self.lineno = lineno

class CheckerResult:
    def __init__(self, template_path, linter_results = [], jinja_errors = None, rendered_template = ""):
        self.path = template_path
        self.linter_results = linter_results
        self.rendered_template = rendered_template
        self.jinja_errors = jinja_errors
    
    def log_rendered_template(self):
        print_group(self.path, self.rendered_template)
    
    def log_linter_findings(self):
        for result in self.linter_results:
            if result.rule.severity == "error":
                print_error(self.path, result.linenumber, result.rule.shortdesc, result.message)
            elif result.rule.severity == "warning":
                print_warning(self.path, result.linenumber, result.rule.shortdesc, result.message)                

    def log_findings(self):
        self.log_linter_findings()
        if self.jinja_errors is not None:
            print_error(self.path, self.jinja_errors.lineno, "Jinja error", self.jinja_errors.message)

    def has_errors(self):
        for result in self.linter_results:
            if result.rule.severity == "error":
                return True
        if self.jinja_errors is not None:
            return True 
        return False


def main():
    failed = False
    checker_results = []

    # First, we fetch all the files that have changed.
    changed_files = os.environ["INPUT_CHANGED_FILES"].split(",")
    # Next, we filter those files to a set of unique template directories.
    template_dirs = TemplateDir.from_paths(changed_files)

    # Go through each template directory that had some change in it,
    # render it using the sample specs provided, and then lint 
    # the rendered templates. 
    for template_dir in template_dirs:
        schema_for_template_dir = SchemaReader(template_dir)
        renderer = Renderer(template_dir, schema_for_template_dir)

        # Render and lint the rendered CloudFormation
        if schema_for_template_dir.schema_type().is_service:
            # Render and lint the Service Instance template
            try: 
                rendered_service_instance_cf = renderer.render_service_instance()
                checker_result = CheckerResult(template_dir.instance_infra_path(), lint_all(rendered_service_instance_cf), None, rendered_service_instance_cf)
                checker_results.append(checker_result)
            except jinja2.TemplateSyntaxError as exc:
                checker_results.append(CheckerResult(template_dir.instance_infra_path(), [], JinjaError(exec.message, exec.lineno), ""))
            except jinja2.TemplateError as exc:
                checker_results.append(CheckerResult(template_dir.instance_infra_path(), [], JinjaError(exec.message, -1), ""))


            # Render and lint the Pipeline template, if it is present.
            #if schema_for_template_dir.schema_type().pipeline_present:
        elif schema_for_template_dir.schema_type().is_env:
            try:
                rendered_cloudformation = renderer.render_environment()
                checker_result = CheckerResult(template_dir.environment_infra_path(), lint_all(rendered_cloudformation), [], rendered_cloudformation)
                checker_results.append(checker_result)
            except jinja2.TemplateSyntaxError as exc:
                checker_results.append(CheckerResult(template_dir.instance_infra_path(), [], JinjaError(exec.message, exec.lineno), ""))
            except jinja2.TemplateError as exc:
                checker_results.append(CheckerResult(template_dir.instance_infra_path(), [], JinjaError(exec.message, -1), ""))


        for result in checker_results:
            result.log_findings()
            if result.has_errors():
                failed = True

    # Write a summary markdown file so the customer gets a nice view of what happened.
    with open(os.environ["GITHUB_STEP_SUMMARY"], 'w') as f:
        f.write(Summary(failed, checker_results).markdown())
    if failed:
        sys.exit("Errors detected linting templates")

if __name__ == "__main__":
    main()
