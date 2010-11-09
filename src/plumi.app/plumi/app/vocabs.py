from zope.i18nmessageid import MessageFactory
_ = MessageFactory("plumi")

vocab_set = {}

taxonomy_sub_folder={'topic':'video_categories','genre':'video_genre','callouts':'submission_categories','countries':''}

vocab_set['video_categories'] = (
         ('poverty', _(u'Poverty / Development')),
         ('indigenous', _(u'Indigenous')),
         ('refugee', _(u'Refugee / Migration')),
         ('health', _(u'Health')),
         ('corporations', _(u'Corporations / Privatisation')),
         ('globalisation', _(u'Globalisation')),
         ('law', _(u'Law / Justice')),
         ('work', _(u'Work')),
         ('consumerism', _(u'Consumerism')),
         ('war', _(u'War / Peace')),
         ('human', _(u'Human Rights')),
         ('disability', _(u'Disability Rights')),
         ('gender', _(u'Gender / Sexuality')),
         ('race', _(u'Race')),
         ('religion', _(u'Religion')),
         ('art', _(u'Art / Culture')),
         ('internet', _(u'Internet')),
         ('media', _(u'Media')),
         ('activism', _(u'Activism')),
         ('politics', _(u'Politics')),
         ('education', _(u'Education')),
         ('biodiversity', _(u'Biodiversity')),
         ('climate', _(u'Climate Change')),
         ('conservation', _(u'Forests / Conservation')),
         ('nuclear', _(u'Nuclear')),
         ('sustainablity', _(u'Sustainability')),
         ('animal', _(u'Animal Rights')),
         ('water', _(u'Water')),
         ('biotech', _(u'Biotech')),
         ('civillib',_(u'Civil Liberties')),
        )
vocab_set['video_genre'] = (
         ('documentary', _(u'Documentary')),
         ('experimental', _(u'Experimental')),
         ('fiction', _(u'Fiction')),
         ('animation', _(u'Animation')),
         ('music', _(u'Music')),
         ('newsreport', _(u'News Report')),
        )
vocab_set['submission_categories'] = (
         ('festival', _(u'Festival')),
         ('screening', _(u'Screening')),
         ('dvd', _(u'DVD')),
         ('production', _(u'Production')),
         ('conference', _(u'Conference')),
         ('workshop', _(u'Workshop')),
         ('crew', _(u'Crew')),
         ('competition', _(u'Competition')),
         ('artprize', _(u'Art Prize')),
         ('exhibition',_(u'Exhibition')),
         ('other', _(u'Other')),
        ) 

