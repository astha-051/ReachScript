import requests
from bs4 import BeautifulSoup


class CompanyResearcher:

    BLOCKED_PHRASES = [
        "request has been blocked",
        "access denied",
        "access forbidden",
        "403 forbidden",
        "captcha",
        "verify you are human",
        "unusual traffic",
        "automated requests",
        "bot detection",
        "security check",
        "temporarily blocked",
    ]

    def research(self, lead):
        company = lead.get("company", "").strip()
        website = lead.get("website", "").strip()

        print(f"Researching company: {company}")

        if not website:
            print("✗ No website available")
            return None

        try:
            response = requests.get(
                website,
                timeout=10,
                headers={
                    "User-Agent": "ReachScript/1.0"
                }
            )

            if not (200 <= response.status_code < 400):
                print(
                    f"✗ Website returned "
                    f"status {response.status_code}"
                )
                return None

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = self.extract_title(soup)
            description = self.extract_description(soup)
            headings = self.extract_headings(soup)
            text = self.extract_main_text(soup)

            # Validate before returning research
            if not self.is_valid_research(
                title,
                description,
                headings,
                text
            ):
                print(
                    "✗ Research appears blocked "
                    "or insufficient"
                )
                return None

            research = {
                "company": company,
                "website": website,
                "title": title,
                "description": description,
                "headings": headings,
                "text": text,
            }

            print("✓ Company research completed")

            if title:
                print(f"  Title: {title}")

            if description:
                print(
                    f"  Description: "
                    f"{description}"
                )

            return research

        except requests.RequestException as error:
            print(f"✗ Research failed: {error}")
            return None

    def is_valid_research(
        self,
        title,
        description,
        headings,
        text
    ):
        combined_text = " ".join([
            title,
            description,
            " ".join(headings),
            text
        ]).lower()

        # Detect common blocking/error pages
        for phrase in self.BLOCKED_PHRASES:
            if phrase in combined_text:
                return False

        # Require at least some meaningful content
        meaningful_content = (
            len(description) >= 20
            or len(headings) >= 1
            or len(text) >= 100
        )

        if not meaningful_content:
            return False

        return True

    def extract_title(self, soup):
        if soup.title:
            return soup.title.get_text(
                strip=True
            )

        return ""

    def extract_description(self, soup):
        tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if tag and tag.get("content"):
            return tag["content"].strip()

        return ""

    def extract_headings(self, soup):
        headings = []

        for tag in soup.find_all(
            ["h1", "h2", "h3"]
        ):
            text = tag.get_text(
                " ",
                strip=True
            )

            if text:
                headings.append(text)

        return headings[:15]

    def extract_main_text(self, soup):
        for tag in soup(
            ["script", "style", "noscript"]
        ):
            tag.decompose()

        text = soup.get_text(
            " ",
            strip=True
        )

        return text[:8000]