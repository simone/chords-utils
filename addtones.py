# Creative Commons
# @ Simone Federici
#
# 1) Il programma serve a alzare/abbassare di n semitoni gli spartiti.
# 2) Inoltre trasforma gli accordi A,B,C... in formato "italiano" LA,SI,DO
#    se lanciato con 0 semitoni fa solo la trasformazione
# 3) La terza feature e' utile per spostare gli accordi sulla linea che precede 
#    il testo anziche sulla successiva. 
# 
# Quasi quasi ci faccio un servizio Internet :-)


import sys
import re

SEMITONI = [
    ['DO', 'SI#', 'C', 'B#'],
    ['DO#', 'REb', 'C#', 'Db'],
    ['RE', 'D'],
    ['MIb', 'RE#', 'Eb', 'D#'],
    ['MI', 'FAb', 'E', 'Fb'],
    ['FA', 'MI#', 'F', 'E#'],
    ['FA#', 'SOLb', 'F#', 'Gb'],
    ['SOL', 'G'],
    ['SOL#', 'LAb', 'G#', 'Ab'],
    ['LA', 'A'],
    ['SIb', 'LA#', 'Bb', 'A#'],
    ['SI', 'DOb', 'B', 'Cb']
]
TOKENS = set(reduce(lambda x,y: x+y,SEMITONI))
re_note = re.compile("|".join(sorted(TOKENS, reverse=True)))

def plus(str,n):
    for i, notes in enumerate(SEMITONI):
        if str in notes:
            return SEMITONI[(i+n)%len(SEMITONI)][0]

def trasform(args, n=2):
    return [plus(x, n) for x in args]


def main(file_in, file_out, toni, su=0, peso=3):
    print "Reading", file_in, "..."
    fin = file(file_in, 'r')
    lines = []

    for line in fin.readlines():
        _from = re_note.findall(line)
        # if len(_from) -> Non sono accordi se le lettere presenti sulla linea 
        #                  sono pesantemente maggiori dei caratteri impiegati dagli accordi
        if len("".join(line.split())) > peso*len("".join(_from)):
            lines.append(line)
        else:
	    _to   = trasform(_from, toni)
            others = re.match(r"(.*)%s(.*)" % r"(.*)".join(_from), line).groups()
            new = "".join(reduce(lambda x,y: x+y, zip(others, _to) + [tuple(others[-1])])) + "\n"
            lines.insert(-su, new) if su else lines.append(new)

    fin.close()
    fout = file(file_out, 'w')
    fout.writelines(lines)
    print "".join(lines)
    fout.close()
    print "Writing", file_out, "... done!"


if __name__ == "__main__":
    print sys.argv
    if len(sys.argv) >= 4:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), 
             int(sys.argv[4]) if len(sys.argv)>=5 else 0, # alza le righe (x portare gli accordi sulla righa superiore passare 1)
             int(sys.argv[5]) if len(sys.argv)==6 else 3  # coefficiente peso accordi sulla linea, [lasciare come sta :-) ]
        )
    else:
        print "USE: python", __file__, "<input> <output> <+/-semitoni> [0|1 <sposta accordi>]"

