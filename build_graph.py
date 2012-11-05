# build a graph from a bunch of json files created by get_feed.py

import networkx as nx
import sys
import os
import json
import link_extractor as le

def build_graphs_from_json(blog_file):
    # get list of blogs based on feedlist in blog_file
    blog_list=[line for line in file(blog_file)]
    # get json files
    json_files = [fil for fil in os.listdir("out/") if fil.endswith(".json")]
    
    # initialize graph
    blog_gr = nx.DiGraph()
    blog_gr.add_nodes_from(blog_list)
    #print blog_gr.nodes()
    for fil in json_files:
        print "Processing: " + fil
        blog_props = json.load(file("out/" + fil))
        # get the node
        blog_url = blog_props[0]['blogurl']
        #blog_url = ''.join([c for c in blog_url if c not in '\n'])
        print blog_props[0]['title'].encode('ascii','ignore')
        #blog_gr[blog_url].setdefault('weight',blog_props[0]['blogtitle'])
        # add up all outlinks
        outlinks = {}
        # note this is commented out because I am using blogroll
        #        for prop in blog_props[1:]:
        #            for outlink in prop['bloglinks']:
        #                outlinks.setdefault(outlink,0)
        #                outlinks[outlink]+=prop['bloglinks'][outlink]
        outlinks = blog_props[0]['blogroll']
        print outlinks
        for outlink in outlinks:
            try:
                blog_gr.add_edge(blog_url,outlink)
            except TypeError:
                print 'Type Error in add_edge'
                print blog_url
                print outlink
                raise TypeError
            blog_gr[blog_url][outlink].setdefault('weight',0)
            blog_gr[blog_url][outlink]['weight']+=1
    nx.write_gml(blog_gr,'out/blogs.gml')
    return

def build_graph_from_manual( blog_file, add_labels=False ):
    blog_list = [line for line in file(blog_file)]
    blog_gr=nx.DiGraph()
    
    for blog in blog_list:
        blog=blog.strip()
        # split on the semicolon, on the left is the node and the right are outlinks
        bl_list = blog.split(';',2)
        blog_gr.add_node(bl_list[0])
        if len(bl_list)>1 and bl_list[1]!="":
            if bl_list[0].find("visualcomplexity.com")>-1:
                # some debugging
                print blog
                print bl_list
                
            outlinks = bl_list[1].split(',')
            for outlink in outlinks:
                if (len(outlink)>1 and outlink[len(outlink)-1]=='/'):
                    outlink=outlink[-1]
                elif (len(outlink)==1 or outlink==''):
                    # skip some slop
                    continue        
                blog_gr.add_edge(bl_list[0],outlink)
    # add labels to nodes, if we need to
    if (add_labels):
        for n in blog_gr:
            blog_gr[n]['title'] = ''
            try:
                webpage_title = le.extract_title_from_url(n)
                print >> sys.stderr, 'Note: web page at ' + n + ' has title ' + webpage_title
                blog_gr[n]['title'] = webpage_title.strip().replace('\n','').replace('&nbsp;','')
            except:
                print >> sys.stderr, 'Note: Could not parse ' + n
                blog_gr[n]['title'] = n
    #write out by hand
    node_dot = ['"%s" [label="%s"]' % (n,blog_gr[n]['title']) for n in blog_gr]
    edge_dot = ['"%s" -> "%s"' % (n1, n2) for n1,n2 in blog_gr.edges() if n2!="title"]
    OUT = "out/blogs_manual.dot"
    f = open(OUT,'w')
    f.write('strict digraph{\n%s\n%s\n}' % (";\n".join(node_dot).encode('ascii','ignore'),";\n".join(edge_dot).encode('ascii','ignore')))
    f.close()
    return
    
def make_feedlist_from_file(blog_file,out_file="feedlist_manual.txt"):
    edge_list = [blog for blog in file(blog_file)]
    url_set = set()
    # create set of urls
    for edge in edge_list:
        urls = edge.split(';')
        url_set.add(urls[0])
        if (len(urls)>1 and urls[1]!=''):
            for url in urls[1].split(','):
                url_set.add(url.strip())
    # write out to file
    f=open(out_file,'w')
    f.write('\n'.join(url_set))
    f.close()
    return
                
def main(  ):
    if len(sys.argv)==1 or len(sys.argv)>3:
        print "Usage: python build_graph.py (json|manual|feedlist) <file>"
        return
    elif len(sys.argv)==2:
        if sys.argv[1]=="json":
            blog_file="feedlist.txt"
        else:
            blog_file="manual_blogroll.txt"    
    elif len(sys.argv)==3:
        blog_file=sys.argv[2]
    if sys.argv[1]=="json":
        build_graphs_from_json(blog_file)
    elif sys.argv[1]=="feedlist":
        make_feedlist_from_file(blog_file)
    else:
        build_graph_from_manual(blog_file,add_labels=True)    
    return
if __name__=='__main__':
    main()