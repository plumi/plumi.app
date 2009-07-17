
import logging
from zope.app.component.interfaces import ISite
from plone.app.controlpanel.security import ISecuritySchema

from plumi.app.vocabs  import vocab_set as vocabs
from plumi.app.config import TOPLEVEL_TAXONOMY_FOLDER , GENRE_FOLDER, CATEGORIES_FOLDER, COUNTRIES_FOLDER, SUBMISSIONS_FOLDER, SE_ASIA_COUNTRIES, LANGUAGES

#imports from old style plone 'Products' namespace
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATCountryWidget.CountryTool import CountryUtils, Country
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.component import enableSite

from AccessControl import allow_module
allow_module('plumi.app.member_area.py')

#i18n
from zope import i18n
_ = i18n.MessageFactory("plumi.app")


def initialize(context):  
    """Initializer called when used as a Zope 2 product."""
    logger=logging.getLogger('plumi.app')
    logger.debug('beginning initialize')
    # this is called at Zope instance startup, ie not installation.
    logger.debug('ending  initialize')

def publishObject(wftool,obj):
    logger=logging.getLogger('plumi.app')
    try:
        logger.info('publishing %s ' % obj)
        wftool.doActionFor(obj,action='publish')
    except WorkflowException:
        logger.error('caught workflow exception!') 
        pass

