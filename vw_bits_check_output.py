#!/usr/bin/env python

"run vw with various bits settings, save reported losses to a csv file"
"subprocess.check_output() version"

import re
import csv
import subprocess

max_bits = 25
min_bits = 8

path_to_cache = 'data/vw/train.vw.cache'
output_file = 'data/vw_bits_amazon.csv'
vw_params = '--loss_function logistic --passes 20 -q ee --l2 0.0000005'

###

def get_loss( output ):
	pattern = 'average loss = ([0-9.e]+)\n'
	m = re.search( pattern, output )
	loss = m.group( 1 )
	return loss

###

o_f = open( output_file, 'wb' )
writer = csv.writer( o_f )
writer.writerow( [ 'bits', 'loss' ] )

for b in range( max_bits, min_bits - 1, -1 ):
	
	cmd = 'vw {} --cache_file {} -b {} 2>&1'.format( vw_params, path_to_cache, b )	
	print cmd
	
	output = subprocess.check_output( '{} | tee /dev/stderr'.format( cmd ), shell = True )
	loss = get_loss( output )
	
	print "\nbits: {}, loss: {}\n".format( b, loss )
	
	writer.writerow( [ b, loss ] )
	o_f.flush()
	
	
