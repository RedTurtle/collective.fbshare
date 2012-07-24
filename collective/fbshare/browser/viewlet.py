# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class OpenGraphMetaViewlet(common.ViewletBase):
    """Generic OpenGraph share viewlet for contents"""

    index = ViewPageTemplateFile("opengraph_meta.pt")

    def share_image(self):
        """Return URL to the image to be used for sharing
        """
        # BBB: this will change in future, for supporting content related images
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        share_image_view = getMultiAdapter((portal_state.portal(), self.request), name=u'collective.fbshare.default_image')
        if share_image_view.data():
            return "%s/@@collective.fbshare.default_image" % portal_state.portal_url()

    def effective(self):
        context = self.context
        effectiveDate = context.getField('effectiveDate').get(context)
        return effectiveDate or None

    def expires(self):
        context = self.context
        expirationDate = context.getField('expirationDate').get(context)
        return expirationDate or None

    def author(self):
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        properties_tool = tools.properties()
        if properties_tool.site_properties.allowAnonymousViewAbout:
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            if self.context.Creator():
                return "%s/author/%s" % (portal_state.portal_url(), self.context.Creator())

class SiteOpenGraphMetaViewlet(common.ViewletBase):
    """OpenGraph share viewlet for site root"""
    
    index = ViewPageTemplateFile("site_opengraph_meta.pt")
    
    def share_image(self):
        """Return URL to the image to be used for sharing"""
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        share_image_view = getMultiAdapter((self.context, self.request), name=u'collective.fbshare.default_image')
        if share_image_view.data():
            return "%s/@@collective.fbshare.default_image" % portal_state.portal_url()
