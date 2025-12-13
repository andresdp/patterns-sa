import os, sys
import itertools
import random
import xml.etree.ElementTree as et
from multiprocessing import Pool, Lock
import time
#sys.path.insert(1, '../')
#from varEnv import * # To import *jmtpath* and *NUM_SIM_THREADS*

NUM_SIM_THREADS = 10 # Number of parallel simulations to run
#JMTPATH = './JMT-1.2.0.jar' # Path of the JMT JAR file
JMTPATH  = '/Users/adiazpace/Documents/my-research/performance-models-cdp/JMT-singlejar-1.2.2.jar'
PATH = './Backends_for_Frontends/'


def genModel(idx, source, params, modelName):
	placeholderName = PATH + 'model.placeholder.jsimg'
	with open(placeholderName, 'r') as f:
		filedata = f.read()
	for s, p in zip(source, params):
		filedata = filedata.replace(s, str(p))
	filedata = filedata.replace(placeholderName, modelName)
	with open(modelName, 'w') as f:
		f.write(filedata)
			
			
def runSim(idx, source, params, outfile):
	modelName = 'model' + str(idx) + '.jsimg'
	resultName = modelName + '-result.jsim'
	genModel(idx, source, params, modelName)
	rnd = str(random.randint(0, sys.maxsize))
	cmd = 'java -cp ' + JMTPATH + ' jmt.commandline.Jmt sim ' + modelName + ' -seed ' + rnd
	start_time = time.time()
	os.popen(cmd).read()
	end_time = time.time()
	collectResults(params, resultName, end_time - start_time, outfile)
	os.popen('rm ' + modelName + ' ' + resultName)
		
		
def collectResults(params, resultName, sim_time, outfile):
	tree = et.parse(resultName)
	root = tree.getroot()
	strAttrVals = ','.join([str(p) for p in params])
	for measure in root:
		dictAttrib = measure.attrib
		strAttrVals = strAttrVals + ',' + ','.join([dictAttrib['meanValue'], dictAttrib['lowerLimit'], dictAttrib['upperLimit']])
	strAttrVals = strAttrVals + ',' + str(sim_time)
	with lockWrite:
		with open(outfile, 'a') as f:
			f.write(strAttrVals + '\n')
	
		
def init(l):
    global lockWrite
    lockWrite = l		
	
	
def main():
	OUTFILE = 'multi_N100.csv'

	N_TOT = 100
	N_A = range(0, N_TOT+1, 1)
	Z_A = [100]
	Z_B = [100]
	S_A_B1 = [13]
	S_B_B2 = [11]
	
	ATTRIBUTE_NAMES = ['N_A', 'N_B', 'r_Z_A', 'r_Z_B', 'r_A_B1', 'r_B_B2']
	MEASURE_NAMES = ['R0', 'R0_low', 'R0_up', 'R0_A', 'R0_A_low', 'R0_A_up', 'R0_B', 'R0_B_low', 'R0_B_up', 'X0', 'X0_low', 'X0_up', 'X0_A', 'X0_A_low', 'X0_A_up', 'X0_B', 'X0_B_low', 'X0_B_up', 'Ub1', 'Ub1_low', 'Ub1_up', 'Ub2', 'Ub2_low', 'Ub2_up', 'sim_time_sec']
	
	with open(OUTFILE, 'w') as f:
		f.write(','.join(ATTRIBUTE_NAMES) + ',' + ','.join(MEASURE_NAMES) + '\n')
	
	source = ['VAL{:03d}'.format(n) for n in range(len(ATTRIBUTE_NAMES))]
	paramsIterable = []
	for idx, vals in enumerate(list(itertools.product(N_A, Z_A, Z_B, S_A_B1, S_B_B2))):
		nA = vals[0]
		nB = N_TOT - nA
		rzA = 1/vals[1]
		rzB = 1/vals[2]
		rAb1 = 1/vals[3]
		rBb2 = 1/vals[4]
		params = [nA, nB, rzA, rzB, rAb1, rBb2]
		paramsIterable.append((idx, source, params, OUTFILE))
	
	l = Lock()	
	with Pool(NUM_SIM_THREADS, initializer=init, initargs=(l,)) as pool:
		pool.starmap(runSim, paramsIterable)	
	pool.close()
	pool.join()
		
		
if __name__ == '__main__':
	main()
