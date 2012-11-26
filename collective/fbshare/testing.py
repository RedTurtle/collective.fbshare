# -*- coding: utf-8 -*-

from zope.configuration import xmlconfig

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID

class FbShare(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.fbshare
        import collective.contentleadimage
        xmlconfig.file('configure.zcml',
                       collective.fbshare,
                       context=configurationContext)
        xmlconfig.file('configure.zcml',
                       collective.contentleadimage,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.fbshare:default')
        applyProfile(portal, 'collective.contentleadimage:default')
        setRoles(portal, TEST_USER_ID, ['Member', 'Manager'])


FBSHARE_FIXTURE = FbShare()
FBSHARE_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(FBSHARE_FIXTURE, ),
                       name="FbShare:Integration")
FBSHARE_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(FBSHARE_FIXTURE, ),
                      name="FbShare:Functional")

