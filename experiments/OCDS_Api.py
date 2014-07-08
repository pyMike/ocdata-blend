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

FILE_SIZE_FAILED = 999999999999

#----------------------------------------------------------------------------
#Examples: of server http or https urls

#Getting all links one page at a time...
#ocds_api_url = 'http://ocds.open-contracting.org/opendatacomparison/api/links'

#Getting all links one page at a time with page size set...for Pagination ...
#ocds_api_url = 'http://ocds.open-contracting.org/opendatacomparison/api/links?page=5&page_size=5'

#Getting only csv links...Sarah configure Django server page size to 500...
#ocds_api_url = 'http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?format=json' 
#----------------------------------------------------------------------------
"""Example: of data structure returned by server...with 5 results all CSVs...

{
    "count": 71,
    "next": "http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?page=2&page_size=5",
    "previous": null,
    "results": [
        {
            "dataset": "Contracts Finder - All Notices",
            "format": "CSV",
            "link": "http://ocds.open-contracting.org/opendatacomparison/download/114/",
            "notes": "",
            "title": "Older Notices - January 2012"
        },
        {
            "dataset": "Buyandsell.gc.ca - Tenders Data",
            "format": "CSV",
            "link": "http://ocds.open-contracting.org/opendatacomparison/download/11/",
            "notes": "microsoft CSV vs CSV",
            "title": "New today tender notices"
        },
        {
            "dataset": "Contracts Finder - All Notices",
            "format": "CSV",
            "link": "http://ocds.open-contracting.org/opendatacomparison/download/80/",
            "notes": "",
            "title": "Older Notices - June 2013"
        },
        {
            "dataset": "OpenTED - Contract Awards",
            "format": "CSV",
            "link": "http://ocds.open-contracting.org/opendatacomparison/download/215/",
            "notes": "",
            "title": "Contract Awards - 2012"
        },
        {
            "dataset": "Buyandsell.gc.ca - Tenders Data",
            "format": "CSV",
            "link": "http://ocds.open-contracting.org/opendatacomparison/download/18/",
            "notes": "",
            "title": "Construction notices"
        }
    ]
}
"""

def merge_json_dict( json_dict1, json_dict2):
    results1 = json_dict1.get('results')
    results2 = json_dict1.get('results')
    return results1.extend(results2)
    
#==============================================================================
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
#==============================================================================  

def get_links(json_dict, key='', value='',prn=True): #, key='format', value='CSV'):
    """Warning: Please Check your key value exists before calling.
    if key='' (the default) then all links are return.""" 
    results = json_dict["results"]
    print len(results)
    links = []
    for (itemNum, item) in enumerate(results):
       print type(value),value, type(item[key]), item[key]  #...make sure both are same type.
       if (key=='') or (item[key] == value):
           if prn:
               print item['link']
           links.append(item['link'])
    if prn:
        print "num of links = ",len(links)
    return links
#-------------------------------------------------------------------------

def get_all_links(json_dict):
    return get_links(json_dict)
#-------------------------------------------------------------------------

def get_all_csv_links(json_dict):
    return get_links(json_dict,'format','CSV')
#==============================================================================   
def select_from_json_dict(json_dict, key='',value='',prn=True):
    """Splits json_dict into two json_dicts by selecting in and out for the
    specified matching key:value pairs"""
    
    json_dict_selected_in  = {}
    json_dict_selected_out = {}
    
    json_dict_selected_in.update(json_dict)
    json_dict_selected_out.update(json_dict)
    

    results = json_dict["results"]
    print len(results)
    res_in  = []
    res_out = []
    for (itemNum, res) in enumerate(results):
       #note: if you don't secify a key then append result.
       if (key=='') or (res[key] == value):
           if prn:
               print res['link']
           res_in.append(res)
       else:  #...select out...
           res_out.append(res)
           
    if prn:
        print "num of results in, out= ",len(res_in),len(res_out)


    json_dict_selected_in['results']  = res_in
    json_dict_selected_out['results'] = res_out

    json_dict_selected_in['count']  = len(res_in)
    json_dict_selected_out['count'] = len(res_out)
    #Future Feature:
    # - take in a {} for key value pairs for multiple conditions.
    #   maybe make another function to iterate AND condition.
    # - consider all boolean operaters AND, OR, NOT, XOR
    # - consider implementing join json_dict
    # - consider creating class json_dict 
    return json_dict_selected_in, json_dict_selected_out

