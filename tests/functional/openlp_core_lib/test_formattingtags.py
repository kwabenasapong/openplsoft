"""
Package to test the openlp.core.lib.formattingtags package.
"""
import copy
from unittest import TestCase

from mock import patch

from openlp.core.lib import FormattingTags


TAG = {
    u'end tag': '{/aa}',
    u'start html': '<span>',
    u'start tag': '{aa}',
    u'protected': False,
    u'end html': '</span>',
    u'desc': 'name'
}


class TestFormattingTags(TestCase):

    def tearDown(self):
        """
        Clean up the FormattingTags class.
        """
        FormattingTags.html_expands = []

    def get_html_tags_no_user_tags_test(self):
        """
        Test the FormattingTags class' get_html_tags static method.
        """
        with patch(u'openlp.core.lib.translate') as mocked_translate, \
                patch(u'openlp.core.lib.settings') as mocked_settings, \
                patch(u'openlp.core.lib.formattingtags.cPickle') as mocked_cPickle:
            # GIVEN: Our mocked modules and functions.
            mocked_translate.side_effect = lambda module, string_to_translate, comment: string_to_translate
            mocked_settings.value.return_value = u''
            mocked_cPickle.load.return_value = []

            # WHEN: Get the display tags.
            FormattingTags.load_tags()
            old_tags_list = copy.deepcopy(FormattingTags.get_html_tags())
            FormattingTags.load_tags()
            new_tags_list = FormattingTags.get_html_tags()

            # THEN: Lists should be identically.
            assert old_tags_list == new_tags_list, u'The formatting tag lists should be identically.'

    def get_html_tags_with_user_tags_test(self):
        """
        Test the FormattingTags class' get_html_tags static method in combination with user tags.
        """
        with patch(u'openlp.core.lib.translate') as mocked_translate, \
                patch(u'openlp.core.lib.settings') as mocked_settings, \
                patch(u'openlp.core.lib.formattingtags.cPickle') as mocked_cPickle:
            # GIVEN: Our mocked modules and functions.
            mocked_translate.side_effect = lambda module, string_to_translate: string_to_translate
            mocked_settings.value.return_value = u''
            mocked_cPickle.loads.side_effect = [[], [TAG]]

            # WHEN: Get the display tags.
            FormattingTags.load_tags()
            old_tags_list = copy.deepcopy(FormattingTags.get_html_tags())

            # WHEN: Add our tag and get the tags again.
            FormattingTags.load_tags()
            FormattingTags.add_html_tags([TAG])
            new_tags_list = FormattingTags.get_html_tags()

            # THEN: Lists should not be identically.
            assert old_tags_list != new_tags_list, u'The lists should be different.'

            # THEN: Added tag and last tag should be the same.
            new_tag = new_tags_list.pop()
            assert TAG == new_tag, u'Tags should be identically.'
