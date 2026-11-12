import unittest
from adapters.mcp_server import capabilities_from_index
class McpTests(unittest.TestCase):
 def test_advertises_capabilities(self):self.assertEqual(capabilities_from_index({"plugins":[{"id":"p","capabilities":[{"id":"x.y","mode":"read"}]}]})[0]["name"],"x.y")
if __name__=="__main__":unittest.main()
