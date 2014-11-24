#!/usr/bin/env python

"run vw with various bits settings, save reported losses to a csv file"
"os.system() version"

import os
import re
import csv

max_bits = 29
min_bits = 8

path_to_cache = 'data/vw/train.cache'
tmp_log_file = 'data/vw/tmp_log.txt'
output_file = 'data/vw_bits_kdd10b.csv'

###

def get_loss( output ):
	pattern = 'average loss = (.*?)\n'
	m = re.search( pattern, output )
	loss = m.group( 1 )
	return loss

###

o_f = open( output_file, 'wb' )
writer = csv.writer( o_f )
writer.writerow( [ 'bits', 'loss' ] )

for b in range( max_bits, min_bits - 1, -1 ):

	cmd = 'vw --loss_function logistic --cache_file {} -b {} 2>&1 | tee {}'.format( path_to_cache, b, tmp_log_file )
	os.system( cmd )

	output = open( tmp_log_file, 'r' ).read()
	loss = get_loss( output )
	
	# redirect stderr to tee, tee to stdout & stderr, catch stdout
	"""	
	cmd = 'vw --loss_function logistic --cache_file {} -b {} 2>&1'.format( path_to_cache, b )	
	output = subprocess.check_output( '{} | tee /dev/stderr'.format( cmd ), shell = True )
	loss = get_loss( output )
	"""
	
	print "\nbits: {}, loss: {}\n".format( b, loss )
	
	writer.writerow( [ b, loss ] )
	o_f.flush()
	
	