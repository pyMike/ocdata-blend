# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 14:15:36 2014

@author: Michael Glaude

Purpose: Gets metadata url links from open contracting server and 
         returns a json compatible data structure.
"""

#==============================================================================
import urllib2, urllib
import simplejson
import json

#----------------------------------------------------------------------------
#Examples: of server http or https urls

#Getting all links one page at a time...
#ocds_api_url = 'http://ocds.open-contracting.org/opendatacomparison/api/links'

#Getting all links one page at a time with page size set...for Pagination ...
#ocds_api_url = 'http://ocds.open-contracting.org/opendatacomparison/api/links?page=5&page_size=5'

#Getting only csv links...Sarah configure Django server page size to 500...
#ocds_api_url = 'http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?format=json' 
#----------------------------------------------------------------------------

def get_json_dict(ocds_api_url='http://ocds.open-contracting.org/opendatacomparison/api/links?'):
    """Gets metadata from opendatacomparison server"""        
    try:
    #...get metadata from open contacting url
       req = urllib2.Request(ocds_api_url)
    except Exception, e:
        print "Failed at Request"
        raise(e)
    try:
      opener = urllib2.build_opener()
    except Exception, e:
        print "Failed at opener"
        raise(e)
    try:
       f = opener.open(req)
    except Exception, e:
        print 'Err: '+ str(e)
        print "Host:", req.get_host()
        print "Data:", req.get_data()
        print "failed at open"
        raise(e)
    try:
        json_dict = simplejson.load(f)  #...returns a python dict
        
    except Exception, e:
        print "failed at load"
        raise(e)
    #Future features:
    # - print 'informative message for failing'
    # - handle more specific exceptions
    return json_dict
#----------------------------------------------------------------------------

def get_json_dict_select(num=5, ocds_api_url='http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?'):
    
    ocds_api_url+='page=1&page_size='+str(num) #...   page=1&page_size=5
    json_dict = get_json_dict(ocds_api_url)
    #Future Features:
    # - Investigate what queries the server can handle and implement select options. 
    # - Pagination?
    return json_dict
#----------------------------------------------------------------------------

def print_json_dict(json_dict):
    print json.dumps(json_dict, sort_keys=True, indent=4, separators=(',', ': '))
    #Future Feature:
    # - print 3 results by default
    return
#----------------------------------------------------------------------------

def use_cases():

    #Examples: Use cases...
    json_dict_all      = get_json_dict()  #...gets all links from ocds api.
    
    json_dict_all_csvs = get_json_dict('http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?')
    
    json_dict_5_csvs   = get_json_dict_select()  #...gets up to 5 csv links from ocds api.
    
    json_dict_500_csvs = get_json_dict_select(500) #...gets up to 500 csv links
    
    json_dict_20       = get_json_dict_select(20, 'http://ocds.open-contracting.org/opendatacomparison/api/links?')
    
    print_json_dict(json_dict_5_csvs)
    return
#----------------------------------------------------------------------------

#Future Features:
# - add comments regarding what this function is about.
# - Note: the above code can be put into a class maybe called OCDS_Api
# - unit testing? 
#==============================================================================
