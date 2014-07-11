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
    return json_dict
#----------------------------------------------------------------------------

def get_json_dict_select(num=5, ocds_api_url='http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?'):
    """Gets the specified number on links from the server"""
    ocds_api_url+='page=1&page_size='+str(num) #...page=1&page_size=5
    json_dict = get_json_dict(ocds_api_url)
    return json_dict
#----------------------------------------------------------------------------

def print_json_dict(json_dict):
    """Provides simple interface to printing json_dict data structure"""
    print json.dumps(json_dict, sort_keys=True, indent=4, separators=(',', ': '))
    return
#==============================================================================  

def get_links(json_dict, key='', value='',prn=True): #, key='format', value='CSV'):
    """Warning: Please Check your key value exists before calling.
    if key='' (the default) then all links are return.""" 
    results = json_dict["results"]
    print len(results)
    links = []
    for (itemNum, item) in enumerate(results):
       if (key=='') or (item[key] == value):
           if prn:
               print item['link']
           links.append(item['link'])
    if prn:
        print "num of links = ",len(links)
    return links
#-------------------------------------------------------------------------

def get_all_links(json_dict):
    """Returns all url links"""
    return get_links(json_dict)
#-------------------------------------------------------------------------

def get_all_csv_links(json_dict):
    """Returns all url links that have CSV file format"""
    return get_links(json_dict,'format','CSV')
#==============================================================================   

#==============================================================================

def get_filename_from_url(url):
    """Rudamentary parsing of URL into a list and assumming last element is the filename """
    filename = url.split('/')[-1]
    return filename 
#------------------------------------------------------------------------------

def get_file_info(link, prn=True):
    """Returns useful info regarding file to download i.e. Metadata
    Getting metadata about one file from remote servers...
    Purpose:  to get filename, filesize, URL & and http Instance info...
    """
    FILE_SIZE_FAILED = '999999999999'  

    the_file = urllib2.urlopen( link )
    #if chk_the_file  #xxx...implement later.
    httpInstance = the_file.info()  #...can get length of file. 

    if prn:    
        print '\n--------------------httpInstance----------------------------------------------'
        print httpInstance
        print '----------------------httpInstance dictionary--------------------------------------------------------'
        print_json_dict(httpInstance.dict)
        print '----------------------httpInstance keys--------------------------------------------------------'
        print_json_dict(httpInstance.keys())
        print '----------------------httpInstance values--------------------------------------------------------'
        print_json_dict(httpInstance.values())
        print '------------------------------------------------------------------------------'

    if 'Strict-Transport-Security' in httpInstance.keys():
        fileSizeStr = httpInstance['Strict-Transport-Security'].split('max-age=')[1]  #xxx ...fails ofen why?
    elif 'content-length' in httpInstance.dict:
        fileSizeStr = httpInstance.dict['content-length']
    else:
        fileSizeStr = FILE_SIZE_FAILED   #...indicates failed extraction.
    fileSize = int(fileSizeStr)
    url = the_file.url
    #if chk_url(url):  #xxx ...implement later.
    filename = get_filename_from_url(url)
    #if chk_filename  #xxx ...implement later.
    
    the_file.close()
    return httpInstance.dict,(fileSize, url, filename )  #...should return struct, filename etc..
#------------------------------------------------------------------------------

def get_all_files_info(json_dict):
    """Gets info on all files i.e. extend/augment json_dict and return
    augmented data structure to include added info/metadata about all files."""
    results = json_dict['results']
    for i,res in enumerate(results):
        http_dict, file_info =  get_file_info(res['link'])
        file_size, url, filename = file_info
        #add http_dict field
        res['http_dict'] = http_dict
        res['file_size'] = file_size
        res['url'] = url
        res['filename'] = filename
        results[i]= res
    json_dict['results']=results
    return json_dict

#==============================================================================
#==============================================================================
def save_file(url, simulate=False):
   """Downloads and Saves one file:"""
   #Notes to self:
   #getting the file contents...    
   the_file = urllib2.urlopen(url)
   url_redirect = the_file.url  #...note1: redirect from Django, Note2: same as the_file.geturl()

   file_info_dict,(file_size, url_redirect, file_name ) = get_file_info(url,False)
   
   #Download file in any format..
   with open(file_name,'wb') as f:
       print "----------------------------------------------------------------------------------------"
       print "From: Django url......:", url
       print "From: Redirect url....:", url_redirect
       print "To: local directory...:", os.getcwd()
       print "To: Filename..........:", file_name 
       print "File size.............:", file_size, 'bytes'
       print "Estimated download time at 1 megabit rate is", (file_size*8.0/1000000)/60, 'minutes'
       print "----------------------------------------------------------------------------------------"
       if not(simulate):
           f.write(the_file.read()) #...xxx add a path here to write files.
       else:
           print "Simulation in progress: creating empty file in current directory"
       f.close()
   the_file.close()
   return 
