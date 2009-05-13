# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import logging

from plumi.app.vocabs  import vocab_set as vocabs

def initialize(context):  
    """Initializer called when used as a Zope 2 product."""
    logger=logging.getLogger('plumi.app')
    logger.info('beginning initialize')

    logger.info('ending  initialize')


def app_installation_tasks(self):
    """Custom Plumi setup code"""
    logger=logging.getLogger('plumi.app')

    logger.info('starting app_installation_tasks. self is %s' %self)

    from Products.CMFCore.utils import getToolByName
    #ATVocabManager setup
    logger.info('Starting ATVocabManager configuration')
    from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
    portal=getToolByName(self,'portal_url').getPortalObject()
    atvm = getToolByName(portal, ATVOCABULARYTOOL)
     
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

    logger.info('starting ATCountryWidget configuration')
