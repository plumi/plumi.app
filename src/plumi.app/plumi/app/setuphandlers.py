import logging
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.security import ISecuritySchema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from plumi.app.vocabs  import vocab_set as vocabs
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL

def setupHome(portal, out):
    """
        set default homepage 
    """
    portal.setLayout('featured_videos_homepage')

def setupSiteSecurity(portal, out):
    """
        site security setup!
    """
    secSchema = ISecuritySchema(portal)
    secSchema.set_enable_self_reg(True)
    secSchema.set_enable_user_pwd_choice(True)
    secSchema.set_enable_user_folders(True)

def setupTranscoding(portal, logger):
    """
        configure PlumiVideo as transcodable
    """
    registry = getUtility(IRegistry)
    registry['collective.transcode.star.interfaces.ITranscodeSettings.portal_types'] = (u'PlumiVideo:video_file',)

def setupSeeding(portal, logger):
    """
        configure PlumiVideo as seedable
    """
    registry = getUtility(IRegistry)
    registry['collective.seeder.interfaces.ISeederSettings.portal_types'] = (u'PlumiVideo:video_file',)

def setupVocabs(portal, logger):
    #
    #ATVocabManager setup
    #
    logger.info('Starting ATVocabManager configuration ')
    atvm = getToolByName(portal, ATVOCABULARYTOOL)
    wftool = getToolByName(portal,'portal_workflow')

    for vkey in vocabs.keys():
        # create vocabulary if it doesnt exist:
        vocabname = vkey
        if atvm.getVocabularyByName(vocabname):
            atvm.manage_delObjects(vocabname)
        logger.debug("adding vocabulary %s" % vocabname)
        atvm.invokeFactory('SimpleVocabulary', vocabname)

        vocab = atvm[vocabname]

        #delete the 'default' item
        if hasattr(vocab, 'default'):
            vocab.manage_delObjects(['default'])

        for (ikey, value) in vocabs [vkey]:
            if not hasattr(vocab, ikey):
                vocab.invokeFactory('SimpleVocabularyTerm', ikey)
                logger.debug("adding vocabulary item %s %s" % (ikey,value))
                vocab[ikey].setTitle(value)

        #reindex
        vocab.reindexObject()

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('plumi.app_various.txt') is None:
        return

    portal = context.getSite()
    logger = logging.getLogger('plumi.app')
    #setupRSS(portal, logger)
    setupHome(portal, logger)
    setupSiteSecurity(portal, logger)
    setupTranscoding(portal, logger)
    setupSeeding(portal, logger)
    setupVocabs(portal, logger)

def uninstall(context):
    if context.readDataFile('plumi.app_uninstall.txt') is None:
        return

