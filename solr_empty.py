import solr
import sys
if __name__ == '__main__':
    print('Emptying Solr')
    solrconn = solr.SolrConnection('http://localhost:8983/solr/crim')
    solrconn.delete_query('*:*')
    solrconn.commit()
    sys.exit()
