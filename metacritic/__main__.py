# import of required modules
from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser

from .parser import get_json_data


# server request definition
class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    # define headers - use 'Content-type', 'application/json'
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        # use_platform and available
        # used to transfer the selected server operation parameters
        global use_platform
        global available
        self._set_headers()
        # parse path in get request
        # replace('%20',' ') - this is convert space from url to normal string
        path = str(self.path).replace('%20', ' ').lower()
        if path.find('/games') != -1:
            s_index = path.find('/games/')
            # use get_json_data(available,platform,search_key) to parse data and get json
            # also use encode() to convert json string to byte obj
            if s_index != -1 and len(path) > 7:
                self.wfile.write((get_json_data(available, use_platform, path[s_index + 7: len(path)]).encode()))
            elif len(path) <= 7:
                self.wfile.write((get_json_data(available, use_platform).encode()))


def start_parser():
    # use_platform and available
    # used to transfer the selected server operation parameters
    global use_platform
    global available
    # define options to start prog
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--platform", default="ps4", dest="platform",
                      help="Platform to parse(ps4,xboxone,switch,pc,wii-u,3ds,vita,ios). default: ps4")
    parser.add_option("-a", "--available", default="available", dest="available",
                      help="Availability of games(new-releases, coming-soon, available). default: available")
    parser.add_option("-s", "--search", default=None,
                      help="""Key to form a request(To enter an argument with a space, you will have to enclose it in quotation marks "request with space"). default:None""",
                      dest="search")
    parser.add_option("-f", "--filename", default=None,
                      dest="filename", help="write output to FILE")
    parser.add_option("-r", "--restapi",
                      action="store_true", dest="restapi", default=False,
                      help="Use REST mode. defaul False")
    parser.add_option("-i", "--ip", default="0.0.0.0", dest="host",
                      help="IP for REST server. default: 0.0.0.0")
    parser.add_option("-t", "--port", default=8000, dest="port",
                      help="Port for REST server. default: 8000")
    (options, args) = parser.parse_args()
    # use options and  start event
    use_platform = options.platform
    available = options.available
    # if restapi - True
    if options.restapi:
        print("Start restapi...")
        httpd = HTTPServer((options.host, options.port), RestHTTPRequestHandler)
        while True:
            httpd.handle_request()
    # if CLI versions
    else:
        json_data = get_json_data(available, use_platform, options.search)
        print(json_data)
        if options.filename != None:
            try:
                with open(options.filename, 'w') as outfile:
                    outfile.write(json_data)
            except:
                print('Error write file %s' % (options.filename))


if __name__ == "__main__":
    start_parser()
