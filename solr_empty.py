import solr
import sys
from django.conf import settings

if __name__ == '__main__':
    print('Emptying Solr')
    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    solrconn.delete_query('*:*')
    solrconn.commit()
    sys.exit()
