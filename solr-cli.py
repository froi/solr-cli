"""
    Usage:
        solr-cli (add | delete | update) <target_host> <target_port> <collection> (-q=<q> | --query=<q>) [--commit=<c>]
        solr-cli migrate <source_host> [<source_port>] <destination_host> [<destination_port>] <collection>... [--wt=<wt>] []
        solr-cli search <target_host> [<target_port>] <collection> (-q=<q> | --query=<q>) [--indent=<ind>] [--limit=<l>]
        solr-cli -h | --help
        solr-cli --version

    Commands:
        add                     Command used to add an entry to a Solr collection
        delete                  Command used to delete an entry in a Solr collection
        update                  Command used to update an entry in a Solr collection
        migrate                 Command used to migrate data from one Solr collection to another.
        search                  Search command.

    Arguments:
        destination_host        Destination host for the data migration. Used only with the migrate cammand.
        destination_port        Source port for the data migration. Used only with the migrate cammand.
                                [default: 8983]
        source_host             Source host for the data migration. Used only with the migrate cammand.
        source_port             Source port for the data migration. Used only with the migrate cammand.
                                [default: 8983]
        target_host             Target host for the search, add, update, and delete commands
        target_port             Target port for the search, add, update, and delete commands
                                [default: 8983]
        collection              Collcetion to use with the Solr command. For the migrate command a list of collections
                                can be supplied.
    Options:
        -h --help               Show this screen.
        --indent=<ind>          Indent output (true or false). Used with the search command.
                                [default: true]
        --rows=<rows>           Limits output amount, pass `all` to get all records. Used with the search command.
                                [default: 10]
        --commit=<c>            Commits action sent to the Solr server.
                                [dafault: false]
        --pagesize=<amount>     [default: 1000]
        -q=<q>, --query=<q>     Data payload to be sent to the server
        --rate=<rate>           [default: 0]
        --sort=<sort>           [default: id ASC]
        --version               Show version.
        --wt=<wt>               [default: json]
        -o <file>, --out=<file> Sends search results to a file.
"""

import docopt
import requests
import time


class SolrBase(object):
    lastmark = '*'

    def __init__(self, collection, **kwargs):
        self.collection = collection
        self.params = kwargs['params'] if kwargs['params'] else None

    @staticmethod
    def get_sorl_url(host, port, collection):
        sorl_url_format = 'http://{}:{}/solr/{}/'

        return sorl_url_format.format(host, port, collection)

    @staticmethod
    def select(target_url, request_params):
        """
        Executes a selection query with the target url.
        """
        request_url = '{}/select/'.format(target_url)

        response = requests.get(request_url, params=request_params)

        return response.json()

    @staticmethod
    def update(target_url, request_params, request_body=None):
        """
        Executes an update query with the target url.
        """
        request_url = '{}/update/'.format(target_url)

        response = requests.get(request_url, params=request_params)

        return response.json()


class SolrMigrate(SolrBase):
    """
    Handles all migration processes. Migrations are between two collections in the same server or between remote servers.
    """

    def __init__(self, source_url, destination_url, collection, **kwargs):

        super(SolrMigrate, self).__init__(collection. kwargs['wt'], kwargs['pagesize'], kwargs['rate'], kwargs['sort'], kwargs['rows'])

        self.source_url = source_url
        self.destination_url = destination_url
        self.documents = None

    def migrate(self, params`):
        """
        Migrate documents from source collection to a destication collection.
        """
        continue_migrate_loop = True

        while continue_migrate_loop:
            response = SolrBase.select(self.source_url, params)

            total_docs = response['response']['numFound']
            docs = response['response']['docs']
            mark = response['nextCursorMark']

            if total_docs:
                cleaned_docs = []

                if mark == self.lastmark:
                    continue_migrate_loop = False
                else:
                    self.lastmark = mark

                    for doc in docs:
                        del(doc['_version_'])

                    # Update destination collection with documents found in the source collection.
                    update_params = {'commit': False, 'softCommit': False, 'waitSearcher': False, 'waitFlush': False, }
                    SolrBase.update(self.destination_url, request_params=update_params, request_body=docs)

                    # Update changes made to the destination colleciton
                    commit_params = {'commit': True, }
                    SolrBase.update(self.destination_url, request_params=commit_params)

            else:
                print('No documents where found at the source url: {}'.format(self.source_url))


class SolrSearch(SolrBase):
    def __init__(self, target_url, collection, **kwargs):
        super(SolrSearch, self).__init__(collection, **kwargs)
        self.target_url = target_url
        if kwargs['-o']:
            self.output_file = kwargs['-o']
        elif kwargs['--out']:
            self.output_file = kwargs['--out']
        else:
            self.output_file = None

    def exec_search(self):
        continue_search_loop = True

        while continue_search_loop:
            response = SolrBase.select(self.target_url, self.params)

            total_docs = response['response']['numFound']
            docs = response['response']['docs']
            mark = response['nextCursorMark']

            if total_docs and total_docs > 0:
                if mark == self.lastmark:
                    continue_search_loop = False
                else:
                    self.lastmark = mark

                    with open(self.output_file, 'a') as tmp_file:
                        for doc in docs:
                            tmp_file.write(doc)
                            tmp_file.write('\n')
            else:
                print('No documents where found at the source url: {}'.format(self.source_url))
                continue_search_loop = False


class SolrAdd(SolrBase):
    def __init__(self, target_url, collection, **kwargs):
        super(SolrAdd, self).__init__(collection, **kwargs)
        self.target_url = target_url


class SolrUpdate(SolrBase):
    def __init__(self, target_url, collection, **kwargs):
        super(SolrUpdate, self).__init__(collection, **kwargs)
        self.target_url = target_url


class SolrDelete(SolrBase):
    def __init__(self, target_url, collection, **kwargs):
        super(SolrDelete, self).__init__(collection, **kwargs)
        self.target_url = target_url


def main(args):
    # Set all argument values
    collection = args['<collection>']
    # wt = args['--wt']
    # pagesize = args['--pagesize']
    # sort = args['--sort']
    # rows = args['--rows']
    rate = args['--rate']
    page = args['--page']

    if args['-q']:
        query = args['-q']
    elif args['--query']:
        query = args['--query'] 
    else:
        query = '*:*'

    params = {
        'q': query,
        'wt': args['--wt'],
        'pagesize': args['pagesize'],
        'sort': args['sort'],
        'rows': args['rows'],
        'cursorMark': SolrBase.mark,
    }

    if 'migrate' in args:
        source_host = args['<source_host>']
        source_port = args['<source_port>']
        destination_host = args['<destination_host>']
        destination_port = args['<destination_port>']

        source_url = SolrBase.get_sorl_url(source_host, source_port, collection)
        destination_url = SolrBase.get_sorl_url(destination_host, destination_port, collection)

        solr_migrate = SolrMigrate(source_url, destination_url, collection, params=params)

        solr_migrate.migrate(params)

    elif 'search' in args:
        target_host = args['<target_host>']
        target_port = args['<target_port>']
        # host_url = args['<host_url>']
        # limit = args['--limit']
        params['indent'] = args['--indent']

        target_url = SolrBase.get_sorl_url(target_host, target_port, collection)

        solr_search = SolrSearch(target_url, collection, params=params)

        solr_search.exec_search()

    elif 'add' in args:
        print('Nothing yet.')
    elif 'delete' in args:
        print('Nothing yet.')
    elif 'update' in args:
        print('Nothing yet.')
    else:
        print('Dude RTFM!')

if __name__ == '__main__':
    print(time.localtime())

    args = docopt(__doc__)

    main(args)

    print(time.localtime())
