#!/usr/bin/env python3

'''
--------------------------------------------------------------------------------
sigprofilersinglesample.py: Script to use SigProfilerSingleSample
--------------------------------------------------------------------------------
'''

import argparse
import os
import sys

from sigproSS import spss


__version__ = '1.0.0'


def get_rspssoptions(argv):
    rspss_parser = argparse.ArgumentParser(
        description='Script to use SigProfilerSingleSample',
        usage='sigprofilersinglesample.py [options]',
    )
    mandatoryrspssp = rspss_parser.add_argument_group('Mandatory arguments')
    mandatoryrspssp.add_argument(
        '--input_dir',
        '-I',
        help='PATH Path to the input files',
        required=True,
    )
    rspss_parser.add_argument(
        '--output_dir',
        '-O',
        default='.',
        help='PATH Path to the results folder',
    )
    rspss_parser.add_argument(
        '--reference_genome',
        '-G',
        choices=['GRCh37', 'GRCh38'],
        default='GRCh37',
        help='STR Reference genome to use',
    )
    rspss_parser.add_argument(
        '--restrict_to_exome',
        '-E',
        action='store_true',
        help='BOOL Restrict analysis to exome',
    )
    rspss_parser.add_argument(
        '--debug',
        '-D',
        action='store_true',
        help='BOOL Print options values and exit',
    )
    return rspss_parser.parse_args(argv)


def run_sigProfilerSingleSample(options):
    spss.single_sample(options.input_dir,
                       options.output_dir,
                       ref=options.reference_genome,
                       exome=options.restrict_to_exome)


def no_flags():
    print('Please re-run the command with "-h" to get usage instructions and a\
 complete list of options\n')
    exit()


def validate_options(options):
    options.input_dir = os.path.abspath(options.input_dir)
    options.output_dir  = os.path.abspath(options.output_dir)
    if options.restrict_to_exome is False:
        options.output_dir = options.output_dir + '/notRestrictedExome'
    else:
        options.output_dir = options.output_dir + '/restrictedExome'
    if options.debug is True:
        print(options)
        exit()


def main():
    if len(sys.argv) == 1:
        no_flags()
    elif len(sys.argv) > 1:
        spss_opts = get_rspssoptions(sys.argv[1:])
        validate_options(spss_opts)
        run_sigProfilerSingleSample(spss_opts)
        sys.exit(0)


if __name__ == '__main__':
    exit(main())
