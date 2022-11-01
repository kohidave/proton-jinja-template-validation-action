import os
from pprint import pprint
import sys
from tokenize import group
from cfnlint.api import lint_all
from summary import Summary
from template_checker.render import Renderer
from template_checker.schema_reader import SchemaReader
from template_checker.template_dir import TemplateDir

def print_group(group_name, content):
    print("::group::" + group_name)
    print(content)
    print("::endgroup::")

def print_warning(file_name, line, title, message):
    print("::warning file={%s},line={%s},title={%s}::%s" % (file_name, line, title, message))

def print_error(file_name, line, title, message):
    print("::warning file={%s},line={%s},title={%s}::%s" % (file_name, line, title, message))

class CheckerResult:
    def __init__(self, template_path, linter_results, rendered_template):
        self.path = template_path
        self.linter_results = linter_results
        self.rendered_template = rendered_template
    
    def log_rendered_template(self):
            print_group(self.path, self.rendered_template)
    
    def log_linter_findings(self):
        for result in self.linter_results:
            if result.rule.severity == "error":
                print_error(self.path, result.linenumber, result.rule.shortdesc, result.message)
            elif result.rule.severity == "warning":
                print_warning(self.path, result.linenumber, result.rule.shortdesc, result.message)                
   
    def has_linter_errors(self):
        for result in self.linter_results:
            if result.rule.severity == "error":
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
        linting_results = []
        # Render and lint the rendered CloudFormation
        if schema_for_template_dir.schema_type().is_service:
            # Render and lint the Service Instance template
            rendered_service_instance_cf = renderer.render_service_instance()
            checker_result = CheckerResult(template_dir.instance_infra_path(), lint_all(rendered_service_instance_cf), rendered_service_instance_cf)
            checker_results.append(checker_result)
            # Render and lint the Pipeline template, if it is present.
            #if schema_for_template_dir.schema_type().pipeline_present:
            #    rendered_pipeline_cf = renderer.render_pipeline() 
            #    linting_results.extend(lint_all(rendered_pipeline_cf))
            #    print_group(template_dir.pipeline_infra_path(), rendered_pipeline_cf)
            #    rendered_templates[template_dir.pipeline_infra_path()] = rendered_pipeline_cf
        elif schema_for_template_dir.schema_type().is_env:
            rendered_cloudformation = renderer.render_environment()
            checker_result = CheckerResult(template_dir.environment_infra_path(), lint_all(rendered_cloudformation), rendered_cloudformation)
            checker_results.append(checker_result)

        for result in checker_results:
            result.log_linter_findings()
            if result.has_linter_errors:
                failed = True

    # Write a summary markdown file so the customer gets a nice view of what happened.
    with open(os.environ["GITHUB_STEP_SUMMARY"], 'w') as f:
        f.write(Summary(failed, checker_results).markdown())
    if failed:
        sys.exit("Errors detected linting templates")

if __name__ == "__main__":
    main()
