#!/usr/bin/env python

import csv
import colorbrewer
import warnings
import argparse
from Bio import Phylo
import matplotlib

# Necessary to run without a DISPLAY variable
matplotlib.use('Agg')

import pylab



def build_parser(parser):
    parser.add_argument('tree',
            help='Tree you want to load')
    # Should allow for alternative node column
    parser.add_argument('metadata',
            help="""csv file mapping tree nodes to a colorable trait. Tree node
            column should be named 'sequence'""",
            type=argparse.FileType('r'))
    parser.add_argument('out', help='filename for PhyloXML output')

    # Should make this just use the first non-sequence column by default
    parser.add_argument('--color-by',
            help='Specify the column you want to color by', required=True)
    # Would be nice to allow for passing in a of manual color map
    parser.add_argument('--palette',
            help='Specify a colorbrewer pallete name (default: %(default)s)',
            default='RdYlBu')
    parser.add_argument('--tree-format',
            help='Input tree format (default: %(default)s)',
            default='newick')


def action(args):
    # Will need to make format an option here if we ever need to
    tree = Phylo.read(args.tree, args.tree_format)
    meta = csv.DictReader(args.metadata)
    color_map = color_mapping(meta, args.color_by, args.palette)
    legend = color_map['by_group']
    sequence_mapping = color_map['by_sequence']

    # Write out the tree
    tree = apply_color_mapping(tree, sequence_mapping)
    Phylo.write(tree, args.out, 'phyloxml')

    # Write out our legend
    leg_handle = open(args.out + '.legend', 'w')
    write_color_legend(legend, leg_handle, args.color_by)

    # close up shop
    leg_handle.close()
    args.metadata.close()


def __color_iterator(groups, palette, group_mapping = {}):
    n_groups = len(groups)
    try:
        colors = palette[n_groups]
    except KeyError:
        m = min(palette.keys())
        # Should only happen if n = 1 or 2
        if n_groups < m:
            p = palette[m]
            colors = [p[0]]
            if n_groups == 2:
                colors.append(p[2])
        else:
            if group_mapping == {}:
                # Only want to warn once...
                warnings.warn("""Coloring more trait classes than there are colors in this palette - reusing
                colors""", Warning)
            colors = palette[max(palette.keys())]

    for i, color in enumerate(colors):
        group_mapping[groups[i]] = color

    if len(groups) > len(colors):
        return __color_iterator(groups[len(colors):], palette, group_mapping)
    else:
        return group_mapping


def color_mapping(metadata_reader, color_by, palette_name='RdYlBu'):
    metadata = list(metadata_reader)
    groups = list(set(map(lambda x: x[color_by], metadata)))
    groups.sort()

    try:
        palette = getattr(colorbrewer, palette_name)
    except AttributeError:
        raise "Unable to find colorbrewer palette {}".format(palette_name)
    group_mapping = __color_iterator(groups, palette)


    sequence_mapping = {}
    for sequence in metadata:
        sequence_mapping[sequence['sequence']] = group_mapping[sequence[color_by]]

    return {'by_group': group_mapping, 'by_sequence': sequence_mapping}


def apply_color_mapping(tree, sequence_mapping):
    tree = tree.as_phyloxml()
    missing = []
    for term in tree.get_terminals():
        try:
            term.color = sequence_mapping[term.name]
        except KeyError:
            missing.append(term.name)

    if len(missing) > 0:
        warnings.warn("Missing color(s) for: " + str(missing))

    return tree


def write_color_legend(legend, handle, color_by):
    leg_writer = csv.writer(handle)
    leg_writer.writerow([color_by, 'color'])
    # Doing it this way so that the order of printing is in the order that the
    # colors are assigned
    members = legend.keys()
    members.sort()
    for member in members:
        leg_writer.writerow([member, legend[member]])


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tree',
            help='Tree you want to load')
    # Should allow for alternative node column
    parser.add_argument('metadata',
            help="""csv file mapping tree nodes to a colorable trait. Tree node
            column should be named 'sequence'""",
            type=argparse.FileType('r'))
    parser.add_argument('out', help='filename')

    parser.add_argument('-I', '--image-out', action="store_true",
            help="""The default output is a PhyloXML file with colored node information. This flag triggers
            instead rendering to a PDF file.""")
    # Should make this just use the first non-sequence column by default
    parser.add_argument('-c', '--color-by',
            help='Specify the column you want to color by', required=True)
    # Would be nice to allow for passing in a of manual color map
    parser.add_argument('-p', '--palette',
            help='Specify a colorbrewer2.org pallete name (default: %(default)s)',
            default='RdYlBu')
    parser.add_argument('-f', '--tree-format',
            help='Input tree format (default: %(default)s)',
            default='newick')

    return parser.parse_args()


def main(args):
    # Will need to make format an option here if we ever need to
    tree = Phylo.read(args.tree, args.tree_format)
    meta = csv.DictReader(args.metadata)
    color_map = color_mapping(meta, args.color_by, args.palette)
    legend = color_map['by_group']
    sequence_mapping = color_map['by_sequence']

    # Write out the tree
    tree = apply_color_mapping(tree, sequence_mapping)
    if args.image_out:
        Phylo.draw_graphviz(tree)
        pylab.show()
        pylab.savefig(args.out)
    else:
        Phylo.write(tree, args.out, 'phyloxml')

    # Write out our legend
    leg_handle = open(args.out + '.legend', 'w')
    write_color_legend(legend, leg_handle, args.color_by)

    # close up shop
    leg_handle.close()
    args.metadata.close()


if __name__ == "__main__":
    args = get_args()
    main(args)


