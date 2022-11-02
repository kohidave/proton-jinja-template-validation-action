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
