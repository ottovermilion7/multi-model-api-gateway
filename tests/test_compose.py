import pathlib,unittest
class T(unittest.TestCase):
 def test_no_secret(self):
  s=pathlib.Path("compose/litellm.config.yaml").read_text();self.assertIn("api_base:",s);self.assertNotIn("sk-",s)
if __name__=="__main__":unittest.main()
