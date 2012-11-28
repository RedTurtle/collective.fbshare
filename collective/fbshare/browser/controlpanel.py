# -*- coding: utf-8 -*-

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from z3c.form import button

from plone.app.registry.browser import controlpanel

from collective.fbshare.interfaces import IFbShareSettings
from collective.fbshare import messageFactory as _


class FbSharingSettingsControlPanelEditForm(controlpanel.RegistryEditForm):
    """Open graph settings form.
    """
    schema = IFbShareSettings
    id = "FbSharingSettingsEditForm"
    label = _(u"Open Graph sharing settings")
    description = _(u"help_fbsharing_settings_editform",
                    default=u"Manage general site configuration for Open Graph")

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@opengraph-sharing-settings")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class FbSharingSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Open Graph settings control panel.
    """
    form = FbSharingSettingsControlPanelEditForm
    #index = ViewPageTemplateFile('controlpanel.pt')
