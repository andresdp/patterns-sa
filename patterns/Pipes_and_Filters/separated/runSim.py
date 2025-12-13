import os, sys
import itertools
import random
import xml.etree.ElementTree as et
from multiprocessing import Pool, Lock
import time
sys.path.insert(1, '../../')
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
	OUTFILE = 'Core1_N50.csv'

	N_TOT = 50
	N_A = range(0, N_TOT+1, 1)
	Z_A = [100]
	Z_B = [100]
	C_A_T1 = [1]
	C_A_T2 = [1]
	C_A_T3 = [1]
	C_B_T1 = [1]
	C_B_T2 = [1]
	C_B_T4 = [1]
	S_A_T1 = [12]
	S_A_T2 = [15]
	S_A_T3 = [11]
	S_B_T1 = [8]
	S_B_T2 = [9]
	S_B_T4 = [10]
	
	ATTRIBUTE_NAMES = ['N_A', 'N_B', 'r_Z_A', 'r_Z_B', 'c_A_T1', 'c_A_T2', 'c_A_T3', 'c_B_T1', 'c_B_T2', 'c_B_T4', 'r_A_T1', 'r_A_T2', 'r_A_T3', 'r_B_T1', 'r_B_T2', 'r_B_T4']
	MEASURE_NAMES = ['R0', 'R0_low', 'R0_up', 'R0_A', 'R0_A_low', 'R0_A_up', 'R0_B', 'R0_B_low', 'R0_B_up', 'X0', 'X0_low', 'X0_up', 'X0_A', 'X0_A_low', 'X0_A_up', 'X0_B', 'X0_B_low', 'X0_B_up', 'Ut1_A', 'Ut1_A_low', 'Ut1_A_up', 'Ut2_A', 'Ut2_A_low', 'Ut2_A_up', 'Ut3_A', 'Ut3_A_low', 'Ut3_A_up', 'Ut1_B', 'Ut1_B_low', 'Ut1_B_up', 'Ut2_B', 'Ut2_B_low', 'Ut2_B_up', 'Ut3_B', 'Ut3_B_low', 'Ut3_B_up', 'sim_time_sec']
	
	with open(OUTFILE, 'w') as f:
		f.write(','.join(ATTRIBUTE_NAMES) + ',' + ','.join(MEASURE_NAMES) + '\n')
	
	source = ['VAL{:03d}'.format(n) for n in range(len(ATTRIBUTE_NAMES))]
	paramsIterable = []
	for idx, vals in enumerate(list(itertools.product(N_A, Z_A, Z_B, C_A_T1, C_A_T2, C_A_T3, C_B_T1, C_B_T2, C_B_T4, S_A_T1, S_A_T2, S_A_T3, S_B_T1, S_B_T2, S_B_T4))):
		nA = vals[0]
		nB = N_TOT - nA
		rzA = 1/vals[1]
		rzB = 1/vals[2]
		cAt1 = vals[3]
		cAt2 = vals[4]
		cAt3 = vals[5]
		cBt1 = vals[6]
		cBt2 = vals[7]
		cBt4 = vals[8]
		rAt1 = 1/vals[9]
		rAt2 = 1/vals[10]
		rAt3 = 1/vals[11]
		rBt1 = 1/vals[12]
		rBt2 = 1/vals[13]
		rBt4 = 1/vals[14]
		params = [nA, nB, rzA, rzB, cAt1, cAt2, cAt3, cBt1, cBt2, cBt4, rAt1, rAt2, rAt3, rBt1, rBt2, rBt4]
		paramsIterable.append((idx, source, params, OUTFILE))
	
	l = Lock()	
	with Pool(NUM_SIM_THREADS, initializer=init, initargs=(l,)) as pool:
		pool.starmap(runSim, paramsIterable)	
	pool.close()
	pool.join()
		
		
if __name__ == '__main__':
	main()
