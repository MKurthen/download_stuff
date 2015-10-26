#!/usr/bin/python3

#Copyright Maximilian Kurthen

#usage: download_stuff.py [user] [password] [-f]
import os
import re
import sys
import urllib.request

import numpy as np

#force flag to overwrite existing files
if '-f' in sys.argv:
    force = True;
else:
    force = False;

#assume homepages to download from are stored in download_stuff.conf, a whitespace seperated csv-like file, first column indicated url of homepage, second column indicates folder to store stuff at

homepages_array = np.genfromtxt('./download_stuff.conf', dtype = 'str')
#reshape to 2d-array (not necessary for 2 or more urls, but 1 url gives a 1d array)
homepages_array = homepages_array.reshape(-1,2)
homepages_list = homepages_array.tolist()

#authentication information
auth_flag = False
if len(sys.argv) >= 3:
    auth_flag = True
    user = sys.argv[1]
    passwd = sys.argv[2]


#use this set for filetypes to match
filetypes = {'pdf'}

for homepage in homepages_list:

    url = homepage[0]
    target_folder = homepage[1]
    #"base url", i.e. url without trailing index.html or similar
    url_base = str.join('/', url.split('/')[:-1])

    
    try:
        request = urllib.request.urlopen(url)
    except:
        e = sys.exc_info()[0]
        print('Exception: \n {} \ at url: {} '.format(e, url))

    str_html = request.read().decode('UTF-8')

    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
        
    matches = list() 
    for filetype in filetypes:
        #regex matches '"[AnyNumerOfCharactersExceptWhitespace].filetype"'
        matches += re.findall(r'"[^\s]*\.{}"'.format(filetype), str_html)
        
    for match in matches:

        match = match.strip('"')
        storepath = os.path.join(target_folder, match.split('/')[-1])
        if os.path.exists(storepath) and not force:
            print('skipping {}, as {} exists'.format(match, storepath))
            continue

        #corner case where links on math lecture homepages are given as /~matzke/stochastik2015/blatt01.pdf
        if match.startswith('/'):
            #set url_base to e.g. http://www.mathematik.uni-muenchen.de
            url_base = re.findall( '(?:www\.|http:)[^\s]*(?:\.de|\.com|\.org)', url)[0]
            match = match.strip('/')

        path = os.path.join(url_base, match)

        cleanpath = os.path.normpath(path)
        #os.path.normpath may replace https:// with http://
        cleanpath = cleanpath.replace(':/www.' ,'://www.')
        cleanpath_base = str.join('/', cleanpath.split('/')[:-1])

        if auth_flag:
            pwd_man = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            pwd_man.add_password(None, cleanpath_base, user, passwd)
            auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_man)
            opener = urllib.request.build_opener(auth_handler)
            urllib.request.install_opener(opener)

        urllib.request.urlretrieve(cleanpath, storepath)
        print('downloading {} to {}'.format(cleanpath, storepath))







