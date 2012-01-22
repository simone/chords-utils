from addtones import Resource
try:
    import cherrypy
except:
    print "Before you need to instalL Cherrypy."
    exit()
try:
    import uwsgi
except:
    print "Before you need to instalL uwsgi."
    exit()

cherrypy.config.update({'environment': 'embedded'})

app = cherrypy.Application(Resource(), script_name='/', config={
   '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
})

uwsgi.applications = {'': app}
