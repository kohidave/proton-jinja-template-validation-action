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
        self.assertTrue(checker_result.has_errors)
        