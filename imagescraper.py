#!/usr/bin/env python
"""
Leah Xue 
June 19th, 2011

To run this, you need

1. wget
2. imagemagick

On mac, get homebrew or macports
On linux, well you probably already know
On windows, cygwin.
"""
import urllib2
import os
import sys

from xml.dom.minidom import parseString #simple XML
from BeautifulSoup import BeautifulSoup #complicated HTML

def get_id_from_page(url):
    """
    returns (id, name)
    """
    f = urllib2.urlopen(url)
    html = f.read()
    soup = BeautifulSoup(html)
    id = soup.body['data-thumbnail']
    return id #get rid of utf-8 to be safe


def get_dimension_info(id):
    """
    Google stores the dimension info for its maps in an xml file. 
    This reads the xml file containing the info and returns a dict of tuples.
    
    return =  magnification : (x tiles, y tiles, x_border, y_border)
    """
    url = "http://lh4.ggpht.com/" + id + "=g"
    print url
    html = urllib2.urlopen(url).read()
    dom = parseString(html)
    dom_tiles = dom.getElementsByTagName('pyramid_level')
    dimension_matrix = dict()
    for magnification, pyramid_data in enumerate(dom_tiles):
        dimension_matrix[magnification] = [int(pyramid_data.getAttribute('num_tiles_x')), int(pyramid_data.getAttribute('num_tiles_y')), int(pyramid_data.getAttribute('empty_pels_x')), int(pyramid_data.getAttribute('empty_pels_y'))]
    return dimension_matrix
        
def scrape_with_id(id, magnification=1,name = None):
    """ 
        Google art project image urls are of the form
        http://lh3.ggpht.com/94h7x8vc6reTGlTijnNZyPunwaIcim6NSl5fSsKYMVLjPCHM0O9BUnB6tg=x0-y0-z1

        To deal with magnification, the pictures are tiled at larger magnifications. The z# represents the dimension of the tiles.

    """
    prefix = "http://lh3.ggpht.com/"
    url = prefix + id 
    
    if not name:
        name = id[:5] 
    
    name = "%s_%d" % (name, magnification)
    
    #dimension stuff
    dimension_matrix = get_dimension_info(id)
    print dimension_matrix
    if not magnification in dimension_matrix:
        return False
    tile_x, tile_y, subtract_x, subtract_y = dimension_matrix[magnification]
    
    print tile_x, tile_y, subtract_x, subtract_y
    
    width = tile_x * 512
    height = tile_y * 512

    # We'll need to save the tiles. This creates an organized directory structure.
    # The directory structures is 
    # id[:5]/magnification/x0_y0_z1.jpg
    # ...
    directory = "%s/%d" % (id[:5], magnification)
    cmd = 'mkdir -p %s' % directory
    print cmd
    os.system(cmd)

    montage_list = [] 
    #loop to get each tile
    for j in range(tile_y):
        for i in range(tile_x):
            coordinates = "x%d-y%d-z%d" % (i,j,magnification)
            picture_name = coordinates + ".jpg"
            cmd = 'wget "%s=%s" -P %s -O %s/%s' % (url,coordinates,directory,  directory, picture_name)
            print cmd
            ret = os.system(cmd)
            montage_list.append("%s/%s" % (directory, picture_name))
           
    montage_cmd = "montage %s -tile %dx%d -geometry +0+0 %s.jpg" % (' '.join(montage_list), tile_x, tile_y, name) 
    print montage_cmd
    os.system(montage_cmd)
    
    crop_cmd = "convert -crop %dx%d+0+0 %s.jpg %s.jpg" % (width - subtract_x,height - subtract_y,name,name)
    print crop_cmd
    os.system(crop_cmd)
    
    delete_tmp = "rm -rf %s/" % directory
    print delete_tmp
    os.system(delete_tmp)
    
    

def main():
    try: 
        url = sys.argv[1]
    except:
        print "Please enter the url for a google art project page"
        exit(1)
    
    id = get_id_from_page(url)
    print id
    
    name = url.split('/')[-1]

    try:
        magnification = int(sys.argv[2])
    except:
        magnification = 3 #big enough for most monitors
        
    # implement more intelligent options
    # http://docs.python.org/library/getopt.html

    scrape_with_id(id,magnification,name)

if __name__ == "__main__":
    main() 
