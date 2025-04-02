
# #working well and good for demo we can use this 

# import ollama
# import requests
# from bs4 import BeautifulSoup
# import time
# from tenacity import retry, stop_after_attempt

# class SmartPentester:
#     def __init__(self):
#         self.session = requests.Session()
#         self.headers = {"User-Agent": "Mozilla/5.0"}
#         self.llm_model = "phi"  # Lightweight model (2.7B params)
#         self.timeout = 10  # Seconds per request
#         self.llm_enabled = True  # Toggle LLM analysis

#     @retry(stop=stop_after_attempt(2))
#     def query_llm(self, prompt):
#         """Safe LLM query with memory limits"""
#         try:
#             response = ollama.generate(
#                 model=self.llm_model,
#                 options={"num_ctx": 1024, "temperature": 0},
#                 prompt=prompt[:500]  # Truncate to save memory
#             )
#             return response["response"]
#         except Exception as e:
#             print(f"\n[LLM Error] {str(e)[:80]}...")
#             return None

#     def fast_detect(self, response_text, vuln_type):
#         """Ultra-fast rule-based detection"""
#         indicators = {
#             "SQLi": ["Welcome", "SQL syntax", "OR 1=1"],
#             "XSS": ["<script>", "alert(1)"],
#             "Path Traversal": ["root:x:", "etc/passwd"]
#         }
        
#         if any(indicator in response_text for indicator in indicators[vuln_type]):
#             return f"{vuln_type}: High (Rule-Based)"
#         return None

#     def scan_endpoint(self, url):
#         """Complete vulnerability assessment"""
#         print(f"\n🔍 Scanning {url}...")
#         start_time = time.time()
        
#         tests = [
#             ("SQLi", "' OR 1=1 --", "POST"),
#             ("XSS", "<script>alert(1)</script>", "GET"),
#             ("Path Traversal", "../../etc/passwd", "GET")
#         ]

#         for vuln_type, payload, method in tests:
#             try:
#                 print(f"  Testing {vuln_type:<15}", end="", flush=True)
                
#                 # Send payload
#                 if method == "POST":
#                     resp = self.session.post(
#                         url, 
#                         data={"login": payload, "password": "x"}, 
#                         timeout=self.timeout
#                     )
#                 else:
#                     resp = self.session.get(
#                         f"{url}?input={payload}", 
#                         timeout=self.timeout
#                     )

#                 # Phase 1: Instant rule-check
#                 if result := self.fast_detect(resp.text, vuln_type):
#                     print(f"\r  ✅ {result}")
#                     continue
                    
#                 # Phase 2: LLM analysis (if enabled)
#                 if self.llm_enabled:
#                     llm_prompt = f"""Security check for {vuln_type}:
#                     Payload: {payload}
#                     Response: {resp.text[:300]}..."""
                    
#                     if llm_result := self.query_llm(llm_prompt):
#                         print(f"\r  ⚠️  {vuln_type}: LLM detected anomaly")
#                     else:
#                         print(f"\r  ❌ {vuln_type}: No detection")
#                 else:
#                     print(f"\r  ❌ {vuln_type}: No detection")

#             except requests.exceptions.Timeout:
#                 print(f"\r  ⌛ {vuln_type}: Timeout")
#             except Exception as e:
#                 print(f"\r  ❗ {vuln_type} failed: {str(e)[:30]}...")

#         print(f"\nScan completed in {time.time() - start_time:.1f}s")

# if __name__ == "__main__":
#     pentester = SmartPentester()
    
#     # Configuration
#     pentester.llm_enabled = True  # Set False for pure rule-based scanning
#     pentester.timeout = 15  # Increase if needed
    
#     targets = [
#         "http://bwapp.hakhub.net/login.php",
#         "http://bwapp.hakhub.net/xss_get.php"
#     ]
    
#     for target in targets:
#         pentester.scan_endpoint(target)


#both are wokring it'll create a report as well in json format

# import ollama
# import requests
# from bs4 import BeautifulSoup
# import time
# import json
# from tenacity import retry, stop_after_attempt

# class SmartPentester:
#     def __init__(self):
#         self.session = requests.Session()
#         self.headers = {"User-Agent": "Mozilla/5.0"}
#         self.llm_model = "phi"  # Lightweight LLM
#         self.timeout = 10  # Request timeout in seconds
#         self.llm_enabled = True  # Toggle AI analysis
#         self.findings = {}  # Store detected vulnerabilities

#     @retry(stop=stop_after_attempt(2))
#     def query_llm(self, prompt):
#         """Query LLM with safe memory limits"""
#         try:
#             response = ollama.generate(
#                 model=self.llm_model,
#                 options={"num_ctx": 1024, "temperature": 0.3},  # Adjust temp for stable responses
#                 prompt=prompt[:500]  # Truncate to avoid memory issues
#             )
#             return response["response"]
#         except Exception as e:
#             print(f"\n[LLM Error] {str(e)[:80]}...")
#             return None