#-----------------------------------------------------------------------------    
def save_files(links, simulate=False):
    """Downloads and saves files to local drive at current directory."""
    for link in links:
        save_file(link, simulate)
    return
#-----------------------------------------------------------------------------    

def save_csvs_by_dataset(value="Contracts Finder - All Notices",num=5, simulate=False):
    """Downloads and saves a specified number of CSV files selected on 
    a specified dataset value.""" 
    json_dict_all_csvs = get_json_dict('http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?')

    links = get_links(json_dict_all_csvs, 'dataset', value ) #...selecting links

    save_files(links, simulate)
    return 
#-----------------------------------------------------------------------------    

def save_csvs_limited_by_size(num=5, size=1000):
    """Will implement next, similar to save_csvs_by_dataset"""
    pass
    #Future Features:
    # - get some rest frist.
    return    
#-----------------------------------------------------------------------------    

def use_cases():
    """Provide user some example use cases"""
    FILE_SIZE_FAILED = '999999999999'
    simulate = True

    #Examples: Use cases...
    #json_dict_all      = get_json_dict()  #...gets all links from ocds api.
    
    #json_dict_all_csvs = get_json_dict('http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?')
    
    json_dict_5_csvs   = get_json_dict_select()  #...gets up to 5 csv links from ocds api.
    
    #json_dict_500_csvs = get_json_dict_select(500) #...gets up to 500 csv links
    
    #json_dict_20       = get_json_dict_select(20, 'http://ocds.open-contracting.org/opendatacomparison/api/links?')
    
    json_dict = json_dict_5_csvs
    #==========================================================================
   
    links1 = get_links(json_dict)  #...gets all links by default 
    links2 = get_links(json_dict, 'format', 'CSV')   #...gets all CSVs
    links3 = get_links(json_dict, 'dataset', 'Contracts Finder - All Notices')

    links4 = get_all_links(json_dict)     #...same as link1
    links5 = get_all_csv_links(json_dict) #...same as link2.
    #==========================================================================
    #gathering more informatinon regarding one file...
    http_info, file_info = get_file_info(links2[0])  #...gets augmented info regarding one file
    #getting information of all files and augmenting json_dict...
    json_dict_augmented = get_all_files_info(json_dict)  #...metadata all collected in one place.
    #==========================================================================
    #Now one can search on augmented metadata...not the best use case example but...
    links6 = get_links(json_dict_augmented, 'file_size', int(FILE_SIZE_FAILED)) #...lists all failed attemps
    #==========================================================================
    # Warning: this section downloads files into your current directory
    # you may want to simulate the download first but be advised that
    # empty files will be written to your current directory.
    if False: #Example: of a specific save function 
        save_csvs_by_dataset()  #...by default saves up to 5 csv files with dataset="Contracts Finder - All Notices"
        save_csvs_by_dataset("Contracts Finder - All Notices")  #...does the same as above
        save_csvs_by_dataset("Buyandsell.gc.ca - Tenders Data", 10, simulate==True) #... simulate saving up to 10 with dataset="Bsyandsell..."
        save_csvs_by_dataset("Buyandsell.gc.ca - Tenders Data", 10)                 #...  saving up to 10 with dataset="Bsyandsell..."
    
    if True: #Example: of a general case: make any selection from source server...
        json_dict   = get_json_dict()  #...gets all links from ocds api of any format.
        #OR...
        json_dict   = get_json_dict_select(500)  #...gets up to 500 csv links from ocds api.
        
        #Using the general get_links function:  make a second selection from json_dict metadata...
        links = get_links(json_dict, 'dataset', "Contract Finder - All notices" ) 
        links = get_links(json_dict, 'format', "CSV" ) 
    
        save_files(links[0:5], simulate==True) #... links are urls and True means simulate.
    
    return
#----------------------------------------------------------------------------

#==============================================================================

#use_cases()