#==============================================================================

def get_filename_from_url(url):
    """Rudamentary parsing of URL into a list and assumming last element is the filename.
    Now handles extraction from url query if it exists."""
    filename = url.split('/')[-1]
    #Sudo Code:
    #if query_exists
    #    get key value pairs
    #    chk for  key="fileName" and get the filename
    
    if filename.find('?'):  #...checking if filename is a possible query.
        dict = extract_info_from_url_query(filename)
        print dict
        if dict=={}:
            print 'filename not found...leaving current filename unchanged'
        else:
            filename = dict.get('fileName') #...should consider case insensitive.
            if filename=="": #...xxx for debugging get ride of later.
                print filename
    
    
    #Futur Feature:
    # - Check for valid filname (must match a file type)
    # - must handle this case:  and probably several more.
    #   (31536000, 'https://online.contractsfinder.businesslink.gov.uk:443/PublicFileDownloadHandler.ashx?fileName=notices_2012_05.csv&recordType=Notices&fileContent=Monthly', 'PublicFileDownloadHandler.ashx?fileName=notices_2012_05.csv&recordType=Notices&fileContent=Monthly')
    # - make functions to handle different cases like...def get_filename_from_content-disposition
    # - run on all data and handle all cases.
    # - key names should be all lower case....to be case insensitive.
    return filename 
#------------------------------------------------------------------------------

def extract_info_from_url_query(a_str):
    #parse above string and reture dict
        #list = bad_filenames[0].split('fileName=')
    dict = {}

    print "-----------------------extract_info_from_url_query---------------------------------------------"
    if a_str.find('?')!=-1:  #...maybe consider a_str.count('?') in case >1 '?'
        print '\na_str=',a_str
        part1,part2 = a_str.split('?')
        
        #example: special case a_str =
        #   "PublicFileDownloadHandler.ashx?fileName=notices_2013_10.xml&recordType=Notices&fileContent=Monthly",

        #if part1 ='PublicFileDownloadHandler.ashx':  #...only need to detect specific cases...going with generality.
        print 'part1=',part1
        print 'part2=',part2
        #extract filename...
        key_values_list = part2.split('&')
        #extracting from strings "key=value" and creating dict 
        for key_value in key_values_list:
            print key_value
            key,value = key_value.split('=')
            dict[key]=value
    else:
        print a_str
        print "? was not found ==> is not a query"

    print "--------------------------------------------------------------------"
    #Future Features:
    # - note: can handle any "part1" string is same way for each special case.
    # - general form part1?part2   part2="key1=value2, key2=value2, ...
    # - part1 string could be a function arg.
    return dict
#------------------------------------------------------------------------------

def get_file_info(link, prn=True):
    """Returns useful info regarding file to download i.e. Metadata
    Getting metadata about one file from remote servers...
    Purpose:  to get filename, filesize, URL & and http Instance info...
    """
    #FILE_SIZE_FAILED = 999999999999  is global constant

    the_file = urllib2.urlopen( link )
    #xxx if chk_the_file  #xxx...implement later.
    #xxx or implement try except here
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
        #xxx Is this really the file size?...verify...
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
    #Future Features:
    # - verify that the filesize is correct. Can be done once downloaded.
    # - add expire date
    # - add try except
    # - check url & filename
    return httpInstance.dict,(fileSize, url, filename )  #...should return struct, filename etc..
#------------------------------------------------------------------------------

