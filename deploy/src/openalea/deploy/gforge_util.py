#!/usr/bin/python
#####################################################################"
# 02/2006 Will Holcomb <wholcomb@gmail.com>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
"""Utility script to upload package on the Gforge

Enables the use of multipart/form-data for posting forms

Inspirations
------------
    Upload files in python:
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
    urllib2_file:
        Fabien Seisen: <fabien@seisen.org>

Example
-------
>>> import MultipartPostHandler, urllib2, cookielib
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
        MultipartPostHandler.MultipartPostHandler)
    params = { "username" : "bob", "password" : "riviera",
        "file" : open("filename", "rb") }
    opener.open("http://wwww.bobsite.com/upload/", params)

Further Example
---------------
  The main function of this file is a sample which downloads a page and
  then uploads it to the W3C validator.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import urllib
import urllib2
import mimetools, mimetypes
import os, stat, sys
from cStringIO import StringIO

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if key == "userfile":
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)

                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        
        return request

    def multipart_encode(vars, files, boundary = None, buf = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buf is None:
            buf = StringIO()
        for(key, value) in vars:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + value + '\r\n')
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buf.write('Content-Type: %s\r\n' % contenttype)
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buf.write('\r\n' + fd.read() + '\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf
    multipart_encode = Callable(multipart_encode)

    https_request = http_request


##########################################################"



import cookielib, urllib, urllib2, urlparse
import os
import glob
urlOpener = None

def cookie_login(loginurl, values):
    """ Open a session
    login_url : the login url
    values : dictionnary containing login form field
    """
    global urlOpener
    # Enable cookie support for urllib2
    cookiejar = cookielib.CookieJar()
    urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar),
                                     MultipartPostHandler)
    
    data = urllib.urlencode(values)
    request = urllib2.Request(loginurl, data)
    url = urlOpener.open(request)  # Our cookiejar automatically receives the cookies
    urllib2.install_opener(urlOpener)


    # Make sure we are logged in by checking the presence of the cookie "session_ser".
    # (which is the cookie containing the session identifier.)
    if not 'session_ser' in [cookie.name for cookie in cookiejar]:
        print "Login failed !"
    else:
        print "We are logged in !"

        


########################################
# To add a new function:
#  + go to the web page and display the source.
#  + search the tag <form /> (function) and the name of the <input />
#  + copy also the url
#  + check the type or the domain of the values.
#  + Create the function (dict+ post url)

def gforge_login(userid, passwd):
    """ Login on Gforge """
    # Create login/password values
    values = {'form_loginname': userid,
              'form_pw': passwd,
              'return_to' : '',
              'login' : "Connexion avec SSL" }
    
    url = "https://gforge.inria.fr/account/login.php"
    cookie_login(url, values)


def delete_package(group_id, pkg_id):
    """ Delete a package """
    url = "https://gforge.inria.fr/frs/admin/?group_id=%i"%(group_id,)
    values = { 'func' : "delete_package",
               'package_id' : pkg_id,
               'sure' : 1,
               'really_sure' : 1,
               }
     
    fp = urlOpener.open(url, values)


def delete_release(group_id, pkg_id, release_id):
    """ Delete a release """
    url = "https://gforge.inria.fr/frs/admin/" +\
        "showreleases.php?group_id=%i&package_id=%i"%(group_id, pkg_id)
    values = { 'func' : "delete_release",
               'release_id' : release_id,
               'sure' : 1,
               'really_sure' : 1,
               }
     
    fp = urlOpener.open(url, values)


def upload_file(filename, group_id, pkg_id, release_id, type_id, proc_id):

    url = "https://gforge.inria.fr/frs/admin/editrelease.php?" \
        + "group_id=%i&release_id=%i&package_id=%i"%(group_id, release_id, pkg_id)

    values = { 'step2' : "1",
               'type_id' : str(type_id),
               'processor_id' : str(proc_id),
               'userfile' : open(filename, "rb"),
               }
    fp = urlOpener.open(url, values)
