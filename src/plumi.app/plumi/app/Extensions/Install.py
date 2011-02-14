import transaction
import logging
from Products.CMFCore.utils import getToolByName
from plumi.app.install import app_installation_tasks

def install(self, reinstall=False):
    logger = logging.getLogger('plumi.app')
    logger.info('starting install')
    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')

    # install collective.transcode.star seperately to avoid utility removal on reinstall
    if not portal_quickinstaller.isProductInstalled('collective.transcode.star'):
        portal_quickinstaller.installProduct('collective.transcode.star')

    logger.info('starting extension profiles')

    portal_setup.runAllImportStepsFromProfile('profile-plumi.app:default', purge_old=False)
    portal_quickinstaller.notifyInstalled('plumi.app')
    transaction.savepoint()

    #run custom setup code.
    logger.info('starting custom setup code')
    app_installation_tasks(self, reinstall)
    logger.info('end install')

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-plumi.app:uninstall')
    return "Ran all uninstall steps."