def get_all_files_info(json_dict):
    """ToDo:  Get info on all files i.e. extend/augment json_dict and return
    augmented data structure to include added info/metadata about all files.
 
    Purpose:  to allow users to select downloading files based on metadata.

    Warnings:
    1) filename extration is currently rudimentry. Please verify.
       Upgrade soon to come.
    2) FILE_SIZE_FAILED = '999999999999' or interger 999999999999

    Example: of augmented resutl withing json_dict
        Note: file_size, filename, http_dict and url have be added...
            {
            "dataset": "Buyandsell.gc.ca - Contract History",
            "file_size": 24360369,
            "filename": "tpsgc-pwgsc_co-ch_EF-FY-13-14.csv",
            "format": "CSV",
            "http_dict": {
                "accept-ranges": "bytes",
                "connection": "close",
                "content-length": "24360369",
                "content-type": "application/octet-stream",
                "date": "Fri, 04 Jul 2014 16:42:38 GMT",
                "last-modified": "Sun, 01 Jun 2014 14:52:41 GMT",
                "server": "nginx",
                "strict-transport-security": "max-age=31536000",
                "x-frame-options": "SAMEORIGIN"
            },
            "link": "http://ocds.open-contracting.org/opendatacomparison/download/5/",
            "notes": "",
            "title": "Contract History - 2013-2014",
            "url": "https://buyandsell.gc.ca/cds/public/contracts/tpsgc-pwgsc_co-ch_EF-FY-13-14.csv"
        }
    """    
    results = json_dict['results']
    for i,res in enumerate(results):
        try:
            print 'i,res =', i,res  #...xxx for debugging.
            print_dict(res)         #...xxx for debugging
            if res.get('link')=='http://ocds.open-contracting.org/opendatacomparison/download/1/':
                print 'xxx debug'
            http_dict, file_info =  get_file_info(res['link'])
            file_size, url, filename = file_info
            #add http_dict field
            res['http_dict'] = http_dict
            res['file_size'] = file_size
            res['url'] = url
            res['filename'] = filename
            results[i]= res
        except Exception, e:
            res['http_dict'] = {'exception':e, 'link': res['link']}  #...use this to list exceptions.
            res['file_size'] = FILE_SIZE_FAILED
            res['url'] = res['link']
            res['filename'] = ''
            print 'EXCEPTION OCCURED:' #...xxx for debuging
            print 'res=', res          #...xxx for debuging
            print_dict(res)            #...xxx for debuging, note does not work with print_json_dict()
            results[i]= res
        
    json_dict['results']=results
    #Future Features:
    # - caching:check if already downloaded, must include expery date check but can
    #   also start by checking by filename &filesize.
    # -
    return json_dict

#==============================================================================

def print_dict_recursive(a_dict,spaces='    '):
    """Print dictionary recursively in readable format, 
    handles recursive structures like lists of ditionaries. 
    Try using this function if print_json_dict fails.
    This function can handle non-serializable objects unlike print_json_dict"""
    #print a_dict.keys()
    
    for key in a_dict.keys():
        value = a_dict.get(key)

        if type(value)==type([]):  #...i.e. is a list of dicts
            print spaces,key,':'
            for sub_dict in value:
                print_dict_recursive(sub_dict, spaces+'    ')  #...recursively call. 
                print spaces +'     '+'------------------------------------------------------'
        elif type(value)==type({}):
            print spaces,key,':'

            print_dict_recursive(value, spaces+'    ')
        else:
            print spaces, key,':', a_dict.get(key)
    return
#------------------------------------------------------------------------------
def print_dict(a_dict, spaces='    '):
    """Print dictionary recursively in readable format, 
    handles recursive structures like lists of ditionaries. 
    This function first tries print_json_dict for a beautifully formatted ouput
    but if it fails, a recursive algorithm takes over and attempts the printing.
    Note:  The recurse algrithim does not care about serializing objects unlike print_json_dict"""
    print '==================================================================='
    try:
        print_json_dict(a_dict)
    except:
        print_dict_recursive(a_dict)
    print '==================================================================='
    return
#------------------------------------------------------------------------------

def get_content(json_dict, key, prn=True): #...add if value contains
    """Given the key, returns list of values from json_dict.
    Great for debugging or just seeing all values for any given key.
    """ 
    results = json_dict.get('results')
    content = []
    for res in results:
        value = res.get(key)
        content.append(value)
        if prn:
            print key+'=',value
    #Future Features:
    # - may want to also return uniq content with frequencies
    return content