def app_installation_tasks(self):
    """Custom Plumi setup code"""
    logger=logging.getLogger('plumi.app')

    logger.info('starting app_installation_tasks. self is %s' %self)
    portal=getToolByName(self,'portal_url').getPortalObject()
    if not ISite.providedBy(portal):
        enableSite(portal)

    # modify site properties

    # XXX turn on RSS site wide
    # XXX turn it on in default_member_content
    # XXX 

    # XXX doesnt work here?! - we could do this in profiles/default/properties.xml, however, we could make some programmatic checks here, if needed.
    portal.manage_changeProperties(**{"layout" : 'featured_videos_homepage'})

    #site security setup!
    secSchema = ISecuritySchema(portal)
    secSchema.set_enable_self_reg(True)
    secSchema.set_enable_user_pwd_choice(True)
    secSchema.set_enable_user_folders(True)

    #setup languages for the site - this is portal languages, not linguaplone
    lang = getToolByName(self, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('en-au')
    lang.display_flags = 1
    lang.force_language_urls = 1
    lang.use_cookie_negotiation = 1
    lang.use_content_negotiation = 1
    lang.use_path_negotiation = 1
    lang.use_request_negotiation = 1

    #
    #
    #ATVocabManager setup
    logger.info('Starting ATVocabManager configuration')
    atvm = getToolByName(portal, ATVOCABULARYTOOL)
    wftool = getToolByName(self,'portal_workflow')
     
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

    #
    #
    #ATCountryWidget setup
    #reset the country tool
    countrytool = getToolByName(self, CountryUtils.id)
    #common code
    countrytool.manage_countries_reset()
        
    if SE_ASIA_COUNTRIES:
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
    # Collections for display 
    # latestvideos / featured-videos / news-and-events
    #

    #The front page, @@featured_videos_homepage, contains
    #links to 'featured-videos' which is a smart folder containing
    #all the videos with keyword 'featured' and 'lastestvideos'
    #which is a smart folder of the latest videos. this method will
    #simply install them.

    # Items to deploy on install.
    items = (dict(id      = 'featured-videos',
                  title   = _(u'Featured Videos'),
                  desc    = _(u'Videos featured by the editorial team.'),
                  layout  = "video_listing_view",
                  exclude = True),

             dict(id      = 'latestvideos',
                  title   = _(u'Latest Videos'),
                  desc    = _(u'Latest videos contributed by the users.'),
                  layout  = "video_listing_view",
                  exclude = False),

	     dict(id      = 'news_and_events',
                  title   = _(u'News and Events'),
                  desc    = _(u'Latest news and events on the site.'),
                  layout  = "folder_summary_view",
                  exclude = True),
		

		)

    # Items creation
    for item in items:
        try:
            self.manage_delObjects([item['id']])
        except:
            ## This is nasty to silence it all
            pass

        # We create the element
        self.invokeFactory('Topic',
                           id = item['id'],
                           title = item['title'],
                           description = item['desc'].translate({}))

        # We change its ownership and wf status
        fv = getattr(self, item['id'])
        publishObject(wftool, fv)

        # Filter results to ATEngageVideo
        # Have to use the name of the Title (and ATEngageVideo will be re-named by configATEngageVideo to Video!)
        # this will actually use ALL objects with title 'Video', which means atm, ATEngageVideo and ATVideo
        type_criterion = fv.addCriterion('Type', 'ATPortalTypeCriterion')
	if item['id'] is 'news_and_events':
		type_criterion.setValue( ("News Item","Event") )
	else:
		type_criterion.setValue("Plumi Video")

        # Filter results to this 'keyword' field, the kw being 'featured'
        if item['id'] is 'featured-videos':
            type_criterion = fv.addCriterion('Subject', 'ATSimpleStringCriterion')
            type_criterion.setValue('featured')

        # Sort on reverse publication date order
	# XXX port functionality
        #sort_crit = fv.addCriterion('getFirstPublishedTransitionTime',"ATSortCriterion")
	sort_crit = fv.addCriterion('created',"ATSortCriterion")
        sort_crit.setReversed(True)

        ## add criteria for showing only published videos
        state_crit = fv.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_crit.setValue('published')

        if item['exclude'] is True:
            fv.setExcludeFromNav(True)

        if item['layout'] is not None:
            fv.setLayout(item['layout'])

        fv.reindexObject()


    #
    #
    # Taxonomy - smart folder hierarchy setup - genres/categories/countries/ for videos
    # 	we automatically [RE]create collections , hierarchically, for all available vocabulary items
    #
    logger.info('starting taxonomy hierarchy setup')
    
    # we start in 'taxonomy', and shld already have sub-folders constructed
    #to hold the topics objects (smart folders), via generic setup XML
    taxonomy_fldr = getattr(self,TOPLEVEL_TAXONOMY_FOLDER,None) 
    if taxonomy_fldr is None:
        logger.error('No taxonomy folder!')
        return
    publishObject(wftool,taxonomy_fldr)

    #
    # 1 of 4: video genre
    #
    genre_fldr = getattr(taxonomy_fldr, GENRE_FOLDER,None)
    if genre_fldr is None:
        logger.error('No genre folder!')
        return
    publishObject(wftool,genre_fldr)
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
         
        # Filter results to Plumi Video
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

        #make the folder published
        publishObject(wftool,fldr)

    #
    # 2 of 4: video categories aka topic
    #
    categ_fldr = getattr(taxonomy_fldr, CATEGORIES_FOLDER,None)
    if categ_fldr is None:
        logger.error('No categories folder!')
        return
    publishObject(wftool,categ_fldr)

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

        # Filter results to Plumi Video
        type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
        type_criterion.setValue("Plumi Video")
        # Filter results to this individual category
        type_criterion = fldr.addCriterion('getCategories', 'ATListCriterion' )
        #match against the ID of the vocab term. see getCategories in content objects
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

        #make the folder published.
        publishObject(wftool,fldr)


    #
    # 3 of 4: video countries
    #
   
    #Countries
    #get the countries from the countrytool!
    # nb: this means that the setup method for the countries should be called BEFORE
    # this one

    countrytool = getToolByName(self,CountryUtils.id)
    cdict = list()
    countries_fldr = getattr(taxonomy_fldr,COUNTRIES_FOLDER,None)
    if countries_fldr is None:
            logger.error('Countries folder is missing!')
            return
    publishObject(wftool,countries_fldr)

    for area in countrytool._area_list:
        for country in area.countries:
            cdict.append([country.isocc,country.name])

    for country in cdict:
        new_smart_fldr_id = country[0]
        try:
            # Remove existing instance if there is one
            countries_fldr.manage_delObjects([new_smart_fldr_id])
        except:
            pass
        #make the new SmartFolder
        countries_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=country[1],description=topic_description_string % country[1]) 
        fldr = getattr(countries_fldr,new_smart_fldr_id)

        # Filter results to  Plumi Video
        type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
        type_criterion.setValue("Plumi Video")

        # Filter results to this individual category
        type_criterion = fldr.addCriterion('getCountries', 'ATListCriterion' )
        #
        #match against the ID of the vocab term. see getCategories in content objects
        type_criterion.setValue(country[0])
        #match if any vocab term is present in the video's selected categories
        type_criterion.setOperator('or')
        ## add criteria for showing only published videos
        state_crit = fldr.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_crit.setValue('published')
        #sort on reverse date order
        sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
        sort_crit.setReversed(True)
        #publish folder
        publishObject(wftool,fldr)

    #
    #4 of 4 : CallOut submission categories
    #
    topic_description_string = "CallOuts for Topic - %s "
    submissions_fldr = getattr(taxonomy_fldr,SUBMISSIONS_FOLDER,None)
    if submissions_fldr is None:
            logger.error('callout submissions folder is missing!')
            return
    publishObject(wftool,submissions_fldr)
    for submission_categ in vocabs['submission_categories']:
        new_smart_fldr_id = submission_categ[0]
        try:
            # Remove existing instance if there is one
            submissions_fldr.manage_delObjects([new_smart_fldr_id])
        except:
            pass

        #make the new SmartFolder
        submissions_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=submission_categ[1], description=topic_description_string % submission_categ[1])
        fldr = getattr(submissions_fldr,new_smart_fldr_id)
        # Filter results to Callouts
        type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
        #the title of the type, not the class name, or portal_type 
        type_criterion.setValue("Plumi Call Out")

        # Filter results to this individual category
        type_criterion = fldr.addCriterion('getSubmissionCategories', 'ATListCriterion' )
        #
        #match against the ID of the vocab term. see getCategories in callout.py (Callout object)
        type_criterion.setValue(submission_categ[0])
        #match if any vocab term is present in the video's selected categories
        type_criterion.setOperator('or')

        ## add criteria for showing only published videos
        state_crit = fldr.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_crit.setValue('published')
        #sort on reverse date order
        sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
        sort_crit.setReversed(True)
        #publish the folder
        publishObject(wftool,fldr)

