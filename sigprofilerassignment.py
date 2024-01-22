#!/usr/bin/env python3
'''
--------------------------------------------------------------------------------
sigprofilerassignment.py: Enables assignment of previously known mutational
signatures to individual samples and individual somatic mutations.
--------------------------------------------------------------------------------
'''

import argparse
import os
import sys
from SigProfilerAssignment import Analyzer as Analyze
import sigprofilertoolscommon as sptc


__version__ = '1.0.0'


def get_sigprofilerassignment_options(argv):
    spa_parser = argparse.ArgumentParser(
        description='Enables assignment of previously known mutational \
signatures to individual samples and individual somatic mutations.',
        usage='SigProfilerTools SigProfilerAssignment [options]',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    mandatory_spap = spa_parser.add_argument_group('Mandatory arguments')
    mandatory_spap.add_argument(
        '--samples',
        '-S',
        help='PATH Path to the input somatic mutations file (if using segmenta\
tion file/mutational matrix) or input folder (mutation calling file/s).',
        required=True,
    )
    spa_parser.add_argument(
        '--output',
        '-O',
        help='PATH Path to the output folder.',
    )
    spa_parser.add_argument(
        '--input_type',
        '-it',
        choices=['vcf', 'seg:ASCAT', 'seg:ASCAT_NGS', 'seg:SEQUENZA',
                 'seg:ABSOLUTE', 'seg:BATTENBERG', 'seg:FACETS', 'seg:PURPLE',
                 'seg:TCGA', 'matrix'],
        default='vcf',
        help='STR Aaccepted input types.',
    )
    spa_parser.add_argument(
        '--context_type',
        '-ct',
        choices=['96', '288', '1536', 'DINUC', 'ID'],
        default='96',
        help='STR Required context type if input_type is "vcf". context_type\
 takes which context type of the input data is considered for assignment.',
    )
    spa_parser.add_argument(
        '--cosmic_version',
        '-cv',
        choices=[1, 2, 3, 3.1, 3.2, 3.3],
        default=3.3,
        help='FLOAT Defines the version of the COSMIC reference signatures.',
    )
    spa_parser.add_argument(
        '--exome',
        '-E',
        action='store_true',
        help='BOOL Defines if the exome renormalized COSMIC signatures will\
 be used.',
    )
    spa_parser.add_argument(
        '--genome_build',
        '-gb',
        choices=['GRCh37', 'GRCh38', 'mm9', 'mm10', 'rn6'],
        default='GRCh37',
        help='STR The reference genome build, used for select the appropriate\
 version of the COSMIC reference signatures, as well as processing the\
 mutation calling file/s.',
    )
    spa_parser.add_argument(
        '--signature_database',
        '-sdb',
        help='PATH Path to the input set of known mutational signatures (only\
 in case that COSMIC reference signatures are not used), a tab delimited file\
 that contains the signature matrix where the rows are mutation types and\
 columns are signature IDs. Dataframe. This is signature catalogue where the\
 row index will be the names of mutations and the column names will be the\
 sample names. The sum of each column should be one. The row numbers should\
 be equal to the row the number of the mutational catalogue and the\
 order/sequence of the mutation types should be same as of those in the\
 mutational catalogue.',
    )
    spa_parser.add_argument(
        '--exclude_signature_subgroups',
        '-ess',
        nargs='+',
        choices=['MMR_deficiency_signatures', 'POL_deficiency_signatures',
                 'HR_deficiency_signatures' , 'BER_deficiency_signatures',
                 'Chemotherapy_signatures', 'Immunosuppressants_signatures',
                 'Treatment_signatures', 'APOBEC_signatures',
                 'Tobacco_signatures', 'UV_signatures', 'AA_signatures',
                 'Colibactin_signatures', 'Artifact_signatures',
                 'Lymphoid_signatures'],
        default=[],
        help='LIST Removes the signatures corresponding to specific subtypes\
 to improve refitting (only available when using default COSMIC reference\
 signatures). The usage is explained at\
 https://github.com/AlexandrovLab/SigProfilerAssignment#-signature-subgroups.',
    )
    spa_parser.add_argument(
        '--export_probabilities',
        '-ep',
        action='store_false',
        help='BOOL Defines if the probability matrix per mutational context\
 for all samples is created.',
    )
    spa_parser.add_argument(
        '--export_probabilities_per_mutation',
        '-eppm',
        action='store_true',
        help='BOOL Defines if the probability matrices per mutation for all\
 samples are created. Only available when input_type is "vcf".',
    )
    spa_parser.add_argument(
        '--make_plots',
        '-P',
        action='store_false',
        help='BOOL Toggle on and off for making and saving plots.',
    )
    spa_parser.add_argument(
        '--sample_reconstruction_plots',
        '-srp',
        choices=['pdf', 'png', 'both'],
        default=None,
        help='STR Select the output format for sample reconstruction plots.',
    )
    spa_parser.add_argument(
        '--verbose',
        '-V',
        action='store_true',
        help='BOOL Prints detailed statements.',
    )
    return spa_parser.parse_args(argv)


def run_sigprofilerassignment_analyses(options):
    Analyze.cosmic_fit(
        options.samples,
        options.output,
        input_type=options.input_type,
        context_type=options.context_type,
        exome=options.exome,
        genome_build=options.genome_build,
        cosmic_version=options.cosmic_version,
        signature_database=options.signature_database,
        exclude_signature_subgroups=options.exclude_signature_subgroups,
        export_probabilities=options.export_probabilities,
        export_probabilities_per_mutation=options.export_probabilities_per_mutation,
        make_plots=options.make_plots,
        sample_reconstruction_plots=options.sample_reconstruction_plots,
        signatures=None,
        nnls_add_penalty=0.05,
        nnls_remove_penalty=0.01,
        initial_remove_penalty=0.05,
        collapse_to_SBS96=options.collapse_to_SBS96,
        connected_sigs=True,
        verbose=options.verbose,
        devopts=None)
    

def validate_options(options):
    options.samples = os.path.abspath(options.samples)
    options.output = os.path.abspath(options.output)
    if not os.path.exists(options.output):
        os.makedirs(options.output)
    if options.context_type == '96':
        options.collapse_to_SBS96 = True
    else:
        options.collapse_to_SBS96 = False


def main():
    if len(sys.argv) == 1:
        sptc.no_flags()
    elif len(sys.argv) > 1:
        SPA_opts = get_sigprofilerassignment_options(sys.argv[1:])
        validate_options(SPA_opts)
        run_sigprofilerassignment_analyses(SPA_opts)
        sys.exit(0)


if __name__ == '__main__':
    exit(main())