#------------------------------------------------------------------------------

def flatten_result(results_dict, prn=True):
    """To facilitate access to result info by flattening the dict data structure"""
    dict={}
    #dict.update(result_dict)
    #results = json_dict.get('results')
    #content = []
    for key in results_dict.keys():  
   
        value = result_dict.get(key)
        #if type(value)==type({}):
            
        #content.append(value)
        if key!='http_dict':
            dict.update({key:value})
        if prn:
            print key+'=',value
    
    dict.update(result_dict.get('http_dict'))
    #Future Features:
    return dict
#-----------------------------------------------------------------------------    

#==============================================================================

def save_file(url, simulate=False):
   """Downloads and Saves one file:"""
   #Notes to self:
   #getting the file contents...    
   the_file = urllib2.urlopen(url)
   url_redirect = the_file.url  #...note1: redirect from Django, Note2: same as the_file.geturl()
   #Parse theUrl to get filename.
   file_name = get_filename_from_url(url_redirect) 

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
   #Future Features:
   # - maybe call this "download_file" from url
   #-  add path to local files
   # - check if file has been downloaded ( file size, chksum etc)
   # - return message regarding successful transfer, overwitten etc.
   # - and try, except and handle specific conditions.
   # - handle multiple downloads at higher level
   # - verbose option
   # - simulate download first option
   # - estimate time to download
   # - progress of download
   # - can easily log or put into Dict or sqlight
   return 
#-----------------------------------------------------------------------------    
def save_files(links, simulate=False):
    """Downloads and saves files to local drive at current directory."""
    for link in links:
        save_file(link, simulate)
    #Future Features:
    # - add path to local drive
    # - maybe rename to download_files
    return
#-----------------------------------------------------------------------------    

def save_csvs_by_dataset(value="Contracts Finder - All Notices",num=5, simulate=False):
    """Downloads and saves a specified number of CSV files selected on 
    a specified dataset value.""" 
    json_dict_all_csvs = get_json_dict('http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?')

    print_json_dict(json_dict_all_csvs)
    links = get_links(json_dict_all_csvs, 'dataset', value ) #...selecting links
    print "links:  ", links
    save_files(links, simulate)
    #Future Feature:
    # - value should be searched case insensitive.
    # - value contains "all notices"
    return 
#-----------------------------------------------------------------------------    

def save_csvs_limited_by_size(num=5, size=1000):
    """Will implement next, similar to save_csvs_by_dataset"""
    pass
    #Future Features:
    # - get some rest frist.
    return    
#-----------------------------------------------------------------------------    

#==============================================================================

def use_cases():
    simulate = True

    #Examples: Use cases...
    json_dict_all      = get_json_dict()  #...gets all links from ocds api.
    
    json_dict_all_csvs = get_json_dict('http://ocds.open-contracting.org/opendatacomparison/api/links/f/csv?')
    
    json_dict_5_csvs   = get_json_dict_select()  #...gets up to 5 csv links from ocds api.
    
    json_dict_500_csvs = get_json_dict_select(500) #...gets up to 500 csv links
    
    json_dict_20       = get_json_dict_select(20, 'http://ocds.open-contracting.org/opendatacomparison/api/links?')
    
    print_json_dict(json_dict_5_csvs)

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
    print_json_dict(http_info) #... print http information collected from server
    print_json_dict(file_info) #...prints file size, url & filename
    #getting information of all files and augmenting json_dict...
    json_dict_augmented = get_all_files_info(json_dict)  #...metadata all collected in one place.
    print_json_dict(json_dict_augmented)
    #==========================================================================
    #Now one can search on augmented metadata...not the best use case example but...
    links6 = get_links(json_dict_augmented, 'file_size', FILE_SIZE_FAILED) #...lists all failed attemps
    print 'Failed to obtain, file sizes for the following links...will have to investigate...' 
    print_json_dict(links6)
    #==========================================================================
    print "Warning: this section downloads files into your current directory"
    print " - you may want to simulate the download first but be advised that"
    print "   empty files will be written to your current directory."
    if True: #Example: of a specific save function 
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
    
        save_files(links, simulate==True) #... links are urls and True means simulate.
        
    print "Finished use_cases"
    
    return
