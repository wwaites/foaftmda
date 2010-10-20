FOAF integration for TMDA
=========================

Put something like this in cron::

    0 0 * * * cat ~/.tmda/lists/whitelist ~/.tmda/lists/confirmed | mboxlist2foaf -m http://example.org/foaf#me -b http://example.org/whitelist > ~/public_html/whitelist.rdf
    0 0 * * * cat ~/.tmda/lists/whitelist ~/.tmda/lists/confirmed | mboxlist2foaf -m http://example.org/foaf#me -b http://example.org/whitelist -f n3 > ~/public_html/whitelist.n3

