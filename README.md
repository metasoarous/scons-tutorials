# SCons for data science & computational biology tutorials

This repository contains code examples from the [SCons for data science and computational biology pipelines](https://www.metasoarous.com/scons-for-data-science-and-compbio/) post on [my blog](http://www.metasoarous.com).
For a full explanation, please see the introductory post.

In short though, SCons is a build tool (akin to make) which uses python to construct build scripts.
These build scripts are valuable for data scientists and computational biologists as a tool for iteratively specifying the structure of a complex analysis with many individual components.
It offers the following advantages over either running individual programs/analyses one at a time or via a shell script:

1. Reproducibility: it's easier to reproduce research when you have a script that runs everything for you
2. Once you get things working, you can hit go and walk away
3. If you update one of the intermediate results, only the downstream results will be updated on subsequent builds, saving time
4. Running independent steps in parallel becomes a snap


## How to run the examples

First install the prerequisites.
If you are running Ubuntu, you can simple run `./install_prereqs.sh`.
(If you are on OSX and feel like specifying a suitable setup with `homebrew` et al., please be my guest)
Note that you will be asked for your password for permission to run `apt-get install` and `sudo pip install`.
If you're paranoid, take a look at the script for yourself to make sure there is no funny business, or just install the various libraries manually.

Once that's out of the way, you should be able to `cd` into an `example*` directory and run `scons` to build the given analysis.
And that's it!
The files produced by the analysis should be in the `output` directory of your `example` directory.

## The data

The [sequence data](https://github.com/metasoarous/scons-tutorials/blob/master/input/sequences.fasta) was obtained from a GenBank submission of Shiino et al., 2012.


