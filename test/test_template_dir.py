from unittest import TestCase
from template_checker.template_dir import TemplateDir

class TestLint(TestCase):

        # Ensure that we can determine if a file path is part of a template directory.
        def test_is_path_template_dir_valid_paths(self):
            valid_paths = [
            "/my-repo/my-service-template/v1/service/instance_infrastructure/cloudformation.yaml",
            "/my-repo/my-service-template/v1/service/pipeline_infrastructure/cloudformation.yaml",
            "/my-repo/my-env-template/v1/infrastructure/cloudformation.yaml",
            "/my-repo/my-env-template/v1/schema/schema.yaml",
            "/my-repo/my-env-template/v1/spec/spec.yaml",
            "/my-repo/my-svc-template/v1/spec/sample-outputs.yaml",
            "/my-repo/my-svc-template/v1/spec/env-spec.yaml"]

            for path in valid_paths:
                self.assertEqual(
                    True,
                    TemplateDir.is_path_template_dir(path),
                    "Expected to be true: " + path)

        # Ensure that we can determine if a file path is NOT part of a template directory.
        def test_is_path_template_dir_invalid_paths(self):
            self.assertEqual(
                False,
                TemplateDir.is_path_template_dir("/my-cool-dir/favorite_services.txt"))

        # Ensure that we can, given a path within a template directory, fetch the top level of the template dir
        def test_top_level_template_dir(self):
            valid_paths = [
            "/my-repo/my-cool-template/v1/instance_infrastructure/cloudformation.yaml",
            "/my-repo/my-cool-template/v1/pipeline_infrastructure/cloudformation.yaml",
            "/my-repo/my-cool-template/v1/infrastructure/cloudformation.yaml",
            "/my-repo/my-cool-template/v1/schema/schema.yaml",
            "/my-repo/my-cool-template/v1/spec/spec.yaml",
            "/my-repo/my-cool-template/v1/spec/sample-outputs.yaml",
            "/my-repo/my-cool-template/v1/spec/env-spec.yaml"]            
            for path in valid_paths:
                self.assertEqual(
                    "/my-repo/my-cool-template/v1",
                    TemplateDir.top_level_template_dir(path),
                    path)

        # Ensure that we can convert a bunch of paths to TemplateDir objects.
        def test_from_paths_many_paths(self):
            paths = [
            "/my-repo/my-service-template/v1/service/instance_infrastructure/cloudformation.yaml",
            "/my-repo/my-service-template/v1/service/pipeline_infrastructure/cloudformation.yaml",
            "/my-repo/my-env-template/v1/infrastructure/cloudformation.yaml",
            "/my-repo/my-env-template/v1/schema/schema.yaml",
            "/my-repo/my-env-template/v1/spec/spec.yaml",
            "/my-repo/my-svc-template/v1/spec/sample-outputs.yaml",
            "/my-repo/my-svc-template/v1/spec/env-spec.yaml",
            "/my-cool-dir/favorite_services.txt" # Make sure we throw in some extra paths
            ]            

            self.assertEqual(
                3,
                len(TemplateDir.from_paths(paths)))

        # Ensure that we can convert a single path to TemplateDir objects.
        def test_from_paths_single_path(self):
            paths = [
            "/my-repo/my-service-template/v1/service/instance_infrastructure/cloudformation.yaml",
            "/my-cool-dir/favorite_services.txt" # Make sure we throw in some extra paths
            ]            

            template_dirs = TemplateDir.from_paths(paths)
            self.assertEqual(
                1,
                len(template_dirs))
            
            generated_template_dir = template_dirs.pop()
            self.assertEqual(
                "",
                generated_template_dir.repo_path
            )
            self.assertEqual(
                "/my-repo/my-service-template/v1/service",
                generated_template_dir.template_path
            )            
            self.assertEqual(
                "/my-repo/my-service-template/v1/service",
                generated_template_dir.path
            )     

        def test_template_dir_attributes(self):
            test_template_dir = TemplateDir("", "/my-cool-repo")
            self.assertEqual(
                "/my-cool-repo/schema/schema.yaml",
                test_template_dir.schema_path()
            )              
            self.assertEqual(
                "/my-cool-repo/spec/sample-outputs.yaml",
                test_template_dir.sample_outputs_path()
            )  
            self.assertEqual(
                "/my-cool-repo/spec/spec.yaml",
                test_template_dir.sample_spec_path()
            )              
            self.assertEqual(
                "/my-cool-repo/instance_infrastructure/cloudformation.yaml",
                test_template_dir.instance_infra_path()
            )                   
            self.assertEqual(
                "/my-cool-repo/pipeline_infrastructure/cloudformation.yaml",
                test_template_dir.pipeline_infra_path()
            )             
            self.assertEqual(
                "/my-cool-repo/infrastructure/cloudformation.yaml",
                test_template_dir.environment_infra_path()
            )             
                        