# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import logging

from plumi.app.vocabs  import vocab_set as vocabs
from plumi.app import config

def initialize(context):  
    """Initializer called when used as a Zope 2 product."""
    logger=logging.getLogger('plumi.app')
    logger.info('beginning initialize')

    logger.info('ending  initialize')


def app_installation_tasks(self):
    """Custom Plumi setup code"""
    logger=logging.getLogger('plumi.app')

    logger.info('starting app_installation_tasks. self is %s' %self)
    #imports from old style plone 'Products' namespace
    from Products.CMFCore.utils import getToolByName
    from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
    from Products.ATCountryWidget.CountryTool import CountryUtils, Country

    #ATVocabManager setup
    logger.info('Starting ATVocabManager configuration')
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

    #ATCountryWidget setup
    #reset the country tool
    countrytool = getToolByName(self, CountryUtils.id)
    #common code
    countrytool.manage_countries_reset()
        
    if config.SE_ASIA_COUNTRIES:
        logger.info('starting custom se-asia countries ATCountryWidget configuration')
        #Add countries missing from the standard installs
        # 
        countrytool.manage_countries_addCountry('WP','West Papua')
        #XXX this is a state of America, not a country - but thats just politics!!
        countrytool.manage_countries_addCountry('HA','Hawaii')
        countrytool.manage_countries_addCountry('BU','Bougainville')
       
        #update three more pre-exisiting countries 
        #change Myanmar to Burma
        #Lao Peoples blah blah to just Laos
        #Viet Nam to Vietnam
        countries = countrytool._country_list
        countries[countries.index(Country('MM'))].name="Burma"
        countries[countries.index(Country('LA'))].name="Laos"
        countries[countries.index(Country('VN'))].name="Vietnam"
        countries[countries.index(Country('NZ'))].name="NZ-Aotearoa"
      
        #add our areas
        countrytool.manage_countries_addArea('South East Asia')
        countrytool.manage_countries_addCountryToArea('South East Asia', ['SG','TH','VN','ID','PH','LA','MY','KH','BN','MM','HK','MO'])
        countrytool.manage_countries_sortArea('South East Asia')
     
        countrytool.manage_countries_addArea('Oceania')
        countrytool.manage_countries_addCountryToArea('Oceania', ['AU','NZ','PG','TL','WP','FJ','SB','HA','NC','VU','WS','BU'    ,'NR','TO','TV','GU','KI','FM','PF','MH','MP','PW','PN','TK','AQ',])
        countrytool.manage_countries_sortArea('Oceania')

    logger.info('starting taxonomy hierarchy setup')
    

