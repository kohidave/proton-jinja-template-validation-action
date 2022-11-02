from unittest import TestCase
from template_checker.inputs import InputProvider
from template_checker.schema_reader import SchemaReader
from template_checker.template_dir import TemplateDir

class TestLint(TestCase):
    def test_service_instance_input(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_template")
        reader = SchemaReader(sample_template)
        input_provider = InputProvider(sample_template, reader)
        self.assertEqual(
            {'proton': 'ServiceSpec', 'pipeline': {'service_dir': 'ecs-static-website', 'dockerfile': 'Dockerfile', 'unit_test_command': "echo 'add your unit test command here'"}, 'instances': [{'name': 'load-balanced-fargate-svc-prod', 'environment': 'fargate-env-prod', 'spec': {'port': 80, 'desired_count': 1, 'task_size': 'x-small', 'subnet_type': 'public', 'loadbalancer_type': 'application', 'image': 'public.ecr.aws/nginx/nginx:1.21', 'backendurl': 'backend-svc-inst.backend-svc.fargate-env.local:80', 'empty': True}}]},
            input_provider.service_instance_input()
        )

    def test_service_instance_render_input(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_template")
        reader = SchemaReader(sample_template)
        input_provider = InputProvider(sample_template, reader)
        self.assertEqual(
            {'environment': {'name': 'fargate-env-prod', 'account_id': '1111111111', 'outputs': {'ServiceTaskDefExecutionRoleArn': 'arn:aws:iam::012345678901:role/role-name-with-path', 'SNSTopicArn': 'arn:aws:sns::012345678901:topic/role-name-with-path', 'SNSTopicName': 'my-cool-topic', 'VPCSecurityGroup': 'daves-cool-security-group', 'PrivateSubnet1': 'subnet-1', 'PrivateSubnet2': 'subnet-2', 'PublicSubnet1': 'public-subnet-1', 'PublicSubnet2': 'public-subnet-2', 'Cluster': 'my-cluster', 'CloudMapNamespaceId': 'cluster-name-space', 'VPC': '12343-vpc', 'SNSRegion': 'us-west-2'}}, 'service': {'name': 'sample-service', 'branch_name': 'main', 'repository_connection_arn': 'arn:connection:dummy', 'repository_id': 'github/sample-repo'}, 'service_instance': {'name': 'load-balanced-fargate-svc-prod', 'inputs': {'port': 80, 'desired_count': 1, 'task_size': 'x-small', 'subnet_type': 'public', 'loadbalancer_type': 'application', 'image': 'public.ecr.aws/nginx/nginx:1.21', 'backendurl': 'backend-svc-inst.backend-svc.fargate-env.local:80', 'empty': True}}},
            input_provider.service_instance_render_input()
        )

    def test_service_pipeline_input(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_pipeline_template")
        reader = SchemaReader(sample_template)
        input_provider = InputProvider(sample_template, reader)
        self.assertEqual(
            {'code_dir': 'lambda-ping-sns', 'unit_test_command': 'make test', 'packaging_command': 'zip function.zip app.js', 'packaging_commands': 'make publish'},
            input_provider.pipeline_input()
        )

    def test_environment_input(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_env_template")
        reader = SchemaReader(sample_template)
        input_provider = InputProvider(sample_template, reader)
        self.assertEqual(
            {'vpc_cidr': '10.0.0.0/16', 'public_subnet_one_cidr': '10.0.0.0/18', 'public_subnet_two_cidr': '10.0.64.0/18', 'private_subnet_one_cidr': '10.0.128.0/18', 'private_subnet_two_cidr': '10.0.192.0/18'},
            input_provider.environment_input()
        )

    def test_environment_render_input(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_env_template")
        reader = SchemaReader(sample_template)
        input_provider = InputProvider(sample_template, reader)
        self.assertEqual(
            {'environment': {'name': 'sample-env', 'inputs': {'vpc_cidr': '10.0.0.0/16', 'public_subnet_one_cidr': '10.0.0.0/18', 'public_subnet_two_cidr': '10.0.64.0/18', 'private_subnet_one_cidr': '10.0.128.0/18', 'private_subnet_two_cidr': '10.0.192.0/18'}}},
            input_provider.environment_render_input()
        )

    def test_service_pipeline_render_input(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_pipeline_template")
        reader = SchemaReader(sample_template)
        input_provider = InputProvider(sample_template, reader)
        self.assertEqual(
            {'pipeline': {'inputs': {'code_dir': 'lambda-ping-sns', 'unit_test_command': 'make test', 'packaging_command': 'zip function.zip app.js', 'packaging_commands': 'make publish'}}, 'service_instances': [{'name': 'front-end', 'environment': {'name': 'crud-api-beta', 'account_id': '11111111', 'outputs': {'SNSTopicArn': 'arn:aws:sns:my-cool-topic', 'SNSTopicName': 'my-cool-topic', 'VPCSecurityGroup': 'daves-cool-security-group', 'PrivateSubnet1': 'subnet-1', 'PrivateSubnet2': 'subnet-2', 'PublicSubnet1': 'public-subnet-1', 'PublicSubnet2': 'public-subnet-2'}}, 'input': {'lambda_handler': 'app.handler', 'lambda_memory': 512, 'lambda_timeout': 30, 'lambda_runtime': 'ruby2.7', 'subnet_type': 'public', 'resource_name': 'task', 'resource_handler': 'src/api'}, 'outputs': {'LambdaRuntime': 'ruby2.7'}}], 'service': {'name': 'sample-service', 'branch_name': 'main', 'repository_connection_arn': 'arn:connection:dummy', 'repository_id': 'github/sample-repo'}},
            input_provider.pipeline_render_input()
        )
