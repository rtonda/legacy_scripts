#!/usr/bin/env perl

package DAT_common;

use strict;
use warnings;

use Carp;
use Exporter;
our @ISA = qw(Exporter);
our @EXPORT_OK = qw(check_mandatory_args get_input read_file set_output write_file);
our @EXPORT = qw(check_mandatory_args get_input read_file set_output write_file);

our $VERSION='1.0.0';


####################################################
#                      Input                       #
####################################################

sub get_input {
    my $input_source=shift;
    my $input_fh;
    if ((!defined $input_source)||($input_source eq '-')||($input_source eq 'STDIN')) {
        $input_fh=*STDIN;
    }
    else {
        $input_fh=read_file($input_source);
	}
	return ($input_fh);
};

sub read_file{
	my $filename=shift;
	my $filename_fh;
    #if (!-e $filename_fh) {croak "ERROR: Couldn't find $filename.\n"}
	if ($filename =~ m/\.gz$/){
		open ($filename_fh, "gunzip -c $filename|") or croak "ERROR: Couldn't open $filename\n\n";
	}
	else {
		open ($filename_fh, '<', $filename) or croak "ERROR: Couldn't open $filename\n\n";
	};
	return ($filename_fh);
};


####################################################
#                     Output                       #
####################################################

sub set_output {
    my $output_destination=shift;
    my $output_fh;
    if ((!defined $output_destination)||($output_destination eq '-')||($output_destination eq 'STDOUT')) {
        $output_fh=*STDOUT;
    }
    else {
        $output_fh=write_file($output_destination);
	}
	return ($output_fh);
};

sub write_file{
	my $filename=shift;
    my $tabix_path='/apps/TABIX/0.2.6/bin';
	my $filename_fh;
	if ($filename =~ m/\.gz$/){
        open ($filename_fh, "| ${tabix_path}/bgzip -c > $filename; ${tabix_path}/tabix -p vcf $filename") or croak "ERROR: Couldn't save in $filename\n\n";
	}
    elsif ($filename =~ m/\.gz$/){
        open ($filename_fh, "| gzip -c > $filename") or croak "ERROR: Couldn't save in $filename\n\n";
    }
	else {
		open ($filename_fh, ">$filename") or croak "ERROR: Couldn't save in $filename\n\n";
	};
	return ($filename_fh);
};


####################################################
#                   Subroutines                    #
####################################################

sub check_mandatory_args {
	my %args=(
		mand_args=>undef,
		method_name=>undef,
		passed_args=>undef,
		usage=>undef,
		@_,
	);

	if (!defined $args{mand_args}) {croak "\nERROR: \'mand_args\' is a mandatory parameter to execute check_mandatory_args.\n"};
	if (!defined $args{method_name}) {croak "\nERROR: \'method_name\' is a mandatory parameter to execute check_mandatory_args.\n"};
	if (!defined $args{passed_args}) {croak "\nERROR: \'passed_args\' is a mandatory parameter to execute check_mandatory_args.\n"};
	if (!defined $args{usage}) {$args{usage}=''};
	foreach my $a(@{$args{mand_args}}) {
		if (!defined ${$args{passed_args}}{$a}) {croak "\nERROR: \'$a\' is a mandatory parameter to execute $args{method_name}.\n$args{usage}"};
	};
    return;
};


1
