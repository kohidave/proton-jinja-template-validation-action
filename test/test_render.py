from unittest import TestCase
from template_checker.render import Renderer
from template_checker.schema_reader import SchemaReader
from template_checker.template_dir import TemplateDir
from pathlib import Path

class TestRender(TestCase):
    def test_service_instance_render(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_template")
        reader = SchemaReader(sample_template)
        renderer = Renderer(sample_template, reader)
        expected_output = Path('test/sample_templates/valid_svc_template/expected_rendered_output.yaml').read_text()

        self.assertEqual(
            expected_output,  
            renderer.render_service_instance()
        )
    def test_pipeline_render(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_pipeline_template")
        reader = SchemaReader(sample_template)
        renderer = Renderer(sample_template, reader)
        expected_output = Path('test/sample_templates/valid_svc_pipeline_template/expected_pipeline_rendered_output.yaml').read_text()
        self.assertEqual(
            expected_output,  
            renderer.render_pipeline()
        )        

    def test_environment_render(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_env_template")
        reader = SchemaReader(sample_template)
        renderer = Renderer(sample_template, reader)
        expected_output = Path('test/sample_templates/valid_env_template/expected_rendered_output.yaml').read_text()
        self.assertEqual(
            expected_output,  
            renderer.render_environment()
        )       