import transaction
import logging
from Products.CMFCore.utils import getToolByName
from plumi.app.install import app_installation_tasks

#install plumi.skin last
PRODUCT_DEPENDENCIES = ('LinguaPlone','plone.contentratings','vaporisation','ATVocabularyManager','ATCountryWidget','ContentLicensing','PressRoom','Marshall','collective.flowplayer','plumi.content','plone.app.blob', 'collective.contentlicensing', 'plone.app.imaging', 'plone.app.discussion', 'plumi.migration', 'json_migrator', 'collective.plonebookmarklets', 'quintagroup.plonecomments', 'plone.app.jquerytools', 'plumi.skin')

# These are deprecated products, and will be removed in plumi 0.5.x
PRODUCT_DEPENDENCIES_LEGACY=('qPloneComments','qRSS2Syndication',)
                        
EXTENSION_PROFILES = ('plumi.app:default',)

def install(self, reinstall=False):
    """Install a set of products (which themselves may either use Install.py
    or GenericSetup extension profiles for their configuration) and then
    install a set of extension profiles.
    
    One of the extension profiles we install is that of this product. This
    works because an Install.py installation script (such as this one) takes
    precedence over extension profiles for the same product in 
    portal_quickinstaller. 
    
    We do this because it is not possible to install other products during
    the execution of an extension profile (i.e. we cannot do this during
    the importVarious step for this profile).
    """
    logger = logging.getLogger('plumi.app')
    logger.info('starting install')
    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')
    logger.info('starting product dependencies')
    for product in PRODUCT_DEPENDENCIES:
        if reinstall and portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.reinstallProducts([product])
            transaction.savepoint()
        elif not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()
    logger.info('starting dependencies legacy')
    for product in PRODUCT_DEPENDENCIES_LEGACY:
        if reinstall and portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.reinstallProducts([product])
            transaction.savepoint()
        elif not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()
    logger.info('starting extension profiles')
    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()
    #run custom setup code.
    logger.info('starting custom setup code')
    app_installation_tasks(self)
    logger.info('end install')

