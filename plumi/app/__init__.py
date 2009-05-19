# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import logging

from plumi.app.vocabs  import vocab_set as vocabs
from plumi.app import config
from plumi.app.config import TOPLEVEL_TAXONOMY_FOLDER , GENRE_FOLDER, CATEGORIES_FOLDER, COUNTRIES_FOLDER, SUBMISSIONS_FOLDER

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

    #
    #
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

    #
    #
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

    #
    #
    # Taxonomy - topics    
    logger.info('starting taxonomy hierarchy setup')
    
    # we start in 'taxonomy', and shld already have sub-folders constructed
    #to hold the topics objects (smart folders), via generic setup XML
    taxonomy_fldr = getattr(self,TOPLEVEL_TAXONOMY_FOLDER,None) 
    if taxonomy_fldr is None:
        logger.error('No taxonomy folder!')
        return
    #genre
    genre_fldr = getattr(taxonomy_fldr, GENRE_FOLDER,None)
    if genre_fldr is None:
        logger.error('No genre folder!')
        return

    #description string for new smart folders
    topic_description_string = 'Channel for %s on ' + '%s' % self.Title()
    for vocab in vocabs['video_genre']:
        new_smart_fldr_id = vocab[0]
        try:
            # Remove existing instance if there is one
            genre_fldr.manage_delObjects([new_smart_fldr_id])
        except:
            pass
        #make the new SmartFolder
        genre_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=vocab[1], description=topic_description_string % vocab[1])
        fldr = getattr(genre_fldr,new_smart_fldr_id)
         
        # Filter results to ATEngageVideo
        type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
        #Have to use the name of the Title of the Type you want to filter.
        type_criterion.setValue("Plumi Video")
         
        # Filter results to this individual genre
        type_criterion = fldr.addCriterion('getGenre', 'ATSimpleStringCriterion' )
        #match against the ID of the vocab term. see getGenre in content types 
        type_criterion.setValue(vocab[0])
        ## add criteria for showing only published videos
        state_crit = fldr.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_crit.setValue('published')
        
        #XXX used to have a custom getFirstPublishedTransitionTime 
        #sort on reverse date order, using the first published time transition
        sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
        sort_crit.setReversed(True)

        #XXX make the folder published

    #XXX categories aka topics
    categ_fldr = getattr(taxonomy_fldr, CATEGORIES_FOLDER,None)
    if categ_fldr is None:
        logger.error('No categories folder!')
        return

    for vocab in vocabs['video_categories']:
        new_smart_fldr_id = vocab[0]
        try:
            # Remove existing instance if there is one
            categ_fldr.manage_delObjects([new_smart_fldr_id])
        except:
            pass
        #make the new SmartFolder
        categ_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=vocab[1], description=topic_description_string % vocab[1])
        fldr = getattr(categ_fldr,new_smart_fldr_id)

        # Filter results to ATEngageVideo
        type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
        type_criterion.setValue("Plumi Video")
        # Filter results to this individual category
        type_criterion = fldr.addCriterion('getCategories', 'ATListCriterion' )
        #match against the ID of the vocab term. see getCategories in engage.py (ATEngageVideo object)
        type_criterion.setValue(vocab[0])
        #match if any vocab term is present in the video's selected categories
        type_criterion.setOperator('or')
        ## add criteria for showing only published videos
        state_crit = fldr.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_crit.setValue('published')
        #sort on reverse date order
        #XXX old getfirstpublishedtransition time 
        sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
        sort_crit.setReversed(True)

        #XXX make the folder published.

    #XXX call submission categories
    #XXX countries


