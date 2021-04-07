#!/usr/bin/env python3

'''
--------------------------------------------------------------------------------
sigprofilerextractor.py: Script to use SigProfilerExtractor
--------------------------------------------------------------------------------
'''

import argparse
import os
import sys

from SigProfilerExtractor import sigpro as sig


__version__ = '1.0.0'


def get_rspeoptions(argv):
    rspe_parser = argparse.ArgumentParser(
        description='Script to use SigProfilerExtractor',
        usage='sigprofilerextractor.py [options]',
    )
    mandatoryrspep = rspe_parser.add_argument_group('Mandatory arguments')
    mandatoryrspep.add_argument(
        '--input_dir',
        '-I',
        help='PATH Path to the input files',
        required=True,
    )
    rspe_parser.add_argument(
        '--output_dir',
        '-O',
        default='.',
        help='PATH Path to the results folder',
    )
    rspe_parser.add_argument(
        '--file_type',
        '-T',
        choices=['vcf'],
        default='vcf',
        help='STR Type of input files',
    )
    rspe_parser.add_argument(
        '--reference_genome',
        '-G',
        choices=['GRCh37', 'GRCh38'],
        default='GRCh37',
        help='STR Reference genome to use',
    )
    rspe_parser.add_argument(
        '--minimum_signatures',
        '-m',
        type=int,
        default=1,
        help='INT Minimum number of signatures to extract',
    )
    rspe_parser.add_argument(
        '--maximum_signatures',
        '-M',
        type=int,
        default=5,
        help='INT Maximum number of signatures to extract',
    )
    rspe_parser.add_argument(
        '--nmf_replicates',
        '-N',
        type=int,
        default=100,
        help='INT Number of replicates',
    )
    rspe_parser.add_argument(
        '--restrict_to_exome',
        '-E',
        action='store_true',
        help='BOOL Restrict analysis to exome',
    )
    rspe_parser.add_argument(
        '--make_decomposition_plots',
        '-P',
        action='store_true',
        help='BOOL Make decomposition plots',
    )
    return rspe_parser.parse_args(argv)


def run_sigProfilerExtractor(options):
    sig.sigProfilerExtractor(options.file_type,
                             options.output_dir,
                             options.input_dir,
                             reference_genome=options.reference_genome,
                             opportunity_genome=options.reference_genome,
                             exome=options.restrict_to_exome,
                             minimum_signatures=options.minimum_signatures,
                             maximum_signatures=options.maximum_signatures,
                             nmf_replicates=options.nmf_replicates,
                             make_decomposition_plots=options.make_decomposition_plots)


def no_flags():
    print('Please re-run the command with "-h" to get usage instructions and a\
 complete list of options\n')
    exit()


def validate_options(options):
    options.input_dir = os.path.abspath(options.input_dir)
    options.output_dir  = os.path.abspath(options.output_dir)
    if options.restrict_to_exome is False:
        options.output_dir = options.input_dir + '/notRestrictedExome'
    else:
        options.output_dir = options.input_dir + '/restrictedExome'
    if options.minimum_signatures > options.maximum_signatures:
        raise ValueError('ERROR: the value of the option minimum_signatures\
 must be smaller than the value of the option maximum_signatures')


def main():
    if len(sys.argv) == 1:
        no_flags()
    elif len(sys.argv) > 1:
        spe_opts = get_rspeoptions(sys.argv[1:])
        validate_options(spe_opts)
        compute_coronary_heart_disease_risk(spe_opts)
        sys.exit(0)


if __name__ == '__main__':
    exit(main())
