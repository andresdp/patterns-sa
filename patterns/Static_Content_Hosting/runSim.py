import os, sys
import itertools
import random
import xml.etree.ElementTree as et
from multiprocessing import Pool, Lock
import time
sys.path.insert(1, '../')
from varEnv import * # To import *jmtpath* and *NUM_SIM_THREADS*



def genModel(idx, source, params, modelName):
	placeholderName = 'model.placeholder.jsimg'
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
	cmd = 'java -cp ' + jmtpath + ' jmt.commandline.Jmt sim ' + modelName + ' -seed ' + rnd
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
	OUTFILE = 'multi_N50.csv'

	N_TOT = 50
	N_A = range(0, N_TOT+1, 1)
	Z_A = [100]
	Z_B = [100]
	C_APP = [1]
	C_STO = [1]
	S_A_APP = [14]
	S_B_APP = [6]
	S_A_STO = [8]
	S_B_STO = [x for x in range(7,16,1)]
	
	ATTRIBUTE_NAMES = ['N_A', 'N_B', 'r_Z_A', 'r_Z_B', 'c_APP', 'c_STO', 'r_A_APP', 'r_B_APP', 'r_A_STO', 'r_B_STO']
	MEASURE_NAMES = ['R0', 'R0_low', 'R0_up', 'R0_A', 'R0_A_low', 'R0_A_up', 'R0_B', 'R0_B_low', 'R0_B_up', 'X0', 'X0_low', 'X0_up', 'X0_A', 'X0_A_low', 'X0_A_up', 'X0_B', 'X0_B_low', 'X0_B_up', 'Uapp', 'Uapp_low', 'Uapp_up', 'Usto', 'Usto_low', 'Usto_up', 'sim_time_sec']
	
	with open(OUTFILE, 'w') as f:
		f.write(','.join(ATTRIBUTE_NAMES) + ',' + ','.join(MEASURE_NAMES) + '\n')
	
	source = ['VAL{:03d}'.format(n) for n in range(len(ATTRIBUTE_NAMES))]
	paramsIterable = []
	for idx, vals in enumerate(list(itertools.product(N_A, Z_A, Z_B, C_APP, C_STO, S_A_APP, S_B_APP, S_A_STO, S_B_STO))):
		nA = vals[0]
		nB = N_TOT - nA
		rzA = 1/vals[1]
		rzB = 1/vals[2]
		capp = vals[3]
		csto = vals[4]
		rAapp = 1/vals[5]
		rBapp = 1/vals[6]
		rAsto = 1/vals[7]
		rBsto = 1/vals[8]
		params = [nA, nB, rzA, rzB, capp, csto, rAapp, rBapp, rAsto, rBsto]
		paramsIterable.append((idx, source, params, OUTFILE))
	
	l = Lock()	
	with Pool(NUM_SIM_THREADS, initializer=init, initargs=(l,)) as pool:
		pool.starmap(runSim, paramsIterable)	
	pool.close()
	pool.join()
		
		
if __name__ == '__main__':
	main()
