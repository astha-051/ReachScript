import requests
from bs4 import BeautifulSoup


class CompanyVerifier:

    def verify(self, lead):
        company = lead.get("company", "").strip()
        website = lead.get("website", "").strip()

        result = {
            "company": company,
            "website": website,
            "company_name_present": bool(company),
            "website_present": bool(website),
            "website_reachable": False,
            "company_name_found": False,
            "verified": False,
        }

        print(f"\nVerifying company: {company}")

        # 1. Check company name
        if result["company_name_present"]:
            print("✓ Company name provided")
        else:
            print("✗ Company name missing")

        # 2. Check website
        if result["website_present"]:
            print("✓ Website provided")
        else:
            print("✗ Website missing")

        # 3. Check website and get its content
        page_content = None

        if website:
            page_content = self.get_website_content(website)

            if page_content:
                result["website_reachable"] = True
                print("✓ Website reachable")
            else:
                print("✗ Website unreachable")

        # 4. Check whether company name appears
        #    in the website content
        if page_content and company:
            company_found = self.company_name_matches(
                company,
                page_content
            )

            result["company_name_found"] = company_found

            if company_found:
                print("✓ Company name found on website")
            else:
                print("✗ Company name not found on website")

        # 5. Final verification
        result["verified"] = (
            result["company_name_present"]
            and result["website_present"]
            and result["website_reachable"]
            and result["company_name_found"]
        )

        if result["verified"]:
            print("Company status: VERIFIED")
        else:
            print("Company status: NOT VERIFIED")

        return result

    def get_website_content(self, website):
        try:
            response = requests.get(
                website,
                timeout=5,
                headers={
                    "User-Agent": "ReachScript/1.0"
                }
            )

            if not (200 <= response.status_code < 400):
                return None

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Remove things that are not useful
            # for company verification.
            for tag in soup(
                ["script", "style", "noscript"]
            ):
                tag.decompose()

            return soup.get_text(
                " ",
                strip=True
            )

        except requests.RequestException:
            return None

    def company_name_matches(
        self,
        company,
        page_content
    ):
        company = company.lower().strip()
        page_content = page_content.lower()

        return company in page_content