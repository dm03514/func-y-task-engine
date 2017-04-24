import os
import unittest

from mock import mock

from funcytaskengine.templateprocessors.environmentalvariable import EnvironmentalVariableTemplateProcessor


class EvnironmentalVariableTemplateProcessorTestCase(unittest.TestCase):

    def test_variable_found_in_env(self):
        env_var_processor = EnvironmentalVariableTemplateProcessor()
        template_str = 'this is a really cool$ENV_VAR_HIENV'
        with mock.patch.dict(os.environ, {'HIENV': 'replaced'}):
            processed_str = env_var_processor.substitute(template_str)
            self.assertEqual(
                processed_str,
                'this is a really coolreplaced'
            )

    def test_variable_not_in_env_key_error(self):
        env_var_processor = EnvironmentalVariableTemplateProcessor()
        template_str = 'this is a really cool$ENV_VAR_HIENV'
        with mock.patch.dict(os.environ, {}):
            with self.assertRaises(KeyError):
                env_var_processor.substitute(template_str)

