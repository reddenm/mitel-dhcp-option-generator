#!/usr/bin/perl -w
# To make this script really ace....
# -Vendor selection radio buttons - look up other vendors to insert a different Vendor ID
#  and tailor the fields in the form so as to be relevent to that vendor. << Javascript
# -Use a 'from_option subroutine' to reverse the operation,
#  perhaps greying out the unused fields on the webpage. << Javascript
# -Include documentation telling how to use this.
# -Make available a command line tool to run directly on 'nix dhcp servers.
# -having multiple tftp servers doesn't seem to make any difference
#  the telephones ignore all but the first (as noticed in October 2013).
#---------------------------------------------------------------------------
#                              include packages
#---------------------------------------------------------------------------
use strict;
use CGI qw(:standard);
use warnings;
#---------------------------------------------------------------------------
# mitel-dhcp-option-generator
# - A web app to assist the auto-configuration of IP phones from vendor option 43 and 125 using 'nix and Windows dhcp servers
# by reddenm
#
# The format of the option is
#
# 00:00:04:03:xx:69:64:.......
# 00:00:04:03					specifies the vendor ID:- hex 403 = decimal 1027, which is Mitel's vendor ID
#            :4A:				is length of remaining string in hex, eg in this case hex 4A refers to 74 characters to follow
#               :69:64:.......	is hexed ASCII representation of the string, which always starts with 20 characters as id:ipphone.mitel.com,
#								so next 20 hex pairs, 6 - 25, are always the same.... 69:64:3A:69:70:70:.......:70:3D:34:36:3B
#								the actual option 125 configuration for the phones then follow after this.
#---------------------------------------------------------------------------
print header;
my @tftplist = param('tftp1');
if (param('tftp2')) {push (@tftplist, param('tftp2')) };
if (param('tftp3')) {push (@tftplist, param('tftp3')) };
if (param('tftp4')) {push (@tftplist, param('tftp4')) };
if (param('tftp5')) {push (@tftplist, param('tftp5')) };
if (param('tftp6')) {push (@tftplist, param('tftp6')) };
my $tftplist = join(',', @tftplist);

my @icplist = param('icp1');
if (param('icp2')) {push (@icplist, param('icp2')) };
if (param('icp3')) {push (@icplist, param('icp3')) };
if (param('icp4')) {push (@icplist, param('icp4')) };
my $icplist = join(',', @icplist);

my $option43string = "id:ipphone.mitel.com;sw_tftp=".$tftplist.";call_srv=".$icplist;

if (param('vlan')) {
                        my $vlan = param('vlan');
                        my $defaultl2p = param('defaultl2p'); my $medial2p = param('medial2p'); my $signalsl2p = param('signalsl2p');
                        $option43string = $option43string.";vlan=".$vlan.";l2p=".$defaultl2p."v"."$medial2p"."s".$signalsl2p;
                       }

my $defaultdscp = param('defaultdscp'); my $mediadscp = param('mediadscp'); my $signalsdscp = param('signalsdscp');
$option43string = $option43string.";dscp=".$defaultdscp."v"."$mediadscp"."s".$signalsdscp;

print	"<HTML>\n",
		" <HEAD>\n",
		"  <TITLE>dhcp option 43 string, and option 125 ASCII hex pair result</TITLE>\n",
		" </HEAD>\n",
		" <BODY>\n",
                "  <H1>dhcp option 43 string, and option 125 ASCII hex pair result</H1>",
		"  <P>\n";

print		"Your option 43 string is:<BR>\n",
                 $option43string, "<BR><BR>\n";

to_option($option43string);          # convert the string to hex values

sub to_option
{
	my ($s) = @_;	#@_ is perl's name of the passed arguments

    my @a = (qw(00 00 04 03));  # mitel vendor code is hex 0x403 (decimal 1027)

    push(@a, sprintf("%02X", length($s))); # 5th element is string length, push appends to list, sprintf("%02X",) creates as digit hex value

    push(@a, (map { sprintf("%02X", ord($_)) } split(m//, $s)));	#split feeds in each individual character, ord() converts chr to ascii code
																	# sprintf("%02X",) creates as digit hex value
																	# map evaulates each element of the list
	if (param('servertype') == "1")
		{
		print "In 'nix dhcp server format, your option 125 ASCII hex pair string is: <BR>\n";
		print join(':', @a);		# linux scope requires : as the hex pair separator
		}
	else
		{
		print "In Microsoft Windows dhcp server format, your option 125 ASCII hex pair string is: <BR>\n";
		print join('', @a);	# windows scope options config requires the string without any separating characters
		}
}
print "<BR>\n";
print "  </P>\n";
print " </BODY>\n";
print "</HTML>\n";
#---------------------------------------------------------------------------
# Local Variables:
# mode: perl
# End:
#---------------------------------------------------------------------------
