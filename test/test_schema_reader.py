from unittest import TestCase
from template_checker.schema_reader import SchemaReader
from template_checker.template_dir import TemplateDir

class TestLint(TestCase):
    def test_schema_type_service(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_template")
        reader = SchemaReader(sample_template)
        schema_type = reader.schema_type()
        self.assertEqual(
            "SERVICE",
            schema_type.template_type
        )

        self.assertEqual(
            "service_input_type",
            schema_type.schema_path
        )

        self.assertTrue(schema_type.is_service)        
        self.assertFalse(schema_type.pipeline_present)                
        self.assertFalse(schema_type.is_env)                

    def test_schema_type_service_pipeline(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_pipeline_template")
        reader = SchemaReader(sample_template)
        schema_type = reader.schema_type()
        self.assertEqual(
            "SERVICE",
            schema_type.template_type
        )

        self.assertEqual(
            "service_input_type",
            schema_type.schema_path
        )

        self.assertTrue(schema_type.is_service)        
        self.assertTrue(schema_type.pipeline_present)                
        self.assertFalse(schema_type.is_env)                        

    def test_schema_type_env(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_env_template")
        reader = SchemaReader(sample_template)
        schema_type = reader.schema_type()
        self.assertEqual(
            "ENVIRONMENT",
            schema_type.template_type
        )

        self.assertEqual(
            "environment_input_type",
            schema_type.schema_path
        )

        self.assertFalse(schema_type.is_service)        
        self.assertFalse(schema_type.pipeline_present)                
        self.assertTrue(schema_type.is_env)                                

    def test_service_schema_defaults(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_template")
        reader = SchemaReader(sample_template)
        self.assertEqual(
            {'port': 80, 'desired_count': 1, 'task_size': 'x-small', 'subnet_type': 'public', 'loadbalancer_type': 'application', 'image': 'public.ecr.aws/nginx/nginx:1.21', 'backendurl': 'backend-svc-inst.backend-svc.fargate-env.local:80'},
            reader.schema_defaults()
        )

    def test_service_pipeline_schema_defaults(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_pipeline_template")
        reader = SchemaReader(sample_template)
        self.assertEqual(
            {'code_dir': 'lambda-ping-sns', 'unit_test_command': "echo 'add your unit test command here'", 'packaging_command': 'zip function.zip app.js'},
            reader.pipeline_schema_defaults()
        )

    def test_env_schema_defaults(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_env_template")
        reader = SchemaReader(sample_template)
        self.assertEqual(
            {'vpc_cidr': '10.0.0.0/16', 'subnet_one_cidr': '10.0.0.0/24', 'subnet_two_cidr': '10.0.1.0/24'},
            reader.schema_defaults()
        )
