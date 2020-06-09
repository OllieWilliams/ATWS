import unittest
from httprequestprocessor import HttpRequestProcessor


class TestStringMethods(unittest.TestCase):

  def test_http_request(self):
      httpreq = HttpRequestProcessor()
      s = '\\n\\n'
      headers_list = httpreq._construct_headers_list(s)
      self.assertEqual(4, len(headers_list), headers_list)

      self.assertEqual('GET / HTTP/1.1', headers_list[0])
      self.assertEqual('Host: localhost', headers_list[1])
      self.assertEqual('Connection: keep-alive', headers_list[2])
      self.assertEqual('Upgrade-Insecure-Requests: 1', headers_list[3])

  def test_incomplete_2(self):
      httpreq = HttpRequestProcessor()
      s = 'GET / HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: keep-alive\\r\\nUpgrade-Insecure-Requests: 1\\r\\n'
      headers_list = httpreq._construct_headers_list(s)
      self.assertEqual(4, len(headers_list), headers_list)

      self.assertEqual('GET / HTTP/1.1', headers_list[0])
      self.assertEqual('Host: localhost', headers_list[1])
      self.assertEqual('Connection: keep-alive', headers_list[2])
      self.assertEqual('Upgrade-Insecure-Requests: 1', headers_list[3])

  def test_header_trim(self):
      httpreq = HttpRequestProcessor()
      s = 'GET / HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: keep-alive\\r\\nUpgrade-Insecure-Requests: ' \
          '1\\r\\nabvdcdfrer'
      headers_list = httpreq._construct_headers_list(s)
      s = httpreq._trim_buffer(headers_list, s)

      self.assertEqual('abvdcdfrer', s, (headers_list, s))

if __name__ == '__main__':
    unittest.main()