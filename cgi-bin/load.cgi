#!/usr/bin/perl
#
# User redis to show the recent spam/ham stats.
#

use strict;
use warnings;

use Redis;
use JSON;

my $r = new Redis();

#
# Get the entries.
#
my @stats = $r->smembers( "stats" );

#
# The data in JSON format.
#
my @array;
foreach my $ent ( @stats )
{
    push( @array, from_json( $ent ) );
}

#
# Sort by date-key
#
@array = sort { $a->{'epoch'} cmp $b->{'epoch'} } @array;

#
# Truncate
#
my $max = 15;
@array= ( $max >= @array) ? @array: @array[-$max .. -1];


#
#  Now turn into spam/ham
#
my @spam;
my @ham ;

foreach my $entry ( @array)
{
    push( @spam, $entry->{'spam'} );
    push( @ham, $entry->{'ham'} );

}

#
#  Show the output
#
print "Content-type: text/plain\n\n";
print "[";
print "[" . join( ",", @spam ) . "],";
print "[" . join( ",", @ham ) . "]";
print "]";


