# build a graph from a bunch of json files created by get_feed.py

import networkx as nx
import sys
import os
import json
import link_extractor as le
import cPickle

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

def build_graph_from_manual( blog_file, add_labels=False, filename="out/blogs_manual.dot" ):
    blog_list = [line for line in file(blog_file)]
    blog_gr=nx.DiGraph()
    
    # create a dictionary of blog url to title out of the json files
    url_titles = {}
    json_files = [fil for fil in os.listdir("out/") if fil.endswith(".json")]
    for json_file in json_files:
        blog_props=json.load(file("out/"+json_file))
        url_titles[blog_props[0]['blogurl'].strip().replace('"','')]=blog_props[0]['title']
    
    for blog in blog_list:
        blog=blog.strip()
        # split on the semicolon, on the left is the node and the right are outlinks
        bl_list = blog.split(';',2)
        try:
            # add node with a label that is the title
            blog_gr.add_node(bl_list[0],label=url_titles[bl_list[0]])
        except KeyError:
            # if we didn't find it in json files, just default to url as label
            blog_gr.add_node(bl_list[0],label=bl_list[0])    
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
                # explicitly add node if not already in
                if outlink not in blog_gr.nodes():
                    try:
                        # add node with a label that is the title
                        blog_gr.add_node(outlink,label=url_titles[outlink])
                    except KeyError:
                        # if we didn't find it in json files, just default to url as label
                        blog_gr.add_node(outlink,label=outlink)    
                           
                blog_gr.add_edge(bl_list[0],outlink)
    if filename.endswith(".dot"):
        #write out by hand
        node_dot = ['"%s" [label="%s"]' % (n[0],n[1]['label'].replace('"','')) for n in blog_gr.nodes(data=True)]
        edge_dot = ['"%s" -> "%s"' % (n1, n2) for n1,n2 in blog_gr.edges() if n2!="title"]
        f = open(filename,'w')
        f.write('strict digraph{\n%s\n%s\n}' % (";\n".join(node_dot).encode('ascii','ignore'),";\n".join(edge_dot).encode('ascii','ignore')))
        f.close()
    elif filename.endswith(".pickle"):
        f = open(filename,'wb')
        cPickle.dump(blog_gr,f)
        f.close()
    elif filename.endswith(".gml"):
        f=open(filename,'w')
        nx.write_gml(blog_gr,f)
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
    if len(sys.argv)==1 or len(sys.argv)>4:
        print "Usage: python build_graph.py (json|manual|feedlist) <file>"
        return
    elif len(sys.argv)==2:
        if sys.argv[1]=="json":
            blog_file="feedlist.txt"
        else:
            blog_file="manual_blogroll.txt"    
    elif len(sys.argv)==3:
        blog_file=sys.argv[2]
    elif len(sys.argv)==4:
        blog_file=sys.argv[2]
        out_file=sys.argv[3]            
    if sys.argv[1]=="json":
        build_graphs_from_json(blog_file)
    elif sys.argv[1]=="feedlist":
        make_feedlist_from_file(blog_file)
    else:
        build_graph_from_manual(blog_file,add_labels=False,filename=out_file)    
    return
if __name__=='__main__':
    main()