#     def fast_detect(self, response_text, vuln_type):
#         """Rule-based detection for fast scanning"""
#         indicators = {
#             "SQLi": ["Welcome", "SQL syntax", "OR 1=1"],
#             "XSS": ["<script>", "alert(1)"],
#             "Path Traversal": ["root:x:", "etc/passwd"]
#         }
        
#         if any(indicator in response_text for indicator in indicators[vuln_type]):
#             return f"{vuln_type}: High Risk (Rule-Based)"
#         return None

#     def scan_endpoint(self, url):
#         """Perform vulnerability assessment"""
#         print(f"\n🔍 Scanning {url}...")
#         start_time = time.time()
        
#         tests = [
#             ("SQLi", "' OR 1=1 --", "POST"),
#             ("XSS", "<script>alert(1)</script>", "GET"),
#             ("Path Traversal", "../../etc/passwd", "GET")
#         ]

#         self.findings[url] = {}

#         for vuln_type, payload, method in tests:
#             try:
#                 print(f"  Testing {vuln_type:<15}", end="", flush=True)
                
#                 # Send payload
#                 if method == "POST":
#                     resp = self.session.post(url, data={"login": payload, "password": "x"}, timeout=self.timeout)
#                 else:
#                     resp = self.session.get(f"{url}?input={payload}", timeout=self.timeout)

#                 # Phase 1: Fast rule-based check
#                 if result := self.fast_detect(resp.text, vuln_type):
#                     print(f"\r  ✅ {result}")
#                     self.findings[url][vuln_type] = "Vulnerable (Rule-Based)"
#                     continue
                    
#                 # Phase 2: AI-powered verification (if enabled)
#                 if self.llm_enabled:
#                     llm_prompt = f"""Security check for {vuln_type}:
#                     Payload: {payload}
#                     Response: {resp.text[:300]}..."""
                    
#                     if llm_result := self.query_llm(llm_prompt):
#                         print(f"\r  ⚠️  {vuln_type}: LLM detected anomaly")
#                         self.findings[url][vuln_type] = "Vulnerable (LLM Analysis)"
#                     else:
#                         print(f"\r  ❌ {vuln_type}: No detection")
#                 else:
#                     print(f"\r  ❌ {vuln_type}: No detection")

#             except requests.exceptions.Timeout:
#                 print(f"\r  ⌛ {vuln_type}: Timeout")
#                 self.findings[url][vuln_type] = "Timeout"
#             except Exception as e:
#                 print(f"\r  ❗ {vuln_type} failed: {str(e)[:30]}...")
#                 self.findings[url][vuln_type] = "Error"

#         print(f"\nScan completed in {time.time() - start_time:.1f}s")

#     def generate_report(self):
#         """Save findings in JSON format"""
#         with open("scan_report.json", "w") as f:
#             json.dump(self.findings, f, indent=4)
#         print("\n📄 Report saved as scan_report.json")

# if __name__ == "__main__":
#     pentester = SmartPentester()
    
#     # Configuration
#     pentester.llm_enabled = True  # Set False for rule-based scanning only
#     pentester.timeout = 15  # Adjust timeout if needed
    
#     targets = [
#         "http://bwapp.hakhub.net/login.php",
#         "http://bwapp.hakhub.net/xss_get.php"
#     ]
    
#     for target in targets:
#         pentester.scan_endpoint(target)

#     pentester.generate_report()

# it works and generate report as well 
import ollama
import requests
from bs4 import BeautifulSoup
import time
import json
from tenacity import retry, stop_after_attempt

