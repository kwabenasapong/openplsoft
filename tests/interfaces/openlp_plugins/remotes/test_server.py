"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os

from unittest import TestCase
from tempfile import mkstemp
from mock import MagicMock
import urllib2
import cherrypy

from BeautifulSoup import BeautifulSoup, NavigableString, Tag

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpserver import HttpServer, fetch_password, sha_password_encrypter
from PyQt4 import QtGui

__default_settings__ = {
    u'remotes/twelve hour': True,
    u'remotes/port': 4316,
    u'remotes/https port': 4317,
    u'remotes/https enabled': False,
    u'remotes/user id': u'openlp',
    u'remotes/password': u'password',
    u'remotes/authentication enabled': False,
    u'remotes/ip address': u'0.0.0.0'
}


class TestRouter(TestCase):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Create the UI
        """
        fd, self.ini_file = mkstemp(u'.ini')
        Settings().set_filename(self.ini_file)
        self.application = QtGui.QApplication.instance()
        Settings().extend_default_settings(__default_settings__)
        self.server = HttpServer()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        os.unlink(self.ini_file)
        self.server.close()

    def start_server(self):
        """
        Common function to start server then mock out the router.  CherryPy crashes if you mock before you start
        """
        self.server.start_server()
        self.server.router = MagicMock()
        self.server.router.process_http_request = process_http_request

    def start_default_server_test(self):
        """
        Test the default server serves the correct initial page
        """
        # GIVEN: A default configuration
        Settings().setValue(u'remotes/authentication enabled', False)
        self.start_server()

        # WHEN: called the route location
        code, page = call_remote_server(u'http://localhost:4316')

        # THEN: default title will be returned
        self.assertEqual(BeautifulSoup(page).title.text, u'OpenLP 2.1 Remote',
            u'The default menu should be returned')

    def start_authenticating_server_test(self):
        """
        Test the default server serves the correctly with authentication
        """
        # GIVEN: A default authorised configuration
        Settings().setValue(u'remotes/authentication enabled', True)
        self.start_server()

        # WHEN: called the route location with no user details
        code, page = call_remote_server(u'http://localhost:4316')

        # THEN: then server will ask for details
        self.assertEqual(code, 401, u'The basic authorisation request should be returned')

        # WHEN: called the route location with user details
        code, page = call_remote_server(u'http://localhost:4316', u'openlp', u'password')

        # THEN: default title will be returned
        self.assertEqual(BeautifulSoup(page).title.text, u'OpenLP 2.1 Remote',
                         u'The default menu should be returned')

        # WHEN: called the route location with incorrect user details
        code, page = call_remote_server(u'http://localhost:4316', u'itwinkle', u'password')

        # THEN: then server will ask for details
        self.assertEqual(code, 401, u'The basic authorisation request should be returned')


def call_remote_server(url, username=None, password=None):
    if username:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
    try:
        page = urllib2.urlopen(url)
        return 0, page.read()
    except urllib2.HTTPError, e:
        return e.code, u''


def process_http_request(url_path, *args):
    cherrypy.response.status = 200
    return None

