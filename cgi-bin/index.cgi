#!/usr/bin/perl -w

=head1 NAME

index.cgi - Show the spam/ok stats.

=cut

=head1 ABOUT

This program outputs the global SPAM/GOOD stats by reading the
redis keys "global-spam" and "global-ok" respectively.

These stats are displayed upon the project's homepage via Ajax.

=cut

=head1 AUTHOR

 Steve
 --
 http://www.steve.org.uk/

=cut

=head1 LICENSE

Copyright (c) 2008-2013 by Steve Kemp.  All rights reserved.

This module is free software;
you can redistribute it and/or modify it under
the same terms as Perl itself.
The LICENSE file contains the full text of the license.

=cut




use strict;
use warnings;


use Redis;

my $r    = Redis->new();
my $spam = $r->get("global-spam") || 0;
my $ok   = $r->get("global-ok") || 0;
$r->quit();


print <<EOF;
Content-type: application/xml

<?xml version="1.0" ?>
<data>
<spam>
$spam
</spam>
<ham>
$ok
</ham>
</data>

EOF


#
#  All done
#
exit;
