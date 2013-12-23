# -*- coding: utf-8 -*-

from Acquisition import aq_parent, aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.fbshare.interfaces import IFbShareSettings
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter, queryUtility

HAS_LEADIMAGE = True
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
except:
    HAS_LEADIMAGE = False

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


class OpenGraphMetaViewlet(SiteOpenGraphMetaViewlet):
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
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IFbShareSettings, check=False)

        if settings.content_use_own_image:
            # Stolen from collective.opengraph
            img_size = settings.content_image_size
            context = aq_inner(self.context)
            obj_url = context.absolute_url()
            if hasattr(context, 'getField'):
                field = self.context.getField('image')
                if not field and HAS_LEADIMAGE:
                    field = context.getField(IMAGE_FIELD_NAME)
                if field and field.get_size(context) > 0 and img_size:
                    return u'%s/%s_%s' % (obj_url, field.getName(), img_size)
                    return u'%s/%s' % (obj_url, field.getName())
            elif hasattr(context, 'image'):
                # maybe a dexterity content type
                if context.image.size > 0 and img_size:
                    return u'%s/@@images/image/%s' % (obj_url, img_size)

        return SiteOpenGraphMetaViewlet.share_image(self)

    def effective(self):
        return self.context.effective() or None

    def expires(self):
        return self.context.expires() or None

    def modified(self):
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        properties_tool = tools.properties()
        if properties_tool.site_properties.allowAnonymousViewAbout:
            return self.context.modified() or None

    def author(self):
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        properties_tool = tools.properties()
        if properties_tool.site_properties.allowAnonymousViewAbout:
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            if self.context.Creator():
                return "%s/author/%s" % (portal_state.portal_url(), self.context.Creator())
