from template_checker.inputs import InputProvider


from jinja2 import Environment, FileSystemLoader

class Renderer:
    def __init__(self, template_dir, schema_reader):
        self.template_dir = template_dir
        self.environment = Environment(loader=FileSystemLoader(template_dir.path))
        self.input_provider = InputProvider(template_dir, schema_reader)

    def render_service_instance(self):
        instance_infra_template = self.environment.get_template(self.template_dir.instance_infra_relative_path())
        return instance_infra_template.render(self.input_provider.service_instance_render_input())

    def render_pipeline(self):
        pipeline_infra_template = self.environment.get_template(self.template_dir.pipeline_infra_relative_path())
        return pipeline_infra_template.render(self.input_provider.pipeline_render_input())

    def render_environment(self):
        env_infra_template = self.environment.get_template(self.template_dir.environment_infra_relative_path())
        return env_infra_template.render(self.input_provider.environment_render_input())
