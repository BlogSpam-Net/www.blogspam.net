#!/usr/bin/perl -w

=head1 NAME

index.cgi - Show the spam/ok stats.

=cut

=head1 ABOUT

This program outputs the global SPAM/GOOD stats by requesting them
from our BlogSPAM API.

We do this because the back-end shouldn't have any implementation
knowledge about the service itself.

=cut

=head1 AUTHOR

 Steve
 --
 http://www.steve.org.uk/

=cut

=head1 LICENSE

Copyright (c) 2008-2017 by Steve Kemp.  All rights reserved.

This module is free software;
you can redistribute it and/or modify it under
the same terms as Perl itself.
The LICENSE file contains the full text of the license.

=cut




use strict;
use warnings;

use JSON;
use LWP::UserAgent;


#
# Create the helper.
#
my $ua = LWP::UserAgent->new;
$ua->timeout(10);
$ua->env_proxy;

#
# Make the request, and show any errors.
#
my $response = $ua->get('http://test.blogspam.net:9999/global-stats');

if ( !$response->is_success )
{
    print $response->status_line;
    exit(0);
}

#
# Decode the JSON
#
my $obj = decode_json( $response->decoded_content() );

print <<EOF;
Content-type: application/xml

<?xml version="1.0" ?>
<data>
<spam>
$obj->{'spam'}
</spam>
<ham>
$obj->{'ok'}
</ham>
</data>

EOF


#
#  All done
#
exit;
