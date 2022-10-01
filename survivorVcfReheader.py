#!/usr/bin/env python3

"""
--------------------------------------------------------------------------------
survivorVcfReheader.py: Tool to add sample legend to survivor's output
--------------------------------------------------------------------------------
"""


import argparse
import pysam
import sys


__version__='1.0.0'



def get_svroptions(argv):
    svrParser = argparse.ArgumentParser(
        usage='''survivorVcfReheader.py [options]
        
Tool to add sample legend to survivor's output
        '''
    )
    svrParser.add_argument(
        '--input_file',
        '-I',
        help='FILE Survivor\'s output file',
    )
    svrParser.add_argument(
        '--output_file',
        '-O',
        default='-',
        help='FILE New output file name',
    )
    svrParser.add_argument(
        '--source_files',
        '-S',
        nargs='+',
        default=['Delly_v0.8.1', 'Lumpy_v0.3.0', 'Manta_v1.4.0'],
        help='STR Name and versions of the programs',
    )
    return svrParser.parse_args(argv)


def reheader_vcf_files(options):
    tmp_fh = pysam.VariantFile(options.input_file, ignore_truncation=True)
    newHeader = tmp_fh.header
    samples_in = list(tmp_fh.header.samples)
    for sample_index in range(len(samples_in)):
        newHeader.add_meta(
            key = samples_in[sample_index] + '_source',
            value = options.source_files[sample_index])
    tmpVcfOut = pysam.VariantFile(options.output_file, 'w', header=newHeader)
    for rec in tmp_fh:
        tmpVcfOut.write(rec)

    tmpVcfOut.close()
#     if options.output_file != '-':
#         pysam.tabix_index(options.output_file, preset='vcf', force=True)


def no_flags():
    print('Please re-run the command with "-h" to get usage instructions and a\
 complete list of options\n')
    exit()


def validate_options(options):
    tmp_fh = pysam.VariantFile(options.input_file, ignore_truncation=True)
    samples_in = list(tmp_fh.header.samples)
    if len(samples_in) != len(options.source_files):
        raise ValueError('ERROR: Number of samples and input files must be the \
same')


def main():
    if len(sys.argv) == 1:
        no_flags()
    else:
        svrOpts=get_svroptions(sys.argv[1:])
        validate_options(svrOpts)
        reheader_vcf_files(svrOpts)
        exit(0)


if __name__=='__main__':
    exit(main())