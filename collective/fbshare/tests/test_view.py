# -*- coding: utf-8 -*-

from StringIO import StringIO

from zope.component import getMultiAdapter

from DateTime import DateTime

from zExceptions import NotFound

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout

from collective.fbshare.testing import FBSHARE_INTEGRATION_TESTING
from collective.fbshare.browser.viewlet import SiteOpenGraphMetaViewlet, OpenGraphMetaViewlet

from base import BaseTestCase

class TestView(BaseTestCase):

    layer = FBSHARE_INTEGRATION_TESTING
    
    def setUp(self):
        self.markRequestWithLayer()
        self.view = getMultiAdapter((self.layer['portal'],
                                     self.layer['request']),
                                     name=u"collective.fbshare.default_image")

    def test_notfoud(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        self.assertRaises(NotFound, self.view)

    def test_image_returned(self):
        portal = self.layer['portal']
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
