import yaml
from pathlib import Path

# Generates the inputs needed to render the template using the sample
# specs and the schema defaults.
class InputProvider:
    def __init__(self, tmpl_dir, schema_reader):
        self.template_dir = tmpl_dir
        self.schema_reader = schema_reader

    def sample_env_outputs(self):
        if not Path(self.template_dir.sample_outputs_path()).exists():
            return {}

        with open(self.template_dir.sample_outputs_path() , "r") as sampleOutputsStream:
            sample_outputs = yaml.safe_load(sampleOutputsStream)
            if "environment" not in sample_outputs:
                return {}
            return sample_outputs["environment"]

    def sample_svc_outputs(self):
        if not Path(self.template_dir.sample_outputs_path()).exists():
            return {}
        
        with open(self.template_dir.sample_outputs_path() , "r") as sampleOutputsStream:
            sample_outputs = yaml.safe_load(sampleOutputsStream)
            if "service" not in sample_outputs:
                return {}
            return sample_outputs["service"]

    def __read_sample_spec(self):
        with open(self.template_dir.sample_spec_path() , "r") as specOutputStream:
            return yaml.safe_load(specOutputStream)  

    def service_instance_input(self):
        default_values = self.schema_reader.schema_defaults()
        sample_spec = self.__read_sample_spec()
        for instance in sample_spec['instances']:
            instance["spec"] = default_values | instance["spec"]
        return sample_spec

    def service_instance_input_for_pipeline(self):
        default_values = self.schema_reader.schema_defaults()
        sample_spec = self.__read_sample_spec()
        for instance in sample_spec['instances']:
            # Update the environment field to include a nested structure with
            # the name of the env, account ID and env outputs. 
            env_name = instance["environment"]
            instance["environment"] = {
                    "name": env_name,
                    "account_id": "11111111",
                    "outputs": self.sample_env_outputs()
            }
            # Rename the instance values in the spec as "input" and
            # merge the spec's default values in.
            instance["input"] = default_values | instance["spec"]
            instance["outputs"] = self.sample_svc_outputs()
            instance.pop('spec', None)
        return sample_spec

    def pipeline_input(self):
        default_values = self.schema_reader.pipeline_schema_defaults()
        sample_spec = self.__read_sample_spec()
        return default_values | sample_spec['pipeline']

    def environment_input(self):
        default_values = self.schema_reader.schema_defaults()
        sample_spec = self.__read_sample_spec()
        return default_values | sample_spec["spec"]

    def pipeline_render_input(self):
        service_instance_inputs = self.service_instance_input_for_pipeline()
        if ('instances' not in service_instance_inputs or len(service_instance_inputs['instances']) == 0): 
            raise "You must provide at least one service instance input in the sample spec"

        service_instances = service_instance_inputs['instances']

        return {
            "pipeline":{
                "inputs": self.pipeline_input()
            },
            "service_instances": service_instances,
            "service": {
                "name": "sample-service",
                "branch_name": "main",
                "repository_connection_arn": "arn:connection:dummy",
                "repository_id": "github/sample-repo"
            }
        }

    def environment_render_input(self):
        return {
            "environment": {
                "name": "sample-env",
                "inputs": self.environment_input()
            }
        }

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