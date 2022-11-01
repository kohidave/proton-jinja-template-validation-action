import os
from pprint import pprint
import sys
from tokenize import group
from cfnlint.api import lint_all
from template_checker.render import Renderer
from template_checker.schema_reader import SchemaReader
from template_checker.template_dir import TemplateDir

def print_group(group_name, content):
    print("::group::" + group_name)
    print(content)
    print("::endgroup::")

def print_warning(file_name, line, title, message):
    print("::warning file={%s},line={%s},title={%s}::{%s}" % (file_name, line, title, message))

def print_error(file_name, line, title, message):
    print("::warning file={%s},line={%s},title={%s}::{%s}" % (file_name, line, title, message))

def main():
    failed = False
    rendered_templates = {}

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
            linting_results.extend(lint_all(rendered_service_instance_cf))
            print_group(template_dir.template_path + " Service Instance Rendered Template", rendered_service_instance_cf)
            rendered_templates[template_dir.template_path+"service-instance"] = rendered_service_instance_cf
            # Render and lint the Pipeline template, if it is present.
            #if schema_for_template_dir.schema_type().pipeline_present:
            #    rendered_pipeline_cf = renderer.render_pipeline() 
            #    linting_results.extend(lint_all(rendered_pipeline_cf))
            #    print_group(template_dir.template_path + " Pipeline Rendered Template", rendered_pipeline_cf)
            #    rendered_templates[template_dir.template_path+"pipeline"] = rendered_pipeline_cf
        elif schema_for_template_dir.schema_type().is_env:
            rendered_cloudformation = renderer.render_environment()
            linting_results.extend(lint_all(rendered_cloudformation))
            print_group(template_dir.template_path + " Environment Rendered Template", rendered_cloudformation)
            rendered_templates[template_dir.template_path+"environment"] = rendered_cloudformation

        for result in linting_results:
            if result.rule.severity == "error":
                failed = True
                print_error(result.filename, result.linenumber, result.rule.shortdesc, result.message)
            elif result.rule.severity == "warning":
                print_warning(result.filename, result.linenumber, result.rule.shortdesc, result.message)                

    # Write a summary markdown file so the customer gets a nice view of what happened.
    with open(os.environ["GITHUB_STEP_SUMMARY"], 'w') as f:
        f.write(Summary(failed, linting_results, rendered_templates).markdown())
    if failed:
        sys.exit("Errors detected linting templates")

if __name__ == "__main__":
    main()
