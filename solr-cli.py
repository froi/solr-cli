"""
    Usage:
        solr-cli search <host_url> <collection> (-q=<query> | --query=<query>) [options]
        solr-cli (add | update | delete) <host_url> <collection> (-q=<query> | --query=<query>) [options]
        solr-cli (-h | --help | --version)

    Options:
        -h --help               Show this screen.
        --version               Show version.
        -q=<q>, --query=<q>     Data payload to be sent to the server
        --wt=<wt>               [default: json]
        --indent=ind            Indent output (true or false).
                                [default: true]
        --limit=l               Limits output amount, pass `all` to get all records.
                                [dfault: 10]
        --commit=c              Commits action sent to the Solr server.
                                [dafault: false]
"""


import docopt

if __name__ == '__main__':
    args = docopt(__doc__)

    # Set all argument values
    host_url = args['<host_url']
    collection = args['collection']
    wt = args['--wt']
    query = args['-q'] if args['-q'] else args['--query']
    indent = args['--indent']
    limit = args['--limit']
    commit = True if args['--commit'] == 'true' else False
