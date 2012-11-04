# given the file name of the term document matrix
# load it into memory, compute a tf-idf matrix, and then
# compute pairwise similarity based on normalized dot product (cosine similarity)
import math

def load_tdf(tdf_name="out\tdf.txt"):
    lines = [line for line in file(tdf_name)]
    # first line is column titles
    colnames=lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        # rownames is the first in each row
        rownames.append(p[0])
        # data is in the remainder of each row
        data.append([float(x) for x in p[1:]])
    return rownames,colnames,data

def compute_idf(tdf):
    idf=[]
    total_documents = len(tdf)
    for i in range(len(tdf[0])):
        doc_freq=len([True for j in range(total_documents) if tdf[j][i]>0])
        if doc_freq==0:
            idf.append(1.0)
        else:
            idf.append(1.0+math.log(total_documents/doc_freq))
    return idf
    
def compute_tf_idf_matrix(tdf,idf):
    """Convert a term document matrix into a tf-idf matrix given the matrix and the idf"""
    for i in range(len(tdf)):
        for j in range(tdf[i]):
            tdf[j][i]=tdf[j][i]*idf[i]
    return tdf            
    
def compute_similarity(v1,v2):
    """compute cosine similarity between two vectors, assumes they have been normalized by tf-idf"""
    norm_v1=0
    norm_v2=0
    cross_v1_v2=0
    for i in range(len(v1)):
        norm_v1+=v1[i]*v1[i]
        norm_v2+=v2[i]*v2[i]
        cross_v1_v2+=v1[i]*v2[i]
    return cross_v1_v2/sqrt(norm_v1)/sqrt(norm_v1)
    
def compute_similarity_matrix:
             
        