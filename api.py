from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
from PIL import Image
from io import BytesIO, StringIO
import uuid

import text_recognition3 as tr
import search

import json

def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
   # binary = ' '.join(format(ord(letter), 'b') for letter in str.encode('ascii', "ignore"))
    binary = str.encode('ascii', "ignore")
    print(binary)
    return binary


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        im = Image.open(BytesIO(base64.b64decode(body)))
        file_id = str(uuid.uuid4().int)
        path = '/home/andrey/Hackaton/price-reader-prototype/recognition api/%s.jpg' % (file_id)
        im.save(path, 'JPEG')
        
        res = tr.main(file_id)
        final_item = search.fuzzy_search(res, similar_threshold=5)[0]
        print(final_item)
        item_info["name"] = final_item["name"]
        item_info["price"] = final_item["price"]
        item_info["percent"] = final_item["percent"]
        #response.
        #print(res)
        dict_to_binary(item_info)
        
        response.write(dict_to_binary(item_info))
        #response.write.write("YOU ARE HERE 2")
        self.wfile.write(response.getvalue())

item_info = { "name":"",
             "price":"",
             "percent":""
}        

httpd = HTTPServer(("192.168.43.84", 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
