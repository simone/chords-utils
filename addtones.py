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
TOKENS = set(reduce(lambda x,y: x+y, SEMITONI))
re_note = re.compile("|".join(sorted(TOKENS, reverse=True)))

def plus(str,n):
    for i, notes in enumerate(SEMITONI):
        if str in notes:
            return SEMITONI[(i+n)%len(SEMITONI)][0]

def trasform(args, n=2):
    return [plus(x, n) for x in args]


def add_tones(input_lines=[], toni=0, su=0, peso=3.0):
    lines = []
    for line in input_lines:
        _from = re_note.findall(line)
        # if len(_from) -> Non sono accordi se le lettere presenti sulla linea 
        #                  sono pesantemente maggiori dei caratteri impiegati dagli accordi
        if len("".join(line.split())) > peso*float(len("".join(_from))):
            lines.append(re.sub('\s+', " ", line))
        else:
	    _to   = trasform(_from, toni)
            others = re.match(r"(.*)%s(.*)" % r"(.*)".join(_from), line).groups()
            new = "<b>%s</b>" % "".join(reduce(lambda x,y: x+y, zip(others, _to) + [tuple(others[-1])]))
            lines.insert(-su, new) if su else lines.append(new)
    return lines

def main(file_in, file_out, toni, su=0, peso=3.0):
    print "Reading", file_in, "..."
    fin = file(file_in, 'r')
    lines = add_tones(fin.readlines(), toni, su, peso)
    fin.close()
    fout = file(file_out, 'w')
    fout.writelines(lines)
    print "".join(lines)
    fout.close()
    print "Writing", file_out, "... done!"




class Resource(object):
    exposed = True

    def GET(self):
        return self.to_html()

    def POST(self, name, chords, tones, upper, peso, method=None):
        name = re.sub("\s+", "_", name).lower()
        return self.to_html(name, chords, 
                            self.chords(chords, int(tones), int(upper), float(peso)),
                            tones, upper, peso, method)

    def to_html(self, name="", source="", compiled="", tones=2, upper=0, peso=3.0, method=None):
        if not method:
            mibemolle = compiled.lower().count("mib")
            return """
		   <html>
            <head><script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
            <script>
            var w, h, d_css;
            function fullScreen(){
                if ($('#full').val() == "Full Screen"){
                    $('#compiled').siblings(".hideable").hide();
                    w = $('#compiled').width();
                    h = $('#compiled').height();
                    $('#compiled').width($(window).width() - 15).height($(window).height() - 15);
                    $('#full').val("Half Screen");
                } else {
                    $('#compiled').siblings(".hideable").show();
                    $('#compiled').width(w).height(h);
                    $('#full').val("Full Screen");
                }
            }
            $('#compiled').dblclick(fullScreen);
			$(document).keyup(function(e) {
			  if (e.keyCode == 27) { fullScreen(); }   // esc
			});
            </script>
            </head>
            <body id="body" style="background-color: #FFFFDF;">
			<form method="POST">
             <div style="float: right">
                 <input id="full" type="button" onclick="fullScreen()" value="Full Screen" />
                 <input name="method" type="submit" value="Download"/>
             </div>
			 <div class="hideable">+/- tones: <input name="tones" value="%(tones)s"> up chord lines of <input name="upper" value="%(upper)s"> 
             peso <input name="peso" value="%(peso)s">
		         <input type="submit"/><input type="button" onclick="window.location.href=window.location.href" value="Reset" /><br/>
                 <input id="name" name="name" value="%(name)s" style="width: 49%%"/> (%(mibemolle)s Mib)<br/>
             </div>
             
			 <textarea id="chords" class="hideable" name="chords" style="width: 49%%; height: 80%%">%(source)s</textarea>
		     <div id="compiled" disabled=true style="float: right; background: #FFFFDF; width: 47%%"><pre>%(compiled)s</pre></div>
			</form>
            </body>
		   </html>""" % vars()
        import cherrypy
        cherrypy.response.headers['content-type'] = 'text/plain'
        cherrypy.response.headers['content-disposition'] = 'attachment; filename=%s.txt' % name
        return compiled.replace("<b>", "").replace("</b>", "")

    def chords(self, source, tones, upper, peso):    
        return "\n".join(add_tones(source.splitlines(), tones, upper, peso))



def run_cherrypy(host='0.0.0.0', port=8000):
    try:
        import cherrypy
    except:
        print "Before you need to instalL Cherrypy."
        return
    
    root = Resource()
    conf = {
        'global': {
            'server.socket_host': host,
            'server.socket_port': int(port),
        },
       '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }
    cherrypy.quickstart(root, '/', conf)


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "cherrypy":
        run_cherrypy(*sys.argv[2:])

    elif len(sys.argv) >= 4:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), 
             int(sys.argv[4]) if len(sys.argv)>=5 else 0,     # alza le righe (x portare gli accordi sulla righa superiore passare 1)
             float(sys.argv[5]) if len(sys.argv)==6 else 3.0  # coefficiente peso accordi sulla linea, [lasciare come sta :-) ]
        )
    else:
        print "USE: python", __file__, "<input> <output> <+/-semitoni> [0|1 <sposta accordi>]"
        print "OR : python", __file__, "cherrypy [0.0.0.0] [8000]"


