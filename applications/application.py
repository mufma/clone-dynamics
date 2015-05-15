from core import engine
import json

def main():
	stem = []
	progenitors = []
	mature = []
	clones = 100
	
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
		reactions.append(engine.reaction({stemname:1, 'data':[S]}, {stemname:1, progname:1, 'data':[S, P]}, 'StemDiff', progenitors, 0.01))
		reactions.append(engine.reaction({progname:1, 'data':[P]}, {progname:2, 'data':[P]}, 'Renew', progenitors, 1.0, [1000.0]))
		reactions.append(engine.reaction({progname:1, 'data':[P]}, {matname:1, 'data':[M]}, 'BloodCreat', progenitors, 0.2))
		reactions.append(engine.reaction({progname:1, 'data':[P]}, {'data':[]}, 'ProgenitorDeath', progenitors, 0.2))
		reactions.append(engine.reaction({matname:1, 'data':[M]}, {'data':[]}, 'MatureDeath', progenitors, 0.2))

	
	G = engine.gillespie(reactions, mature)
	data = G.run(20000)
	jsondata = json.dumps(data)
	with open("serious.txt", "w") as text_file:
	    text_file.write(jsondata)
	    
main()