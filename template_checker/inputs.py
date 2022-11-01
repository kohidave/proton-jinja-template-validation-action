import yaml

# Generates the inputs needed to render the template using the sample
# specs and the schema defaults.
class InputProvider:
    def __init__(self, tmpl_dir, schema_reader):
        self.template_dir = tmpl_dir
        self.schema_reader = schema_reader

    def sample_env_outputs(self):
        with open(self.template_dir.sample_env_output_path() , "r") as envOutputsStream:
            return yaml.safe_load(envOutputsStream)

    def __read_sample_spec(self):
        with open(self.template_dir.sample_spec_path() , "r") as specOutputStream:
            return yaml.safe_load(specOutputStream)  

    def service_instance_input(self):
        default_values = self.schema_reader.schema_defaults()
        sample_spec = self.__read_sample_spec()
        for instance in sample_spec['instances']:
            instance["spec"] = default_values | instance["spec"]
        return sample_spec

    def pipeline_input(self):
        default_values = self.schema_reader.pipeline_schema_defaults()
        sample_spec = self.__read_sample_spec()
        return default_values | sample_spec['pipeline']

    def environment_input(self):
        default_values = self.schema_reader.schema_defaults()
        sample_spec = self.__read_sample_spec()
        return default_values | sample_spec["spec"]

    # This method returns the full data required to render
    # a service instance template.
    def service_instance_render_input(self):
        service_instance_inputs = self.service_instance_input()
        if ('instances' not in service_instance_inputs or len(service_instance_inputs['instances']) == 0): 
            raise "You must provide at least one service instance input in the sample spec"

        service_instance_config = service_instance_inputs['instances'][0]
        return {
            "environment": {
                "name": service_instance_config['environment'],
                "account_id": "1111111111",
                "outputs" : self.sample_env_outputs()},
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