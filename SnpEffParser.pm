#!/usr/bin/env perl

package SnpEffParser;

use Carp;
use Moose;
use Vcf;

our $VERSION='1.0.1';

my %known_aliases=(
        'AA.length'=>'aa_length',
        'AA.pos'=>'aa_pos',
        'AA.pos/AA.length'=>'aa_pos_length',
        Allele=>'alt_allele_number',
        Amino_Acid_change=>'aa_change',
        Amino_Acid_Change=>'aa_change',
        Amino_Acid_length=>'aa_length',
        Annotation=>'effect',
        Annotation_Impact=>'impact',
        'cDNA.length'=>'cdna_length',
        'cDNA.pos'=>'cdna_pos',
        'cDNA.pos/cDNA.length'=>'cdna_pos_length',
        'CDS.length'=>'cds_length',
        'CDS.pos'=>'cds_pos',
        'CDS.pos/CDS.length'=>'cds_pos_length',
        Coding=>'coding',
        Codon_Change=>'codon_change',
        Distance=>'distance',
        Effect=>'effect',
        Effect_Impact=>'impact',
        Effefct_Impact=>'impact',
        ERRORS=>'errors',
        'ERRORS/WARNINGS/INFO'=>'errors_warnings_info',
        Exon=>'exon',
        Exon_Rank=>'exon',
#        Feature_ID=>'feature',
#        Feature_Type=>'transcript',
        Feature_ID=>'transcript',
        Feature_Type=>'feature',
        Functional_Class=>'class',
        Gene_BioType=>'biotype',
        Gene_Coding=>'coding',
        Gene_ID=>'geneid',
        Gene_Name=>'gene',
        Genotype_Number=>'alt_allele_number',
        'HGVS.c'=>'hgvsc',
        'HGVS.p'=>'hgvsp',
        INFO=>'info',
        Rank=>'exon',
        Transcript=>'transcript',
        Transcript_BioType=>'biotype',
        Transcript_ID=>'transcript',
        WARNINGS=>'warnings',
);

#Object internals
has 'Alias'=>(
    traits  => ['Hash'],
    is      => 'rw',
    isa     => 'HashRef[Str]',
    default => sub { { } },
    handles => {
        exists_in_Alias => 'exists',
        ids_in_Alias    => 'keys',
        get_alias       => 'get',
        set_alias       => 'set',
    },
);

has 'AliasedIndex'=>(
    traits  => ['Hash'],
    is      => 'rw',
    isa     => 'HashRef[Str]',
    default => sub { { } },
    handles => {
        exists_in_aliasedindex => 'exists',
        ids_in_aliasedindex    => 'keys',
        get_aliasedindex       => 'get',
        set_aliasedindex       => 'set',
    },
);

has 'Author'=>(is=>'rw',isa=>'Str');

has 'Build'=>(is=>'rw',isa=>'Str');

has 'Command'=>(is=>'ro',isa=>'Str');

has 'Format'=>(is=>'rw',isa=>'ArrayRef');

has 'Index'=>(
    traits  => ['Hash'],
    is      => 'rw',
    isa     => 'HashRef[Str]',
    default => sub { {} },
    handles => {
        exists_in_index => 'exists',
        ids_in_index    => 'keys',
        get_index       => 'get',
        set_index       => 'set',
    },
);

has 'Raw_format'=>(is=>'ro',isa=>'Str');

has 'Type'=>(is=>'ro',isa=>'Str');

has 'vcf'=>(is=>'ro',isa=>'Vcf');

has 'Version'=>(is=>'ro',isa=>'Str');

around BUILDARGS=>sub {
    my $orig=shift;
    my $class=shift;
    my $args=shift; #other arguments passed in (if any).
    confess "No vcf object found in BUILDARGS" unless defined $args->{vcf};

    if (scalar(@{$args->{vcf}->get_header_line(key=>'INFO',ID=>'EFF')})==0 && scalar(@{$args->{vcf}->get_header_line(key=>'INFO',ID=>'ANN')})==0) {
        croak "ERROR: The provided vcf file does not have EFF or ANN annotations.\n"
    }
    elsif (scalar(@{$args->{vcf}->get_header_line(key=>'INFO',ID=>'EFF')})>=1 && scalar(@{$args->{vcf}->get_header_line(key=>'INFO',ID=>'ANN')})>=1) {
        croak "ERROR: The provided vcf file has EFF and ANN annotations.\n"
    }
    else {
        if (scalar(@{$args->{vcf}->get_header_line(key=>'INFO',ID=>'EFF')})>=1) {
            $args->{Type}='EFF'
        }
        else {
            $args->{Type}='ANN'
        }
    };
    my $raw_format=${$args->{vcf}->get_header_line(key=>'INFO',ID=>$args->{Type})}[0]{Description};
    $args->{Raw_format}=$raw_format;
    $raw_format=~m/'(.*)'/g;
    $raw_format=$1;
    my @format=split(/\(|\|/,$raw_format);
    for my $field_counter(0..$#format) {
        $format[$field_counter]=~s/\s*//gmx;
        $format[$field_counter]=~s/\)|\[|\]//gmx;
        $args->{Index}->{$format[$field_counter]}=$field_counter;
        $args->{Alias}->{$format[$field_counter]}=$known_aliases{$format[$field_counter]};
        $args->{AliasedIndex}->{$known_aliases{$format[$field_counter]}}=$field_counter;
    }        
    $args->{Format}=\@format;
    my $cmd=${$args->{vcf}->get_header_line(key=>'SnpEffCmd')}[0][0]{value};
    $cmd=~s/\"//gmx;
    $args->{Command}=$cmd;

    my $raw_version=${$args->{vcf}->get_header_line(key=>'SnpEffVersion')}[0][0]{value};
    $raw_version=~s/\"//gmx;
    $raw_version=~qr/(.*) \(build (.*)\)\, by (.*)/;
    $args->{Version}=$1;
    $args->{Build}=$2;
    $args->{Author}=$3;
    
    return $class->$orig($args);
};

sub get_all_effects_array {
    my $self=shift;
    my $allEff2parse=shift;
    $allEff2parse=~s/$self->Type()=//gmx;
    my @allEffects=split(/,/,$allEff2parse);
    return @allEffects;
}

sub get_allele {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'allele')
}

sub get_annotation {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'annotation')
}

sub get_byAlias {
    my $self=shift;
    my $eff2parse=shift;
    my $alias=shift;
    if (!$self->exists_in_aliasedindex($alias)) {croak "ERROR: There is not information associated to the alias $alias.\n"};
    return $$eff2parse[$self->get_aliasedindex($alias)];
}

sub get_biotype {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'biotype')
}

sub get_coding {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'coding')
}

sub get_eff_array {
    my $self=shift;
    my $str2parse=shift;
    my @eff_array = ref($str2parse) eq '' ? split(/\(|\|/,$str2parse)
                  : ref($str2parse) =~ /ARRAY/ ?  @{$str2parse}
                  :                     croak "ERROR: Wrong type\n";                       
    map {s/\)//gmx} @eff_array;
    return @eff_array;
}

sub get_effect {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'effect')
}

sub get_errors {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'errors')
}

sub get_errors_warnings_info {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'errors_warnings_info')
}

sub get_feature {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'feature')
}

sub get_functional_class {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'functional_class')
}

sub get_gene {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'gene')
}

sub get_impact {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'impact')
}

sub get_transcript {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'transcript')
}

sub get_warnings {
    my $self=shift;
    my $eff2parse=shift;
    $self->get_byAlias($eff2parse,'warnings')
}

no Moose;
__PACKAGE__->meta->make_immutable;

1
