import os
import sys
import hfst
import glob

if len(sys.argv) <= 1:
	print('test.py <lang code>')
	sys.exit(-1)

lang = sys.argv[1]

testf = []

if len(sys.argv) == 3 and '.tsv' in sys.argv[2]:
	testf = [sys.argv[2]]
else:
	testf = glob.glob('*.tsv')

if '-m' in sys.argv:
    os.system('cd /media/zu_ann/OS/Users/zu_ann/Yandex.Disk/HSE/evenki/apertium-evn && make clean && make')

istr1 = hfst.HfstInputStream('../'+lang+'.automorf.hfst')
anal = istr1.read()
#anal.remove_epsilons()

istr2 = hfst.HfstInputStream('../'+lang+'.autogen.hfst')
gene = istr2.read()
#gene.remove_epsilons()


print(testf)
err_g = 0
corr_g = 0
total_g = 0
err_a = 0
corr_a = 0
total_a = 0
for f in testf: 
	print(f + ':')
	tf = open(f).read().strip().split('\n')
	print('Generation:')
	for t in tf: 
		if t.strip() == '': continue

		row = t.strip().split('\t')
		g_res = gene.lookup(row[0])

		if row[0] == '>': 
			continue
		

		if g_res == (): 
			print('!\t%s\t%s\t%s' % (row[1], row[2], g_res))
			err_g += 1
			total_g += 1
			continue
		
		g_res_corr = g_res[0][0].replace('@_EPSILON_SYMBOL_@', '')
		if g_res_corr == row[2]: 
			print('+\t%s\t%s\t%s' % (row[1], g_res[0][0],
			' '.join([g[0] for g in g_res]).replace('@_EPSILON_SYMBOL_@', '')))
			corr_g += 1
		else: 	
			print('-\t%s\t%s\t%s' % (row[1], row[2],
			 ' '.join([g[0] for g in g_res]).replace('@_EPSILON_SYMBOL_@', '')))
			err_g += 1
		
		total_g += 1
	
	print('Analysis:')
	for t in tf: 
		if t.strip() == '': continue

		row = t.strip().split('\t')

		if row[0] == '<': 
			continue
		

		a_res = anal.lookup(row[2])

		found = False
		for r in a_res: 
			if row[0] == r[0].replace('@_EPSILON_SYMBOL_@', ''): found = True
		
		if found: 
			print('+\t%s\t%s\t%s\t%s' % (row[2], row[1], row[0],
			' '.join([g[0] for g in a_res]).replace('@_EPSILON_SYMBOL_@', '')))
			corr_a += 1
		else: 	
			print('-\t%s\t%s\t%s\t%s' % (row[2], row[1], row[0],
			' '.join([g[0] for g in a_res]).replace('@_EPSILON_SYMBOL_@', '')))
			err_a += 1
		
		total_a += 1
	
	print('')


corr = corr_g + corr_a
total = total_g + total_a

print('PASS:\t%.2f%%' % ((corr/total)*100.0))
print('GEN :\t%d\t%d\t%d' % (total_g, corr_g, err_g))
print('ANAL:\t%d\t%d\t%d' % (total_a, corr_a, err_a))

if corr == total:
	sys.exit(0)
else:
	sys.exit(1)
