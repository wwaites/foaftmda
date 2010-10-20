FOAF integration for TMDA
=========================

  * Source code: http://github.com/wwaites/foaftmda
  * PyPI: http://pypi.python.org/pypi/foaftmda

Put something like this in cron::

    0 0 * * * cat ~/.tmda/lists/whitelist ~/.tmda/lists/confirmed | \
        mboxlist2foaf -m http://example.org/foaf#me \
        -b http://example.org/whitelist > ~/public_html/whitelist.rdf
    0 0 * * * cat ~/.tmda/lists/whitelist ~/.tmda/lists/confirmed | \
        mboxlist2foaf -m http://example.org/foaf#me \
        -b http://example.org/whitelist -f n3 > ~/public_html/whitelist.n3

(lines wrapped for readability)

And if you have an RDF file, perhaps built from various sources
that you want to check to authorize mail, you can do put the 
following in your *~/.tmda/filters/incoming*::

    pipe-headers "checkfoaf -i /some/where/bigwhitelist.rdf" accept