class SmartPentester:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.llm_model = "phi"  # Lightweight LLM
        self.timeout = 10  # Request timeout in seconds
        self.llm_enabled = True  # Toggle AI analysis
        self.findings = {}  # Store detected vulnerabilities

    @retry(stop=stop_after_attempt(2))
    def query_llm(self, prompt):
        """Query LLM with safe memory limits"""
        try:
            response = ollama.generate(
                model=self.llm_model,
                options={"num_ctx": 1024, "temperature": 0.3},  # Adjust temp for stable responses
                prompt=prompt[:500]  # Truncate to avoid memory issues
            )
            return response["response"]
        except Exception as e:
            print(f"\n[LLM Error] {str(e)[:80]}...")
            return None

    def fast_detect(self, response_text, vuln_type):
        """Rule-based detection for fast scanning"""
        indicators = {
            "SQLi": ["Welcome", "SQL syntax", "OR 1=1"],
            "XSS": ["<script>", "alert(1)"],
            "Path Traversal": ["root:x:", "etc/passwd"]
        }
        
        if any(indicator in response_text for indicator in indicators[vuln_type]):
            return f"{vuln_type}: High Risk (Rule-Based)"
        return None

    def scan_endpoint(self, url):
        """Perform vulnerability assessment"""
        print(f"\n🔍 Scanning {url}...")
        start_time = time.time()
        
        tests = [
            ("SQLi", "' OR 1=1 --", "POST"),
            ("XSS", "<script>alert(1)</script>", "GET"),
            ("Path Traversal", "../../etc/passwd", "GET")
        ]

        self.findings[url] = {}

        for vuln_type, payload, method in tests:
            try:
                print(f"  Testing {vuln_type:<15}", end="", flush=True)
                
                # Send payload
                if method == "POST":
                    resp = self.session.post(url, data={"login": payload, "password": "x"}, timeout=self.timeout)
                else:
                    resp = self.session.get(f"{url}?input={payload}", timeout=self.timeout)

                # Phase 1: Fast rule-based check
                if result := self.fast_detect(resp.text, vuln_type):
                    print(f"\r  ✅ {result}")
                    self.findings[url][vuln_type] = "Vulnerable (Rule-Based)"
                    continue
                    
                # Phase 2: AI-powered verification (if enabled)
                if self.llm_enabled:
                    llm_prompt = f"""Security check for {vuln_type}:
                    Payload: {payload}
                    Response: {resp.text[:300]}..."""
                    
                    if llm_result := self.query_llm(llm_prompt):
                        print(f"\r  ⚠️  {vuln_type}: LLM detected anomaly")
                        self.findings[url][vuln_type] = "Vulnerable (LLM Analysis)"
                    else:
                        print(f"\r  ❌ {vuln_type}: No detection")
                else:
                    print(f"\r  ❌ {vuln_type}: No detection")

            except requests.exceptions.Timeout:
                print(f"\r  ⌛ {vuln_type}: Timeout")
                self.findings[url][vuln_type] = "Timeout"
            except Exception as e:
                print(f"\r  ❗ {vuln_type} failed: {str(e)[:30]}...")
                self.findings[url][vuln_type] = "Error"

        print(f"\nScan completed in {time.time() - start_time:.1f}s")

    def generate_report(self):
        """Save findings in JSON format"""
        with open("scan_report.json", "w") as f:
            json.dump(self.findings, f, indent=4)
        print("\n📄 Report saved as scan_report.json")

if __name__ == "__main__":
    pentester = SmartPentester()
    
    # Configuration
    pentester.llm_enabled = True  # Set False for rule-based scanning only
    pentester.timeout = 15  # Adjust timeout if needed
    
    targets = [
        "http://bwapp.hakhub.net/login.php",
        "http://bwapp.hakhub.net/xss_get.php"
    ]
    
    for target in targets:
        pentester.scan_endpoint(target)

    pentester.generate_report()

class DefensiveMechanisms:
    def __init__(self):
        self.llm_model = "phi"  # AI model for mitigation analysis
        self.findings = self.load_scan_results()
        self.mitigations = {}

    def load_scan_results(self):
        """Load scan results from SmartPentester"""
        try:
            with open("scan_report.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("\n❌ Scan results not found! Run the scan first.")
            return {}

    def query_llm(self, prompt):
        """Use LLM to generate security fixes"""
        try:
            response = ollama.generate(
                model=self.llm_model,
                options={"num_ctx": 1024, "temperature": 0.3},
                prompt=prompt[:500]  # Truncate for stability
            )
            return response["response"]
        except Exception as e:
            print(f"\n[LLM Error] {str(e)[:80]}...")
            return None

    def generate_mitigation_report(self):
        """Suggest security fixes for detected vulnerabilities"""
        if not self.findings:
            print("\n⚠️ No vulnerabilities detected. No mitigation needed.")
            return
        
        print("\n🛡️  Generating security recommendations...")

        for url, issues in self.findings.items():
            self.mitigations[url] = {}

            for vuln, status in issues.items():
                if "Vulnerable" in status:
                    print(f"  🔹 Analyzing fix for {vuln} at {url}...")

                    llm_prompt = f"""
                    A security scan detected {vuln} vulnerability at {url}.
                    Suggest mitigation strategies to prevent this exploit.
                    Provide practical, implementable security measures.
                    """

                    fix = self.query_llm(llm_prompt)
                    self.mitigations[url][vuln] = fix if fix else "LLM analysis failed."

        # Save mitigation report
        with open("mitigation_report.json", "w") as f:
            json.dump(self.mitigations, f, indent=4)

        print("\n✅ Mitigation report saved as mitigation_report.json")

if __name__ == "__main__":
    # Run defensive module after scanning
    defense = DefensiveMechanisms()
    defense.generate_mitigation_report()


