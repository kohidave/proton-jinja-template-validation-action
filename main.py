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

def build_service_instance_input(spec, env_outputs):
    service_instance_config = spec['instances'][0]
    return {
        "environment": {
            "name": service_instance_config['environment'],
            "account_id": "1111111111",
            "outputs" : env_outputs},
        "service": {
            "name": "sample-service",
            "branch_name": "main",
            "repository_connection_arn": "arn:connection:dummy",
            "repository_id": "github/sample-repo"},
        "service_instance": {
            "name": service_instance_config['name'],
            "inputs": service_instance_config['spec']
        # No components yet
        }
    }

def default_values_from_schema(schema):
    schema_input_type_name = schema["schema"]["service_input_type"]
    schema_parameters = schema["types"][schema_input_type_name]["properties"]
    property_defaults = {}
    for property, definition in schema_parameters.iteritems():
        if (definition.default != None): 
            property_defaults[property] = definition.default
    return property_defaults

def read_hydrated_spec(sample_spec_yaml, schema_file_yaml):
    default_values = default_values_from_schema(schema_file_yaml)
    return sample_spec_yaml['instances'].map(lambda provided_values: default_values | provided_values )

def main():
    repo_path =""
    # First, i want to fetch all the files that have changed.
    changed_files = os.environ["INPUT_CHANGED_FILES"].split(",")
    # Next, I want to group these into template directories
    changed_template_files = set(filter(looks_like_template_dir, changed_files))

    template_dirs = set(map(top_level_template_dir, changed_template_files))

    for template_dir in template_dirs:
        environment = Environment(loader=FileSystemLoader(repo_path + template_dir))
        instance_infra_template = environment.get_template("/instance_infrastructure/cloudformation.yaml")
        pipeline_infra_template = environment.get_template("/pipeline_infrastructure/cloudformation.yaml")

        with open(repo_path+template_dir+"/schema/schema.yaml", "r") as schemaStream:
            try:
                schema = yaml.safe_load(schemaStream)
                # assume a spec/spec.yaml file
                with open(repo_path + template_dir + "/spec/spec.yaml", "r") as specStream:
                    sample_spec_yaml = yaml.safe_load(specStream)
                    hydrated_spec = read_hydrated_spec(sample_spec_yaml, schema)
                    print("spec with defaults:")
                    print(hydrated_spec)
                    instnace_render_input = build_service_instance_input(hydrated_spec, {
                            "TableName": "DummyTable" # This should come from customer
                    })
                    print(instnace_render_input)
                    rendered_instance_yaml = instance_infra_template.render(instnace_render_input)
                    print(rendered_instance_yaml)
                    #rendered_pipeline_yaml = pipeline_infra_template.render(sample_spec_yaml)
            except yaml.YAMLError as exc:
                print(exc)                    


if __name__ == "__main__":
    main()
