from optparse import OptionParser
from hashlib import sha1
import sys, re

from rdflib.graph import Graph
from rdflib.namespace import Namespace, RDF
from rdflib.term import URIRef, Literal, BNode

FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class MboxList2Foaf(object):
    opt_parser = OptionParser(usage="""
Take a list of email addresses and turn them into an
RDF graph representing a foaf:Group
""")
    opt_parser.add_option("-c", "--config",
                          dest="config",
                          help="Configuration file")
    opt_parser.add_option("-d", "--debug",
                          dest="debug",
                          default=False,
                          action="store_true",
                          help="debug")
    opt_parser.add_option("-i", "--input",
                          dest="infile",
                          default="-",
                          help="Input file (default: stdin)")
    opt_parser.add_option("-o", "--output",
                          dest="outfile",
                          default="-",
                          help="Output file (default: stdout)")
    opt_parser.add_option("-f", "--format",
                          dest="format",
                          default="pretty-xml",
                          help="Output format (default: xml)")
    opt_parser.add_option("-b", "--base",
                          dest="base",
                          help="Base URI for output")
    opt_parser.add_option("-m", "--maker",
                          dest="maker",
                          help="Maker URI")
    config = {}
    def __init__(self):
        self.opts, self.args = self.opt_parser.parse_args()
        if self.opts.config:
            fp = open(self.opts.config)
            cfg = eval(fp.read())
            fp.close()
            self.config.update(cfg)
    def command(self):
        if self.opts.infile == "-":
            infile = sys.stdin
        else:
            infile = open(self.opts.infile)
        if self.opts.outfile == "-":
            outfile = sys.stdout
        else:
            outfile = open(self.opts.outfile, "w+")

        if self.opts.base:
            base = self.opts.base
        elif self.opts.outfile != "-":
            base = self.opts.outfile
        else:
            base = "http://example.org/mboxlist"

        if not base.endswith("#"):
            base = base + "#"

        BASE = Namespace(base)

        g = Graph()
        g.bind("foaf", FOAF)

        g.add((BASE["mboxlist"], RDF["type"], FOAF["Group"]))
        if self.opts.maker:
            maker = URIRef(self.opts.maker)
            g.add((BASE["mboxlist"], FOAF["maker"], maker))

        for line in infile.readlines():
            mbox = line.strip()
            if not mbox: continue

            member = BNode()
            g.add((BASE["mboxlist"], FOAF["member"], member))
            g.add((member, RDF["type"], FOAF["Agent"]))

            sha1sum = Literal(sha1("mailto:" + mbox).hexdigest())
            g.add((member, FOAF["mbox_sha1sum"], sha1sum))

        g.serialize(outfile, format=self.opts.format)

_from_re = re.compile("^.*<(?P<addr>.*)>")

class CheckFoaf(object):
    opt_parser = OptionParser(usage="""
Check incoming message headers (From) against an RDF
file containing foaf:mbox or foaf:mbox_sha1sum triples
""")
    opt_parser.add_option("-c", "--config",
                          dest="config",
                          help="Configuration file")
    opt_parser.add_option("-d", "--debug",
                          dest="debug",
                          default=False,
                          action="store_true",
                          help="debug")
    opt_parser.add_option("-i", "--input",
                          dest="infile",
                          default=None,
                          help="Trusted senders File")
    opt_parser.add_option("-f", "--format",
                          dest="format",
                          default="xml",
                          help="Trusted senders format (default: xml)")
    config = {}
    def __init__(self):
        self.opts, self.args = self.opt_parser.parse_args()
        if self.opts.config:
            fp = open(self.opts.config)
            cfg = eval(fp.read())
            fp.close()
            self.config.update(cfg)

    def command(self):
        assert self.opts.infile is not None, "Must specify an input file"

        g = Graph()
        fp = open(self.opts.infile)
        g.parse(fp, format=self.opts.format)
        fp.close()

        def check_mbox(mbox):
            print "Checking:", mbox
            for _x in g.triples((None, FOAF["mbox"], URIRef(mbox))):
                sys.exit(0)
            mbox_sha1sum = sha1(mbox).hexdigest()
            print "Checking", mbox_sha1sum
            for _x in g.triples((None, FOAF["mbox_sha1sum"], Literal(mbox_sha1sum))):
                sys.exit(0)

        for line in sys.stdin.readlines():
            line = line.strip()
            if line.startswith("From:"):
                header, val = line.split(":", 1)
                val = val.strip()
                m = _from_re.match(val)
                if m:
                    mbox = "mailto:" + m.groupdict()["addr"]
                    check_mbox(mbox)
                check_mbox("mailto:" + val)
        sys.exit(1)

def mboxlist2foaf():
    MboxList2Foaf().command()

def checkfoaf():
    CheckFoaf().command()
