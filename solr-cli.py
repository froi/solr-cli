"""
    Usage:
        solr-cli search <target_host> [<target_port>] <collection> (-q=<query> | --query=<query>) [options]
        solr-cli (add | update | delete) <target_host> < <collection> (-q=<query> | --query=<query>) [options]
        solr-cli migrate <source_host> [<source_port>] <destination_host> [<destination_port>] <collection> [options]
        solr-cli (-h | --help | --version)

    Commands:
        search                  Search command.
        add                     Command used to add an entry to a Solr collection
        update                  Command used to update an entry in a Solr collection
        delete                  Command used to delete an entry in a Solr collection
        migrate                 Command used to migrate data from one Solr collection to another.

    Arguments:
        target_host             Target host for the search, add, update, and delete commands
        target_port             Target port for the search, add, update, and delete commands
                                [default: 8983]
        source_host             Source host for the data migration. Used only with the migrate cammand.
        source_port             Source port for the data migration. Used only with the migrate cammand.
                                [default: 8983]
        destination_host        Destination host for the data migration. Used only with the migrate cammand.
        destination_port        Source port for the data migration. Used only with the migrate cammand.
                                [default: 8983]
    Options:
        -h --help               Show this screen.
        --version               Show version.
        -q=<q>, --query=<q>     Data payload to be sent to the server
        --wt=<wt>               [default: json]
        --indent=ind            Indent output (true or false). Used with the search command.
                                [default: true]
        --limit=l               Limits output amount, pass `all` to get all records. Used with the search command.
                                [default: 10]
        --commit=c              Commits action sent to the Solr server.
                                [dafault: false]
        --pagesize=<amount>     [default: 1000]
        --rate=<rate>           [default: 0]
        --page=<page>           [default: 1]
        --sort=<sort>           [default: id ASC]
        --mark=<mark>           [default: *]
        --lastmark=<lastmark>   [default: *]
"""

import docopt
import requests
import time


class SolrBase(object):

    def __init__(self, wt, pagesize, rate, page, sort, collection):
        self.wt = wt
        self.pagesize = pagesize
        self.rate = rate
        self.page = page
        self.sort = sort
        self.collection = collection

    @staticmethod
    def get_sorl_url(host, port, collection):
        sorl_url_format = 'http://{}:{}/solr/{}/'

        return sorl_url_format.format(host, port, collection)

    @staticmethod
    def select(target_url, params):
        request_url = '{}/select/'.format(target_url)

        response = requests.get(request_url, params=params)

        data = response.json

        return data['response']['docs']

    def update(self):
        pass

    def commit(self):
        pass


class SolrMigrate(SolrBase):

    def __init__(self, wt, pagesize, rate, page, sort, collection,
                 source_host, source_port, destination_host, destination_port):

        super(SolrMigrate, self).__init__(wt, pagesize, rate, page, sort, collection)

        self.source_host = source_host
        self.source_port = source_port
        self.destination_host = destination_host
        self.destination_port = destination_port
        self.documents = None

    def get_source_documents(self, params):
        self.documents = SolrBase.select(self.source_url, params)


class SolrSearch(SolrBase):
    def __init__(self, wt, pagesize, rate, page, sort, source_host, source_port, destination_host, destination_port):
        pass


class SolrAdd(SolrBase):
    def __init__(self, wt, pagesize, rate, page, sort, source_host, source_port, destination_host, destination_port):
        pass


class SolrUpdate(SolrBase):
    def __init__(self, wt, pagesize, rate, page, sort, source_host, source_port, destination_host, destination_port):
        pass


class SolrDelete(SolrBase):
    def __init__(self, wt, pagesize, rate, page, sort, source_host, source_port, destination_host, destination_port):
        pass


def main(args):
    # Set all argument values
    collection = args['<collection>']
    wt = args['--wt']
    pagesize = args['--pagesize']
    rate = args['--rate']
    page = args['--page']
    sort = args['--sort']
    mark = args['--mark']
    lastmark = args['--lastmark']

    if args['migrate']:
        source_host = args['<source_host>']
        source_port = args['<source_port>']
        destination_host = args['<destination_host>']
        destination_port = args['<destination_port>']

        solr_migrate = SolrMigrate(wt, pagesize, rate, page, sort, collection,
                                   source_host, source_port, destination_host, destination_port)

        solr_migrate.source_url = SolrBase.get_sorl_url(source_host, source_port, collection)
        solr_migrate.destination_url = SolrBase.get_sorl_url(destination_host, destination_port, collection)

        params = {
            'q': '*.*',
            'rows': pagesize,
            'sort': sort,
            'cursorMark': mark,
        }

        solr_migrate.get_source_documents(params)

    elif args['search']:
        target_host = args['<target_host>']
        target_port = args['<target_port>']
        host_url = args['<host_url>']
        query = args['-q'] if args['-q'] else args['--query']
        indent = args['--indent']
        limit = args['--limit']
        commit = True if args['--commit'] == 'true' else False

if __name__ == '__main__':
    print(time.localtime())

    args = docopt(__doc__)

    main(args)

    print(time.localtime())
