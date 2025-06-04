
#working well and code 

# it doesn't scan any website automatically it just analysis test cases

# import ollama
# from tenacity import retry, stop_after_attempt, wait_fixed

# MODEL = "phi3"  # 3.8B parameter model

# @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
# def analyze_security(log):
#       Content: {html[:1000]}... [truncated]
            
#             Respond in this exact format:
#             1. [VULN_TYPE]: [RISK_LEVEL] - [ONE_SENTENCE_DESCRIPTION]
#             2. ...""",
#             options={"temperature": 0}
#         )
#         return result["response"]
#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     target = "http://bwapp.hakhub.net/login.php"  # Default test site
#     print("Scanning:", target)
#     print(quick_scan(target))try:
# #         response = ollama.generate(
# #             model=MODEL,
# #             options={
# #                 "num_ctx": 1024,  # Reduced context window
# #                 "temperature": 0
# #             },
# #             prompt=f"""Analyze this log entry concisely:
#             {log[:300]}
            
#             Respond with:
#             - Vulnerability type
#             - Risk level (High/Medium/Low)
#             - One mitigation"""
#         )
#         return response["response"]
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         raise

# if __name__ == "__main__":
#     test_cases = [
#         "GET /login.php?user=admin'--",
#         "<script>alert('XSS')</script> in search box",
#         "POST /reset-password with {'token':'1234'}"
#     ]
    
#     for test in test_cases:
#         print(f"\nAnalyzing: {test}")
#         print(analyze_security(test))




#working 
# import requests
# from bs4 import BeautifulSoup

# def test_bwapp():
#     BASE_URL = "http://bwapp.hakhub.net"
#     session = requests.Session()
    
#     # 1. Login (required for most tests)
#     login_url = f"{BASE_URL}/login.php"
#     session.post(login_url, data={"login": "bee", "password": "bug", "form": "submit"})
    
#     # 2. Test SQL Injection
#     sqli_url = f"{BASE_URL}/sqli_1.php"
#     response = session.post(sqli_url, data={"title": "x' OR 1=1 -- ", "action": "search"})
#     sqli_vulnerable = "You have an error in your SQL syntax" not in response.text
#     print("SQLi Response Code:", response.status_code)
#     print("SQLi Response Snippet:", response.text[:200])
    
#     # 3. Test XSS
#     xss_url = f"{BASE_URL}/xss_stored_1.php"
#     test_payload = "<script>alert(1)</script>"
#     session.post(xss_url, data={"entry": test_payload, "form": "submit"})
#     response = session.get(xss_url)
#     xss_vulnerable = test_payload in response.text
    
#     return {
#         "SQLi": "✅ Vulnerable" if sqli_vulnerable else "❌ Patched",
#         "XSS": "✅ Vulnerable" if xss_vulnerable else "❌ Patched"
#     }

# print("bWAPP Test Results:")
# print(test_bwapp())



import ollama
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

MODEL = "phi3"  # Lightweight 3.8B parameter model

class LLMPentester:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0"}

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def query_llm(self, prompt):
        """Query local LLM with error handling"""
        try:
            response = ollama.generate(
                model=MODEL,
                prompt=prompt,
                
                options={"num_ctx": 1024,  # Reduce context window
                         "num_thread": 4,  # Limit CPU threads
                        "temperature": 0},
            )
            return response["response"]
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            return None

    def analyze_response(self, response_text):
        """Analyze server response for vulnerabilities using LLM"""
        prompt = f"""Analyze this web response for security vulnerabilities:
        
        {response_text[:1000]}...

        Respond in this exact format:
        1. [VULN_TYPE]: [RISK_LEVEL] - [DESCRIPTION]
        2. [MITIGATION]
        Example:
        1. SQLi: High - Unsanitized input in login form
        2. Use parameterized queries"""
        
        return self.query_llm(prompt)

    def scan_url(self, url):
        """Full scan workflow"""
        print(f"\n[+] Scanning {url}")
        
        # 1. Fetch target page
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Submit test payloads
            test_payloads = [
                ("SQLi", "' OR 1=1 --"),
                ("XSS", "<script>alert(1)</script>"),
                ("Path Traversal", "../../etc/passwd")
            ]
            
            for vuln_type, payload in test_payloads:
                print(f"Testing {vuln_type}...")
                if "login.php" in url:
                    data = {"login": payload, "password": "test", "form": "submit"}
                    resp = self.session.post(url, data=data)
                else:
                    resp = self.session.get(f"{url}?q={payload}")
                
                # 3. LLM Analysis
                if resp.status_code == 200:
                    analysis = self.analyze_response(resp.text)
                    if analysis:
                        print(f"[!] Potential {vuln_type}:\n{analysis}")
        
        except Exception as e:
            print(f"Scan failed: {str(e)}")

if __name__ == "__main__":
    tester = LLMPentester()
    
    # Test cases
    targets = [
        "http://bwapp.hakhub.net/login.php",
        "http://bwapp.hakhub.net/xss_get.php"
    ]
    
    for target in targets:
        tester.scan_url(target)