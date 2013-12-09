"""
Package to test the openlp.core.ui package.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui, QtTest

from openlp.core.lib import Registry
from openlp.core.ui import starttimeform
from tests.interfaces import MagicMock, patch


class TestStartTimeDialog(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = starttimeform.StartTimeForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def ui_defaults_test(self):
        """
        Test StartTimeDialog are defaults correct
        """
        self.assertEqual(self.form.hourSpinBox.minimum(), 0, 'The minimum hour should stay the same as the dialog')
        self.assertEqual(self.form.hourSpinBox.maximum(), 4, 'The maximum hour should stay the same as the dialog')
        self.assertEqual(self.form.minuteSpinBox.minimum(), 0,
            'The minimum minute should stay the same as the dialog')
        self.assertEqual(self.form.minuteSpinBox.maximum(), 59,
            'The maximum minute should stay the same as the dialog')
        self.assertEqual(self.form.secondSpinBox.minimum(), 0,
            'The minimum second should stay the same as the dialog')
        self.assertEqual(self.form.secondSpinBox.maximum(), 59,
            'The maximum second should stay the same as the dialog')
        self.assertEqual(self.form.hourFinishSpinBox.minimum(), 0,
            'The minimum finish hour should stay the same as the dialog')
        self.assertEqual(self.form.hourFinishSpinBox.maximum(), 4,
            'The maximum finish hour should stay the same as the dialog')
        self.assertEqual(self.form.minuteFinishSpinBox.minimum(), 0,
            'The minimum finish minute should stay the same as the dialog')
        self.assertEqual(self.form.minuteFinishSpinBox.maximum(), 59,
            'The maximum finish minute should stay the same as the dialog')
        self.assertEqual(self.form.secondFinishSpinBox.minimum(), 0,
            'The minimum finish second should stay the same as the dialog')
        self.assertEqual(self.form.secondFinishSpinBox.maximum(), 59,
            'The maximum finish second should stay the same as the dialog')

    def time_display_test(self):
        """
        Test StartTimeDialog display functionality
        """
        # GIVEN: A service item with with time
        mocked_serviceitem = MagicMock()
        mocked_serviceitem.start_time = 61
        mocked_serviceitem.end_time = 3701
        mocked_serviceitem.media_length = 3701

        # WHEN displaying the UI and pressing enter
        self.form.item = {'service_item': mocked_serviceitem}
        with patch('PyQt4.QtGui.QDialog.exec_'):
            self.form.exec_()
        ok_widget = self.form.button_box.button(self.form.button_box.Ok)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following input values are returned
        self.assertEqual(self.form.hourSpinBox.value(), 0)
        self.assertEqual(self.form.minuteSpinBox.value(), 1)
        self.assertEqual(self.form.secondSpinBox.value(), 1)
        self.assertEqual(self.form.item['service_item'].start_time, 61, 'The start time should stay the same')

        # WHEN displaying the UI, changing the time to 2min 3secs and pressing enter
        self.form.item = {'service_item': mocked_serviceitem}
        with patch('PyQt4.QtGui.QDialog.exec_'):
            self.form.exec_()
        self.form.minuteSpinBox.setValue(2)
        self.form.secondSpinBox.setValue(3)
        ok_widget = self.form.button_box.button(self.form.button_box.Ok)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following values are returned
        self.assertEqual(self.form.hourSpinBox.value(), 0)
        self.assertEqual(self.form.minuteSpinBox.value(), 2)
        self.assertEqual(self.form.secondSpinBox.value(), 3)
        self.assertEqual(self.form.item['service_item'].start_time, 123, 'The start time should have changed')