import os
import csv
from platform import node
from unittest import result
from .verifier import CompanyVerifier
from .researcher import CompanyResearcher
from .personalizer import EmailPersonalizer
from .email_sender import EmailSender
from .errors import RuntimeError

from .ast import (
    ProgramNode,
    CampaignNode,
    LoadLeadsNode,
    SetNode,
    VerifyCompanyNode,
    ResearchCompanyNode,
    PersonalizeEmailNode,
    PreviewEmailNode,
    SendEmailNode,
    ForEachNode,
    IfNode,
)


class Interpreter:

    def __init__(self):
        self.campaign_name = None
        self.leads = []
        self.current_lead = None
        self.verified = False
        self.research = None
        self.email = None
        self.last_email_sent = False

        self.stats = {
            "total": 0,
            "verified": 0,
            "research_valid": 0,
            "emails_generated": 0,
            "emails_sent": 0,
            "skipped": 0,
            "failed": 0,
        }

        self.results = []

        self.verifier = CompanyVerifier()
        self.researcher = CompanyResearcher()
        self.personalizer = EmailPersonalizer()
        self.email_sender = EmailSender()

        self.research = None
        self.research_valid = False

        self.settings = {
            "tone": "PROFESSIONAL",
            "length": "SHORT",
            "SENDER":"ReachScript",
            "SUBJECT":"",
            "DRY_RUN":"TRUE",
        }

    def execute(self, node):

        if isinstance(node, ProgramNode):
            return self.execute_program(node)

        if isinstance(node, CampaignNode):
            return self.execute_campaign(node)

        if isinstance(node, LoadLeadsNode):
            return self.execute_load_leads(node)

        if isinstance(node, VerifyCompanyNode):
            return self.execute_verify_company(node)

        if isinstance(node, ResearchCompanyNode):
            return self.execute_research_company(node)

        if isinstance(node, PersonalizeEmailNode):
            return self.execute_personalize_email(node)

        if isinstance(node, PreviewEmailNode):
            return self.execute_preview_email(node)

        if isinstance(node, SendEmailNode):
            return self.execute_send_email(node)

        if isinstance(node, ForEachNode):
            return self.execute_for_each(node)

        if isinstance(node, IfNode):
            return self.execute_if(node)

        if isinstance(node, SetNode):
            return self.execute_set(node)

        raise RuntimeError(
            f"Unknown AST node: {type(node).__name__}"
        )


    def execute_program(self, node):
        for statement in node.statements:
            self.execute(statement)

        self.print_campaign_report()
        self.export_results()

    def execute_campaign(self, node):
        self.campaign_name = node.name

        print(f"\nCampaign: {self.campaign_name}")

    def execute_load_leads(self, node):
        print(f"Loading leads from: {node.filename}")

        possible_paths = [
            node.filename,
            os.path.join("sample_data", node.filename),
        ]

        file_path = None

        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break

        if file_path is None:
            raise RuntimeError(
                f"Could not find lead file: {node.filename}. "
                f"Make sure the file exists in the project directory "
                f"or inside the sample_data directory."
            )

        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            self.leads = list(reader)

            self.stats["total"] = len(self.leads)

        print(f"Loaded {len(self.leads)} leads")

    def execute_set(self, node):

        variable = node.variable.upper()
        value = node.value

        if variable == "TONE":

            allowed = ["PROFESSIONAL", "FRIENDLY"]

            if value.upper() not in allowed:
                raise RuntimeError(
                    f"Invalid tone '{value}'. "
                    f"Allowed values: PROFESSIONAL, FRIENDLY"
                )

            self.settings["TONE"] = value.upper()

        elif variable == "LENGTH":

            allowed = ["SHORT", "MEDIUM", "LONG"]

            if value.upper() not in allowed:
                raise RuntimeError(
                    f"Invalid length '{value}'. "
                    f"Allowed values: SHORT, MEDIUM, LONG"
                )

            self.settings["LENGTH"] = value.upper()

        elif variable == "SENDER":

            if not value.strip():
                raise RuntimeError(
                    "Sender cannot be empty"
                )

            self.settings["SENDER"] = value

        elif variable == "SUBJECT":

            if not value.strip():
                raise RuntimeError(
                    "Subject cannot be empty"
                )

            self.settings["SUBJECT"] = value

        elif variable == "SUBJECT":

            if not value.strip():
                raise RuntimeError(
                    "Subject cannot be empty"
                )

            self.settings["SUBJECT"] = value

        elif variable == "DRY_RUN":

            allowed = ["TRUE", "FALSE"]

            if value.upper() not in allowed:
                raise RuntimeError(
                    f"Invalid DRY_RUN value '{value}'. "
                    f"Allowed values: TRUE, FALSE"
                )

            self.settings["DRY_RUN"] = value.upper()

        else:

            raise RuntimeError(
                f"Unknown setting '{variable}'"
            )

        print(f"✓ Setting {variable} = {value}")

    def execute_verify_company(self, node):
        if self.current_lead is None:
            print("No lead selected for verification")
            self.verified = False
            return

        result = self.verifier.verify(self.current_lead)

        self.verified = result["verified"]

        if self.verified:
            self.stats["verified"] += 1

    def execute_research_company(self, node):
        if self.current_lead is None:
            print("No lead selected for research")
            self.research = None
            self.research_valid = False
            return

        self.research = self.researcher.research(
            self.current_lead
        )

        if self.research is None:
            self.research_valid = False

            print(
                "Research unavailable. "
                "Skipping personalization."
            )
        else:
            self.research_valid = True
            self.stats["research_valid"] += 1

    def execute_personalize_email(self, node):
        if self.current_lead is None:
            print("No lead selected for personalization")
            self.email = None
            return

        if not self.research_valid:
            print(
                "✗ Cannot personalize: "
                "valid research is unavailable"
            )
            self.email = None
            return

        tone = self.settings.get("TONE", "PROFESSIONAL")
        length = self.settings.get("LENGTH", "SHORT")
        sender = self.settings.get("SENDER", "ReachScript")

        self.email = self.personalizer.personalize(
            self.current_lead,
            self.research,
            tone=tone,
            length=length,
            sender=sender,
            use_verified_research=node.use_verified_research
        )

        if self.email:
            self.stats["emails_generated"] += 1
            print("✓ Personalized email generated")
        else:
            self.stats["failed"] += 1
            print("✗ Email personalization failed")

    def execute_preview_email(self, node):

        if not self.email:
            print("✗ Cannot preview: no email available")
            return

        subject = self.settings.get(
            "SUBJECT",
            ""
        )

        print("\n--- EMAIL PREVIEW ---")

        if subject:
            print(f"Subject: {subject}")
            print()

        print(self.email)

        print("---------------------")

    def execute_send_email(self, node):

        self.last_email_sent = False

        if self.current_lead is None:
            print("✗ No lead selected")
            return

        if not self.email:
            print("✗ No email available")
            return

        subject = self.settings.get(
            "SUBJECT",
            ""
        )

        sender = self.settings.get(
            "SENDER",
            "ReachScript"
        )

        dry_run = self.settings.get(
            "DRY_RUN",
            "TRUE"
        )

        dry_run = str(dry_run).upper() == "TRUE"

        result = self.email_sender.send(
            self.current_lead,
            self.email,
            subject,
            sender,
            dry_run
        )

        if result:

            if dry_run:
                self.stats["skipped"] += 1
            else:
                self.stats["emails_sent"] += 1
                self.last_email_sent = True

        else:
            self.stats["failed"] += 1

    def execute_for_each(self, node):

        for lead in self.leads:

            self.current_lead = lead

            # Reset state for the new lead
            self.verified = False
            self.research = None
            self.research_valid = False
            self.email = None

            print(
                f"\nProcessing: "
                f"{lead.get('name', 'Unknown')} "
                f"({lead.get('company', 'Unknown')})"
            )

            for statement in node.body:
                self.execute(statement)

            # Determine final lead status
            if self.last_email_sent:
                status = "SENT"
            elif not self.verified:
                status = "NOT_VERIFIED"
            elif not self.research_valid:
                status = "RESEARCH_FAILED"
            elif not self.email:
                status = "EMAIL_FAILED"
            else:
                status = "SKIPPED"

            self.results.append({
                "name": lead.get("name", ""),
                "company": lead.get("company", ""),
                "email": lead.get("email", ""),
                "verified": self.verified,
                "research_valid": self.research_valid,
                "email_generated": bool(self.email),
                "email_sent": status == "SENT",
                "status": status,
            })

    def execute_if(self, node):

        # Check the main IF condition
        if self.evaluate_condition(node.condition):

            for statement in node.body:
                self.execute(statement)

            return

        # Check ELSE IF conditions
        for condition, body in getattr(node, "else_if", []):

            if self.evaluate_condition(condition):

                for statement in body:
                    self.execute(statement)

                return

        # Execute ELSE
        for statement in getattr(node, "else_body", []):

            self.execute(statement)


    def evaluate_condition(self, condition):

        # Handle compound conditions
        if isinstance(condition, tuple):

            left, operator, right = condition

            left_result = self.evaluate_condition(left)
            right_result = self.evaluate_condition(right)

            if operator == "AND":
                return left_result and right_result

            if operator == "OR":
                return left_result or right_result

            return False

        condition = condition.upper()

        if condition == "VERIFIED":
            return self.verified

        if condition == "NOT_VERIFIED":
            return not self.verified

        if condition == "RESEARCH_VALID":
            return self.research_valid

        if condition == "NOT_RESEARCH_VALID":
            return not self.research_valid

        return False

    def print_campaign_report(self):

        print("\n")
        print("=" * 45)
        print("           CAMPAIGN REPORT")
        print("=" * 45)

        print(f"\nCampaign:          {self.campaign_name}")
        print(f"Total Leads:       {self.stats['total']}")
        print(f"Verified:          {self.stats['verified']}")
        print(f"Research Valid:    {self.stats['research_valid']}")
        print(f"Emails Generated:  {self.stats['emails_generated']}")
        print(f"Emails Sent:       {self.stats['emails_sent']}")
        print(f"Skipped:           {self.stats['skipped']}")
        print(f"Failed:            {self.stats['failed']}")

        print("\n" + "=" * 45)
        print("Campaign completed successfully.")
        print("=" * 45)


    def export_results(self, filename="campaign_results.csv"):

        if not self.results:
            print("\nNo campaign results to export.")
            return

        fieldnames = [
            "name",
            "company",
            "email",
            "verified",
            "research_valid",
            "email_generated",
            "email_sent",
            "status",
        ]

        os.makedirs("results", exist_ok=True)

        file_path = os.path.join("results", filename)

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(self.results)

        print(
            f"\n✓ Campaign results exported to: "
            f"{file_path}"
        )