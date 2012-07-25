# -*- coding: utf-8 -*-

from Acquisition import aq_parent, aq_inner

from zope.component import getMultiAdapter, queryUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.registry.interfaces import IRegistry

from plone.app.layout.viewlets import common

from collective.fbshare.interfaces import IFbShareSettings

class OpenGraphMetaViewlet(common.ViewletBase):
    """Generic OpenGraph share viewlet for contents"""

    index = ViewPageTemplateFile("opengraph_meta.pt")
    site_template = ViewPageTemplateFile("site_opengraph_meta.pt")
    
    def _isPortalDefaultView(self):
        context = self.context
        if ISiteRoot.providedBy(aq_parent(aq_inner(context))):
            putils = getToolByName(context, 'plone_utils')
            return putils.isDefaultPage(context)
        return False
    
    def render(self):
        if self._isPortalDefaultView():
            return self.site_template()
        return self.index()

    def share_image(self):
        """Return URL to the image to be used for sharing
        """
        # BBB: this will change in future, for supporting content related images
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IFbShareSettings, check=False)
        if settings.image_to_share==u'site_logo':
            portal = self.portal_state.portal()
            logoName = portal.restrictedTraverse('base_properties').logoName
            return "%s/%s" % (portal_state.portal_url(), logoName)
        
        share_image_view = getMultiAdapter((portal_state.portal(), self.request),
                                           name=u'collective.fbshare.default_image')
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
        """Return URL to the image to be used for sharing
        """
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IFbShareSettings, check=False)
        if settings.image_to_share==u'site_logo':
            portal = self.portal_state.portal()
            logoName = portal.restrictedTraverse('base_properties').logoName
            return "%s/%s" % (portal_state.portal_url(), logoName)
        
        share_image_view = getMultiAdapter((portal_state.portal(), self.request),
                                           name=u'collective.fbshare.default_image')
        if share_image_view.data():
            return "%s/@@collective.fbshare.default_image" % portal_state.portal_url()
