#!/usr/bin/env python
import urllib2
import os
import sys

def get_dimension_info(id):

def scrape_with_id(id, magnification=1,name = "foo"):
    """ 
        Google art project image urls are of the form
        http://lh3.ggpht.com/94h7x8vc6reTGlTijnNZyPunwaIcim6NSl5fSsKYMVLjPCHM0O9BUnB6tg=x0-y0-z1

        To deal with magnification, the pictures are tiled at larger magnifications. The z# represents the dimension of the tiles.

    """
    prefix = "http://lh3.ggpht.com/"
    url = prefix + id 

    # We'll need to save the tiles. This creates an organized directory structure.
    # The directory structures is 
    # id[:5]/magnification/x0_y0_z1.jpg
    # ...
    dimension_tuple = get_dimension_info(id)
    tile_x, tile_y = dimension_tuple

    directory = "%s/%d" % (id[:5], magnification)
    cmd = 'mkdir -p %s' % directory
    print cmd
    os.system(cmd)

    montage_list = [] 

    #tiling dimension values
    max_x = 0
    max_y = 0
    
    #loop to get each tile
    for j in range(tile_y):
        for i in range(tile_x):
            coordinates = "x%d-y%d-z%d" % (i,j,magnification)
            picture_name = coordinates + ".jpg"
            cmd = 'wget "%s=%s" -P %s -O %s/%s' % (url,coordinates,directory,  directory, picture_name)
            print cmd
            ret = os.system(cmd)
            #if ret == 0:
            #only attach if not 404
            montage_list.append("%s/%s" % (directory, picture_name))
           
    #montage_cmd = "montage %s -geometry +0+0 %s.jpg" % ("%s/*" % directory, name) 
    montage_cmd = "montage %s -tile %dx%d -geometry +0+0 %s.jpg" % (' '.join(montage_list), tile_x, tile_y, name) 
    print montage_cmd
    os.system(montage_cmd)
    
    

def main():
    try: 
        id = sys.argv[1]
    except:
        print "Please enter an id for the picture"
        exit(1)

    try:
        magnification = int(sys.argv[2])
    except:
        magnification = 1

    scrape_with_id(id,magnification)

if __name__ == "__main__":
    main() 
