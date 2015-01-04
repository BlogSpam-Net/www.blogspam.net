#!/usr/bin/perl -w

use strict;
use warnings;

use JSON;
use Redis;
use CGI;

binmode( STDOUT, ":utf8" );
my $cgi  = new CGI;
my $r    = new Redis;
my $json = JSON->new()->allow_nonref();



if ( $cgi->param("blacklist") )
{

    $r->set( "blacklist-" . $cgi->param("blacklist"),
             "Comment rejected by admin." );
    $r->expire( "blacklist-" . $cgi->param("blacklist"), 60 * 60 * 24 * 7 );

    print $cgi->redirect( -url => '/cgi-bin/admin/index.cgi' );
    exit;
}
elsif ( $cgi->param("trim") )
{
    $r->ltrim( "recent-comments", 0, 0 );
    print $cgi->redirect( -url => '/cgi-bin/admin/index.cgi' );
    exit;
}
else
{
    print "Content-type: text/html\n\n";

    my $out   = "";
    my $count = 0;

    my @ent = $r->lrange( "recent-comments", 0, -1 );
    foreach my $ent (@ent)
    {
        my $obj;
        eval {$obj = $json->decode($ent); $obj = $json->decode($obj)};
        next if ($@);

        #
        #  Get the IP and make sure it is sane.
        #
        my $ip = $obj->{ 'ip' };
        next unless ($ip);
        next if ( $ip =~ /,/ );
        next if ( $ip eq "127.0.0.1" );

        #
        #  Ignore some sites
        #
        next if ( ($obj) && ( $obj->{ 'site' } =~ /www.wejoinin.com/ ) );

        #
        #  Ignore comments that come from hosts we've already blacklisted.
        #
        my $blacklisted = $r->get("blacklist-$ip") || "";
        next if ( length($blacklisted) );

        #
        #  Ignore empty comments?
        #
        next unless ( length( $obj->{ 'comment' } ) > 0 );

        my $method = $obj->{ 'method' } || "JSON";


        $out .=
          "<p>$method <a href=\"/cgi-bin/admin/index.cgi?blacklist=$ip\">$ip</a> ";
        $out .= " - [Subject: $obj->{ 'subject' }]" if ( $obj->{ 'subject' } );
        $out .= "</p>";

        $out .= "<blockquote>\n";
        $out .= "<p>Link: $obj->{'link'}</p>" if ( $obj->{ 'link' } );
        $out .= "<p>Name: $obj->{'name'}</p>" if ( $obj->{ 'name' } );
        $out .= "<p>Site: $obj->{'site'}</p>" if ( $obj->{ 'site' } );
        $out .= $obj->{ 'comment' } if ( $obj->{ 'comment' } );
        $out .= "</blockquote>\n";

        $out .= "<p>&nbsp;</p>";

        $count += 1;
    }


    print
      "<html><head><meta http-equiv=\"refresh\" content=\"30\"><title>Admin [$count]</title></head><body>";
    print "<p><a href=\"/cgi-bin/admin/index.cgi?trim=1\">Trim</a></p>";
    print $out;
    print "</body></html";
}
