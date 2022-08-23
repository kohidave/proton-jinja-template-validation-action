import os
from jinja2 import Environment, FileSystemLoader
import yaml

def looks_like_template_dir(path): 
    return path.find("/instance_infrastructure/") != -1 or path.find("/pipeline_infrastructure/") != -1 or path.find("/schema/") != -1 or path.find("/spec/spec.yaml") != -1

def top_level_template_dir(path):
    print("Trying to find tld of " + path)
    instance_infra_folder_index  = path.find("/instance_infrastructure/")
    pipeline_infra_folder_index = path.find("/pipeline_infrastructure/")
    schema_folder_index = path.find("/schema/")
    spec_folder_index = path.find("/spec/spec.yaml")

    if instance_infra_folder_index != -1:
        return path[0:instance_infra_folder_index]
    if pipeline_infra_folder_index != -1:
        return path[0:pipeline_infra_folder_index]     
    if schema_folder_index != -1:
        return path[0:schema_folder_index]     
    if spec_folder_index != -1:
        return path[0:spec_folder_index]
    return ""

def main():
    repo_path =""
    print(repo_path)
    # First, i want to fetch all the files that have changed.
    changed_files = os.environ["INPUT_CHANGED_FILES"].split(",")
    print(changed_files)
    # Next, I want to group these into template directories
    changed_template_files = set(filter(looks_like_template_dir, changed_files))
    print(changed_template_files)

    template_dirs = set(map(top_level_template_dir, changed_template_files))
    print(template_dirs)

    for template_dir in template_dirs:
        environment = Environment(loader=FileSystemLoader(repo_path + template_dir))
        instance_infra_template = environment.get_template("/instance_infrastructure/cloudformation.yaml")
        pipeline_infra_template = environment.get_template("/pipeline_infrastructure/cloudformation.yaml")

        # assume a spec/spec.yaml file
        with open(repo_path + template_dir + "/spec/spec.yaml", "r") as stream:
            try:
                sample_spec_yaml = print(yaml.safe_load(stream))
                rendered_instance_yaml = instance_infra_template.render(sample_spec_yaml)
                rendered_pipeline_yaml = pipeline_infra_template.render(sample_spec_yaml)
            except yaml.YAMLError as exc:
                print(exc)

if __name__ == "__main__":
    main()
