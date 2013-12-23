# -*- coding: utf-8 -*-

from collective.fbshare.interfaces import IFbShareSettings
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.component import queryUtility, getMultiAdapter


class ShareDefaultImage(BrowserView):
    """Return a bytestream with the default image"""
    
    def data(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IFbShareSettings, check=False)
        return settings.default_image
    
    def __call__(self, *args, **kwargs):
        bytes = self.data()
        if bytes:
            response = self.request.response
            response.setHeader('Content-Type','image/jpg')
            response.setHeader('Content-Disposition', 'inline; filename=collective.fbshare.default_image.jpg')
            response.write(bytes)
            return
        # no data? no image
        raise NotFound()