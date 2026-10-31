import io, json, threading, unittest, urllib.error, urllib.request
from unittest.mock import patch
from http.server import ThreadingHTTPServer
import server
class BridgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler); cls.http.model='test-model'
        cls.worker=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.worker.start()
        cls.url='http://127.0.0.1:%s/ask' % cls.http.server_port
    @classmethod
    def tearDownClass(cls): cls.http.shutdown();cls.http.server_close();cls.worker.join()
    def post(self,data): return urllib.request.urlopen(urllib.request.Request(self.url,data=data,method='POST'),timeout=3)
    def test_forward(self):
        original=urllib.request.urlopen
        class Response(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self,*args): self.close()
        def route(req,*args,**kwargs):
            if req.full_url == 'http://127.0.0.1:11434/api/generate':
                payload=json.loads(req.data); self.assertEqual(payload['prompt'],'hello'); self.assertEqual(payload['model'],'test-model')
                return Response(b'{"response":"Hello Cece"}')
            return original(req,*args,**kwargs)
        with patch.object(server.urllib.request,'urlopen',side_effect=route):
            with self.post(b'hello') as result: self.assertEqual(result.read(),b'Hello Cece')
    def test_empty_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as e: self.post(b'')
        self.assertEqual(e.exception.code,413)
if __name__=='__main__': unittest.main()
