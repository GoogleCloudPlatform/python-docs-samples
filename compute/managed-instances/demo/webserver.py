#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os, socket, requests, re, random
from SocketServer import ThreadingMixIn
from multiprocessing import Process

PORT_NUMBER = 80
WORKING = False
HEALTHY = True
PROCESS = None

class myHandler(BaseHTTPRequestHandler):
	def get_zone(self):
		r = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/zone', headers={'Metadata-Flavor':'Google' })
		if r.status_code == 200:
			return re.sub(r'.+zones/(.+)', r'\1', r.text.encode('utf-8'))
		else:
			return ''

	def get_template(self):
		r = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/attributes/instance-template', headers={'Metadata-Flavor':'Google' })
		if r.status_code == 200:
			return re.sub(r'.+instanceTemplates/(.+)', r'\1', r.text.encode('utf-8'))
		else:
			return ''

	def burn_cpu(x):
		while True:
			random.random()*random.random()

	def do_GET(self):
		global WORKING, HEALTHY, PROCESS

		if self.path == '/makeHealthy':
			HEALTHY = True
			self.send_response(302)
			self.send_header('Location','/')
			self.end_headers()
			return

		if self.path == '/makeUnhealthy':
			HEALTHY = False
			self.send_response(302)
			self.send_header('Location','/')
			self.end_headers()
			return

		if self.path == '/startLoad':
			if not WORKING:
				PROCESS = Process(target=self.burn_cpu)
				PROCESS.start()

			WORKING = True
			self.send_response(302)
			self.send_header('Location','/')
			self.end_headers()
			return

		if self.path == '/stopLoad':
			if PROCESS.is_alive():
				PROCESS.terminate()

			WORKING = False
			self.send_response(302)
			self.send_header('Location','/')
			self.end_headers()
			return

		if self.path == '/health':
			if not HEALTHY:
				self.send_response(500)
				self.end_headers()
			else:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write('<span style="font-family: verdana; font-weight: bold; font-size: 40px">HTTP/1.0 200 OK</span>')
				self.wfile.close()
			return

		HOSTNAME = socket.gethostname().encode('utf-8')
		ZONE = self.get_zone()
		TEMPLATE = self.get_template()

		self.send_response(200 if HEALTHY else 500)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write('''
<html>
<head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css">
	<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/js/materialize.min.js"></script>
</head>
<body>
	<table class="striped">
		<colgroup>
			<col width="200">
		</colgroup>
		<tbody>
			<tr>
				<td>Hostname:</td>
				<td><b>''' + HOSTNAME +'''</b></td>
			</tr>
			<tr>
				<td>Zone:</td>
				<td><b>''' + ZONE +'''</b></td>
			</tr>
			<tr>
				<td>Template:</td>
				<td><b>''' + TEMPLATE +'''</b></td>
			</tr>
			<tr>
				<td>Current load:</td>
				<td><span class="btn ''' + ('red' if WORKING else 'green') + '''"">''' + ('high' if WORKING else 'none') + '''</span></td>
			</tr>
			<tr>
				<td>Health status:</td>
				<td><span class="btn ''' + ('green' if HEALTHY else 'red') + '''">''' + ('healthy' if HEALTHY else 'unhealthy') + '''</span></td>
			</tr>
			<tr>
				<td>Actions:</td>
				<td>
					<a class="btn blue" href="/''' + ('makeUnhealthy' if HEALTHY else 'makeHealthy') + '''">Make ''' + ('unhealthy' if HEALTHY else 'healthy') + '''</a>
					<a class="btn blue" href="/''' + ('stop' if WORKING else 'start') + '''Load">''' + ('Stop' if WORKING else 'Start') + ''' load</a>
					<a class="btn blue" href="/health">Check health</a>
				</td>
			</tr>
		</tbody>
	</table>
</body>
</html>
''')
		self.wfile.close()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

try:
	server = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port %s' % PORT_NUMBER)
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
