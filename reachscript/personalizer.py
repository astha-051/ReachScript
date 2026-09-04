from .ai_client import GeminiClient


class EmailPersonalizer:

    def __init__(self):
        self.ai = GeminiClient()

    def personalize(self, lead, research, tone="PROFESSIONAL", length="SHORT", use_verified_research=True, sender="ReachScript"):
        if not lead:
            print("✗ No lead available")
            return None

        if not research:
            print("✗ No research available")
            return None

        name = lead.get("name", "").strip()
        company = lead.get("company", "").strip()
        role = lead.get("role", "").strip()

        website = research.get("website", "")
        title = research.get("title", "")
        description = research.get("description", "")
        headings = research.get("headings", [])

        headings_text = "\n".join(
            f"- {heading}"
            for heading in headings
        )

        prompt = f"""
You are a strict B2B email personalization assistant.

Your job is to write a short, professional cold outreach email
using ONLY the evidence provided below.

RECIPIENT INFORMATION
Name: {name}
Role: {role}
Company: {company}

VERIFIED WEBSITE
{website}

VERIFIED RESEARCH
Page title:
{title}

Description:
{description}

Relevant headings:
{headings_text}

PERSONALIZATION SETTINGS
Tone: {tone}
Length: {length}
Use verified research only: {use_verified_research}
SENDER:
{sender}

STRICT EVIDENCE RULES

1. Treat the recipient name, role, and company as lead-provided
   information. Do not add facts about the person beyond these fields.

2. Treat the website, title, description, and headings as
   researched information.

3. You may mention ONLY facts explicitly present in the
   information above.

4. NEVER infer or assume:
   - the person's responsibilities
   - the company's goals
   - the company's problems
   - the company's customers
   - the company's products
   - the company's achievements
   - the company's industry
   - the company's size
   - revenue or statistics

5. If there is not enough research for a specific observation,
   do NOT invent one.

6. If "Use verified research only" is True,
   base personalization on the researched information provided
   above and do not use unsupported assumptions.

7. AI-powered automation may be presented as a potential idea,
   but never claim that the company needs it.

8. Follow the requested tone exactly.

9. Follow the requested length exactly.

10. Keep the email natural and professional.

11. Do not mention that you are an AI.

12. Do not use exaggerated marketing language.

13. Include a low-pressure call to action.

14. Do not include a subject line.

15. End the email with:

Best,
{sender}

16. Return ONLY the email body.

EMAIL STRUCTURE

Hi [Name],

Use a factual observation only if the research supports one.

Briefly introduce AI-powered automation as a potential
area worth exploring, without claiming that the company
has a specific problem.

Ask a low-pressure question.

Best,
ReachScript
"""

        try:
            email = self.ai.generate(prompt)

            if not email:
                print("✗ Gemini returned an empty response")
                return None

            return email.strip()

        except Exception as error:
            print(f"✗ AI personalization failed: {error}")
            return None