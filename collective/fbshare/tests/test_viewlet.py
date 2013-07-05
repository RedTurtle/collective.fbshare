# -*- coding: utf-8 -*-

import os.path

from zope.component import getMultiAdapter

from DateTime import DateTime

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout

from collective.fbshare.testing import FBSHARE_INTEGRATION_TESTING
from collective.fbshare.browser.viewlet import SiteOpenGraphMetaViewlet, OpenGraphMetaViewlet

from base import BaseTestCase

class TestViewlet(BaseTestCase):

    layer = FBSHARE_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        self.markRequestWithLayer()
        portal.invokeFactory(type_name='Document', id='page', title='A good article')
    
    def test_viewlet_registered_for_site(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        self.assertTrue('<meta property="og:type" content="website" />' in portal())

    def test_viewlet_registered_for_site_default_page(self):
        portal = self.layer['portal']
        request = self.layer['request']
        page = portal.page
        portal.manage_addProperty('default_page', 'page', 'string')
        request.set('ACTUAL_URL', 'http://nohost/plone/page')
        self.assertTrue('<meta property="og:type" content="website" />' in page())

    def test_viewlet_registered_for_content(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/page')
        self.assertTrue('<meta property="og:type" content="article" />' in portal.page())

    def test_pubblication_date(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/page')
        page = portal.page
        self.assertFalse('<meta property="article:published_time"' in page())
        page.edit(effectiveDate=DateTime())
        self.assertTrue('<meta property="article:published_time"' in page())

    def test_expiration_date(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/page')
        page = portal.page
        self.assertFalse('<meta property="article:expiration_time"' in page())
        page.edit(expirationDate=DateTime())
        self.assertTrue('<meta property="article:expiration_time"' in page())

    def test_user_profile_link(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/page')
        page = portal.page
        page.edit(creators=TEST_USER_ID)
        logout()
        self.assertFalse('<meta property="article:author"' in page())
        portal.portal_properties.site_properties.allowAnonymousViewAbout = True
        self.assertTrue('<meta property="article:author" content="http://nohost/plone/author/%s"' % TEST_USER_ID in page())

    def test_image_sitelogo(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        settings = self.getSettings()
        settings.image_to_share = u'site_logo'
        self.assertTrue('<meta property="og:image" content="http://nohost/plone/logo.png"' in portal())

    def test_image_noimage(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        settings = self.getSettings()
        settings.image_to_share = u'custom_image'
        self.assertFalse('<meta property="og:image"' in portal())

    def test_image_customimage(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone')
        settings = self.getSettings()
        settings.image_to_share = u'custom_image'
        settings.default_image = 'FOO'
        self.assertTrue('<meta property="og:image" content="http://nohost/plone/@@collective.fbshare.default_image"' in portal())


class TestViewletOnContent(BaseTestCase):

    layer = FBSHARE_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        self.markRequestWithLayer()
        portal.invokeFactory(type_name='News Item', id='news', title='A site news')
        portal.news.edit(image=open(os.path.join(os.path.dirname(__file__), 'plone-icon.png')))
        portal.invokeFactory(type_name='Document', id='page', title='A good article')
        portal.page.edit(leadImage=open(os.path.join(os.path.dirname(__file__), 'plone-icon.png')))

    def test_content_image_disabled(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        settings = self.getSettings()
        settings.content_use_own_image = False
        self.assertFalse('<meta property="og:image"' in portal.news())

    def test_content_image_simple(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        settings = self.getSettings()
        settings.content_use_own_image = True
        self.assertTrue('<meta property="og:image" content="http://nohost/plone/news/image_mini"' in portal.news())

    def test_content_image_custom_resize(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        settings = self.getSettings()
        settings.content_use_own_image = True
        settings.content_image_size = 'icon'
        self.assertTrue('<meta property="og:image" content="http://nohost/plone/news/image_icon"' in portal.news())
        settings.content_image_size = ''
        self.assertTrue('<meta property="og:image" content="http://nohost/plone/news/image"' in portal.news())

    def test_contentleadimage_support(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/page')
        settings = self.getSettings()
        settings.content_use_own_image = True
        self.assertTrue('<meta property="og:image" content="http://nohost/plone/page/leadImage_mini"' in portal.page())

    def test_default_folder_page(self):
        portal = self.layer['portal']
        request = self.layer['request']
        portal.invokeFactory(type_name='Folder', id='folder', title='A folder')
        portal.folder.invokeFactory(type_name='Document', id='page', title='Home')
        portal.folder.setDefaultPage(portal.folder.page.getId())
        #portal.folder.setLayout(portal.folder.page.getId())
        request.set('ACTUAL_URL', 'http://nohost/plone/folder')
        request.set('URL', 'http://nohost/plone/folder')
        home = portal.folder.restrictedTraverse('page')
        self.assertTrue('<meta property="og:title" content="Home"' in home())
        self.assertTrue('<meta property="og:url" content="http://nohost/plone/folder"' in home())
