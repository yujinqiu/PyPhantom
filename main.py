import cherrypy, json, time, string, random, os.path, sys, getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

phantomjs = ""
 
class PyPhantomWeb(object):
	@cherrypy.expose
	def index(self):
		return "PyPhantom Web Server"
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def get(self, url, screenshot="false"):
		return phantomGet(url, screenshot)
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def gowork(self, work):
		workdata = json.loads(work)
		return phantomGet(workdata["url"], workdata["screenshot"])

def main(argv):
	ip = ""
	port = 0
	try:
		opts, args = getopt.getopt(argv, "hipj", ["ip=", "port=", "phantomjs="])
	except getopt.GetoptError:
		print("PyPhantom --ip=<IP to listen on, e.g. 127.0.0.1> --port=<Port to listen on, e.g. 80> --phantomjs=<PhantomJS startup command, e.g. phantomjs.cmd>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("PyPhantom --ip=<IP to listen on, e.g. 127.0.0.1> --port=<Port to listen on, e.g. 80> --phantomjs=<PhantomJS startup command, e.g. phantomjs.cmd>")
			sys.exit()
		elif opt in ("-i", "--ip"):
			ip = arg
		elif opt in ("-p", "--port"):
			port = int(arg)
		elif opt in ("-j", "--phantomjs"):
			global phantomjs
			phantomjs = arg
	cherrypy.config.update({"server.socket_port": port, "server.socket_host": ip})
	cherrypy.quickstart(PyPhantomWeb(), "/", {"/":{"tools.gzip.on": True, "tools.encode.on": True, "tools.encode.encoding": "utf-8"}})

def phantomGet(url, screenshot):
	driver = webdriver.PhantomJS(phantomjs)
	driver.set_window_size(1024, 768)
	driver.set_page_load_timeout(180)
	driver.get(url)
	time.sleep(10)
	if screenshot == "true":
		screenshotID = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
		if os.path.isfile(screenshotID + ".png") == True:
			screenshotID = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
		driver.save_screenshot(screenshotID + ".png")
		res = {"result":driver.page_source, "screenshot":screenshotID + ".png"}
	else:
		res = {"result":driver.page_source}
	driver.close()
	driver.quit()
	cherrypy.response.headers["Content-Type"] = "application/json"
	return res

if __name__ == "__main__":
	main(sys.argv[1:])