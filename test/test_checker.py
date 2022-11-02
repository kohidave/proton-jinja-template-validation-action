from unittest import TestCase
from template_checker.template_dir import TemplateDir
from pathlib import Path
from main import get_checker_results

class TestChecker(TestCase):
    def test_checker_handles_jinja_syntax_error(self):
        sample_template = TemplateDir("", "test/sample_templates/invalid_jinja_syntax_template")
        checker_results = get_checker_results([sample_template])
        self.assertEqual(
            1,
            len(checker_results))
        checker_result = checker_results[0]
        self.assertIsNotNone(checker_result.jinja_errors)
        self.assertEqual("expected token 'end of statement block', got 'SecurityGroups'", checker_result.jinja_errors.message)
        self.assertEqual(31, checker_result.jinja_errors.lineno)
        self.assertTrue(checker_result.has_errors)

    def test_checker_handles_jinja_error(self):
        sample_template = TemplateDir("", "test/sample_templates/invalid_jinja_template")
        checker_results = get_checker_results([sample_template])
        self.assertEqual(
            1,
            len(checker_results))
        checker_result = checker_results[0]
        self.assertIsNotNone(checker_result.jinja_errors)
        self.assertEqual("'dict object' has no attribute 'this_does'", checker_result.jinja_errors.message)
        self.assertEqual(-1, checker_result.jinja_errors.lineno)
        self.assertTrue(checker_result.has_errors())
        
    def test_checker_handles_valid_template(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_template")
        expected_rendered_template = Path('test/sample_templates/valid_svc_template/expected_rendered_output.yaml').read_text()
        checker_results = get_checker_results([sample_template])
        self.assertEqual(
            1,
            len(checker_results))
        checker_result = checker_results[0]
        self.assertFalse(checker_result.has_errors())        
        self.assertEqual(expected_rendered_template, checker_result.rendered_template)
        self.assertEqual(4, len(checker_result.linter_results))

    def test_checker_handles_valid_svc_pipeline_template(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_svc_pipeline_template")
        expected_rendered_template = Path('test/sample_templates/valid_svc_pipeline_template/expected_pipeline_rendered_output.yaml').read_text()
        checker_results = get_checker_results([sample_template])
        self.assertEqual(
            2,
            len(checker_results))
        svc_result = checker_results[0]
        pipeline_result = checker_results[1]
        self.assertEqual(expected_rendered_template, pipeline_result.rendered_template)

    def test_checker_handles_template_with_linting_error(self):
        sample_template = TemplateDir("", "test/sample_templates/valid_env_template")
        expected_rendered_template = Path('test/sample_templates/valid_env_template/expected_rendered_output.yaml').read_text()
        checker_results = get_checker_results([sample_template])
        self.assertEqual(
            1,
            len(checker_results))
        checker_result = checker_results[0]
        self.assertTrue(checker_result.has_errors())
        self.assertEqual(expected_rendered_template, checker_result.rendered_template)

    def test_checker_handles_template_invalid_bundle(self):
        sample_template = TemplateDir("", "test/sample_templates/invalid_template_bundle")
        checker_results = get_checker_results([sample_template])
        self.assertEqual(
            1,
            len(checker_results))
        checker_result = checker_results[0]
        self.assertTrue(checker_result.has_errors())       
        self.assertEqual("Error reading the schema file: [Errno 2] No such file or directory: 'test/sample_templates/invalid_template_bundle/schema/schema.yaml'", checker_result.unknown_error)        

