# -*- coding: utf-8 -*-

from StringIO import StringIO
from base import BaseTestCase
from collective.fbshare.testing import FBSHARE_INTEGRATION_TESTING
from zExceptions import NotFound
from zope.component import getMultiAdapter


class TestView(BaseTestCase):

    layer = FBSHARE_INTEGRATION_TESTING
    
    def setUp(self):
        self.markRequestWithLayer()
        self.view = getMultiAdapter((self.layer['portal'],
                                     self.layer['request']),
                                     name=u"collective.fbshare.default_image")

    def test_notfoud(self):
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        self.assertRaises(NotFound, self.view)

    def test_image_returned(self):
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        settings = self.getSettings()
        settings.default_image = 'FOO'
        out = StringIO()
        self.view.request.response.stdout = out
        self.view()
        self.assertEquals(out.getvalue(),
                          'Status: 200 OK\r\n'
                          'X-Powered-By: Zope (www.zope.org), Python (www.python.org)\r\n'
                          'Content-Length: 0\r\n'
                          'Content-Type: image/jpg\r\n'
                          'Content-Disposition: inline; filename=collective.fbshare.default_image.jpg\r\n'
                          '\r\nFOO'
                          )