#==============================================================================
#def investigate_failed_attempts():
#------------------------------------------------------------------------------
    
if True:   #NOTE: this takes 5-10 minutes to fetch data from internet

    #json_dict_all      = get_json_dict()  #...gets all links from ocds api.
    json_dict_500       = get_json_dict_select(500, 'http://ocds.open-contracting.org/opendatacomparison/api/links?')

    json_dict_augmented = get_all_files_info(json_dict_500)  #...metadata all collected in one place.
    #print_json_dict(json_dict_augmented)
if True:
    links6 = get_links(json_dict_augmented, 'file_size', FILE_SIZE_FAILED) #...lists all failed attemps
    print 'Failed to obtain, file sizes for the following links...will have to investigate...' 
    print_json_dict(links6)

    links7 = get_links(json_dict_augmented, 'file_size', FILE_SIZE_FAILED) #...lists all failed attemps
    print 'Failed to obtain, file sizes for the following links...will have to investigate...' 
    print_json_dict(links6)


    json_dict_selected_in_csvs, json_dict_selected_out_csvs = select_from_json_dict(json_dict_augmented, 'format','CSV',True)
    json_dict_selected_in_bad, json_dict_selected_out_bad = select_from_json_dict(json_dict_augmented, 'file_size', FILE_SIZE_FAILED,True)
    #print_dict(json_dict_selected_in_bad)
    
    bad_filenames = get_content(json_dict_selected_in_bad, 'filename')
    print_json_dict( bad_filenames )

    #------------------------------------------------------------------------- 
    #Example1:  Extracting info from a url query...   
    filename_dict = extract_info_from_url_query("PublicFileDownloadHandler.ashx?fileName=notices_2013_10.xml&recordType=Notices&fileContent=Monthly")
    filename = filename_dict['fileName']
    print filename
    #Example2:  Extracting info from a url query...   
    filename_dict = extract_info_from_url_query("search?f%5Bitem_type%5D%5B%5D=Call+for+tenders&q=everything")
    filename = filename_dict.get('fileName')
    print "does filename exist:", filename==None
    #-------------------------------------------------------------------------    
    #Example: of printing one flattened result...
    result_dict = json_dict_selected_in_csvs.get('results')[0]
    flat_result = flatten_result(result_dict)
    print_dict(flat_result)
    print_dict(flat_result.keys())
    print_dict(flat_result.values())
    print "==================================================================="
    print_dict(get_content(json_dict_augmented, 'filename'))  #...all extracted filenames.
    print "==================================================================="
    print_dict(get_content(json_dict_selected_in_csvs, 'filename'))  #...all extracted CSV filenames.
    #-------------------------------------------------------------------------    








#ToDo:
# - save limit size
# - get filename cases:
#       in some cases can get filename from...content-disposition : attachment; filename="notices_2012_08.csv"
#      "rows.json?accessType=DOWNLOAD"
#      "rows.csv?accessType=DOWNLOAD"
#      "tpsgc-pwgsc_ao-t_n?publication_date=today",
# - get this...
#      res['http_dict'] = {'exception':e, 'link': res['link']}  #...use this to list exceptions.
# - get all file types 
    #list all filenames that don't end in a ".file_type"
    #list all empty filenames and other info
    #generate filenames from url and other info.
# - done: flatten dict struct?  but not results
# - get expiry date
# - get superset of http fieldnames
# - create secific function called extract_from_http_dict
        

    
#----------------------------------------------------------------------------

#Future Features:
# - add comments regarding what this function is about.
# - Note: the above code can be put into a class maybe called OCDS_Api
# - package up some of the functions info a class called json_dict
# - unit testing? consider later.
#==============================================================================

#use_cases()
#testing()