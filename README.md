# simple_scripts

## Program Description

The simple_script program produces observing scripts for the GBT for
common types of simple observations.  Upon class initialization, it
creates an empty structure with the necessary observing
parameters. This structure is then filled in using a series of helper
functions. An example interface is given in get_user_parameters().

It currently supports pointed or mapping extragalactic neutral
hydrogen observations, but should be easily extendable to other common
observing modes (Galactic neutral hydrogen, ammonia mapping, pointed
water maser, and HCN/HCO+ pointed and mapping observations). This
routine does not take in account the redshift of the object for
determining the mapping parameters, so the mapping routines may
oversample because the beam is smaller at the rest frequency than it
is at the observed ("sky") frequency. The mapping routines could be
extended to take this into account. Astrid, however, does not provide
the sky frequency automatically; it would have to be calculated via
the usual definitions.

## Usage

This script will only works on GBT computers. You need to import the
GBT turtle libraries prior to running using the command "source
/home/gbt/sparrow/sparrow.bash". The script can then be executed in
Python using

ipython --pylab
execfile('simple_scripts.py')

get_user_parameters()

The get_user_parameters() routine takes as input a GBT project code
and GBT catalog file (see catalog_template.cat for an example and the
GBT Observer's Guide for more information). Then the program walks the
user through a series of simple questions about the observation to
produce the observing files. Observing files are created for each
target as well as a configuration file and an example focus
script. The resulting scripts can then be modified as necessary and
loaded into Astrid for observing. The configuration and catalog files
are assumed to reside in the same directory that get_user_parameters()
was called from. The output scripts are labeled with the project id and the source name (for target observations) or focus (for focus observations).

## Future improvements

* update to use VEGAS instead of the Spectrometer

* add in other types of observing including:
  * Galactic HI, 
  * ammonia mapping with KFPA, 
  * pointed water maser observations,  and
  * HCN/HCO+ pointed and mapping observations.

* generate the mapping parameters based on the sky frequency rather than the rest frequency

* generate AutoOOF scripts for high frequency observations.