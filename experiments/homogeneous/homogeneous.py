from core import engine
import json

def main(alpha, p, mu_p, omega, mu_d, K, C):
	stem = []
	progenitors = []
	mature = []
	clones = C
	
	for rep in range(clones):
	    stemname = 'stem{0}'.format(rep)
	    progname = 'progenitor{0}'.format(rep)
	    matname = 'mature{0}'.format(rep)
	    S = engine.colony(stemname, 1)
	    P = engine.colony(progname, 0)
	    M = engine.colony(matname, 0)
	    stem.append(S)
	    progenitors.append(P)
	    mature.append(M)
	
	reactions = []
	for rep in range(clones):
		stemname = 'stem{0}'.format(rep)
		progname = 'progenitor{0}'.format(rep)
		matname = 'mature{0}'.format(rep)
		S = stem[rep]
		P = progenitors[rep]
		M = mature[rep]
		reactions.append(engine.reaction({stemname:1, 'data':[S]}, {stemname:1, progname:1, 'data':[S, P]}, 'StemDiff', progenitors, alpha))
		reactions.append(engine.reaction({progname:1, 'data':[P]}, {progname:2, 'data':[P]}, 'Renew', progenitors, p, [K]))
		reactions.append(engine.reaction({progname:1, 'data':[P]}, {matname:1, 'data':[M]}, 'BloodCreat', progenitors, omega))
		reactions.append(engine.reaction({progname:1, 'data':[P]}, {'data':[]}, 'ProgenitorDeath', progenitors, mu_p))
		reactions.append(engine.reaction({matname:1, 'data':[M]}, {'data':[]}, 'MatureDeath', progenitors, mu_d))

	
	G = engine.gillespie(reactions, mature+progenitors)
	data_all = G.run(20000)
	data_mature = {key:value for (key,value) in data_all.items() if 'mature' in key}
	data_progenitor = {key:value for (key,value) in data_all.items() if 'progenitor' in key}
	json_mature = json.dumps(data_mature)
	json_progenitor = json.dumps(data_progenitor)
	with open("storage/mature.txt", "w") as text_file:
	    text_file.write(json_mature)
	with open("storage/progenitor.txt", "w") as text_file:
	    text_file.write(json_progenitor)

# Parameters of the reactions	    
alpha, p, mu_p, omega, mu_d, K, C = 0.01, 1.0, 0.2, 0.2, 0.2, 1000.0, 1000
main(alpha, p, mu_p, omega, mu_d, K, C)
