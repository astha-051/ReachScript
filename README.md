# ReachScript

> **A domain-specific language for intelligent, personalized business outreach automation.**

ReachScript is a **Domain-Specific Language (DSL)** designed to simplify business outreach automation.

Instead of writing Python code to verify companies, research websites, generate personalized emails, preview messages, and send emails, users can describe the entire workflow using a simple, readable ReachScript program.

```text
CAMPAIGN "Tech Outreach"

SET TONE = FRIENDLY
SET LENGTH = SHORT
SET SENDER = "ReachScript AI"
SET SUBJECT = "AI Automation for Your Company"
SET DRY_RUN = TRUE

LOAD LEADS FROM "leads.csv"

FOR EACH LEAD
    VERIFY COMPANY
    RESEARCH COMPANY
    PERSONALIZE EMAIL
    PREVIEW EMAIL
    SEND EMAIL
END
```

ReachScript translates this high-level campaign definition into an executable workflow.

---

## 🚀 Why ReachScript?

Traditional outreach automation often requires developers to connect multiple services manually:

* Lead data processing
* Website verification
* Company research
* AI-based personalization
* Email generation
* Email delivery
* Campaign tracking
* Error handling

This creates unnecessary technical complexity for users who simply want to describe **what their campaign should do**.

ReachScript introduces a higher-level abstraction.

Instead of implementing the workflow in Python, users can write:

```text
VERIFY COMPANY
RESEARCH COMPANY
PERSONALIZE EMAIL
SEND EMAIL
```

The ReachScript interpreter handles the underlying implementation.

### The idea

**Turn business automation logic into a readable programming language.**

---

# ✨ Features

ReachScript currently supports:

* Campaign definitions
* Configurable email tone
* Configurable email length
* Custom sender name
* Custom email subject
* Dry-run mode
* Real email sending through SMTP
* CSV lead loading
* Lead-by-lead processing
* Company verification
* Website research
* AI-powered email personalization
* Email preview
* Conditional execution
* `AND` conditions
* `OR` conditions
* `NOT` conditions
* `IF / ELSE` blocks
* Runtime error handling
* Campaign statistics
* Campaign result export to CSV
* Lexer and parser
* Abstract Syntax Tree (AST)
* Interpreter-based execution
* Automated tests

---

# 🧠 How ReachScript Works

ReachScript follows a compiler/interpreter-style pipeline:

```text
ReachScript Program
        │
        ▼
      Lexer
        │
        ▼
     Tokens
        │
        ▼
      Parser
        │
        ▼
       AST
        │
        ▼
   Interpreter
        │
        ├───────────────┐
        ▼               ▼
 Company Verification  Research
        │               │
        └───────┬───────┘
                ▼
        AI Personalization
                │
                ▼
          Email Preview
                │
                ▼
           Email Sender
                │
                ▼
         Campaign Report
                │
                ▼
        CSV Result Export
```

### 1. Lexer

The lexer converts the ReachScript source code into tokens.

For example:

```text
SET TONE = FRIENDLY
```

becomes tokens representing:

```text
SET
TONE
=
FRIENDLY
```

### 2. Parser

The parser converts the token stream into an Abstract Syntax Tree.

Example:

```text
CAMPAIGN "Tech Outreach"
```

becomes a structure such as:

```text
CampaignNode(name="Tech Outreach")
```

### 3. AST

The AST represents the structure and meaning of the ReachScript program.

Examples of supported nodes include:

```text
ProgramNode
CampaignNode
SetNode
LoadLeadsNode
VerifyCompanyNode
ResearchCompanyNode
PersonalizeEmailNode
PreviewEmailNode
SendEmailNode
ForEachNode
IfNode
```

### 4. Interpreter

The interpreter walks through the AST and executes each operation.

This allows the DSL to control the complete campaign workflow.

---

# 📦 Project Structure

```text
ReachScript/
│
├── reachscript/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ast.py
│   ├── interpreter.py
│   ├── errors.py
│   ├── verifier.py
│   ├── researcher.py
│   ├── personalizer.py
│   └── email_sender.py
│
├── examples/
│   ├── basic.reach
│   ├── verification.reach
│   ├── conditions.reach
│   └── real_email.reach
│
├── sample_data/
│   └── leads.csv
│
├── results/
│   └── campaign_results.csv
│
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_interpreter.py
│   └── test_email_sender.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd ReachScript
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

ReachScript can use external services for AI personalization and email delivery.

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_app_password
```

Never commit your real API keys or email passwords to GitHub.

Add the environment file to `.gitignore`:

```text
.env
```

For Gmail SMTP, use a **Google App Password** rather than your normal Gmail password.

---

# 📄 Lead CSV Format

ReachScript loads leads from CSV files.

Example:

```csv
name,company,email,website,role
Rahul,Google,rahul@example.com,https://www.google.com,CEO
Priya,Microsoft,priya@example.com,https://www.microsoft.com,CTO
Amit,DataFlow,amit@example.com,https://dataflow-example.com,Founder
```

### Required fields

```text
name
company
email
website
```

Additional fields can be included for personalization.

For example:

```text
role
industry
location
pain_point
```

---

# 📖 ReachScript Language

## CAMPAIGN

Defines the campaign name.

```text
CAMPAIGN "Tech Outreach"
```

---

## SET

Configures campaign settings.

### Tone

```text
SET TONE = FRIENDLY
```

Supported values:

```text
PROFESSIONAL
FRIENDLY
```

### Length

```text
SET LENGTH = SHORT
```

Supported values:

```text
SHORT
MEDIUM
LONG
```

### Sender

```text
SET SENDER = "ReachScript AI"
```

### Subject

```text
SET SUBJECT = "AI Automation for Your Company"
```

### Dry Run

```text
SET DRY_RUN = TRUE
```

Possible values:

```text
TRUE
FALSE
```

---

# 📂 LOAD LEADS

Loads leads from a CSV file.

```text
LOAD LEADS FROM "leads.csv"
```

ReachScript searches for the specified file and can also look inside the `sample_data` directory.

---

# 🔁 FOR EACH LEAD

Processes each lead individually.

```text
FOR EACH LEAD

    VERIFY COMPANY
    RESEARCH COMPANY
    PERSONALIZE EMAIL

END
```

The interpreter sets the current lead before executing the statements inside the loop.

---

# 🔍 VERIFY COMPANY

Verifies the company information and website.

```text
VERIFY COMPANY
```

The verification process can check:

* Company name availability
* Website availability
* Website reachability
* Company name presence on the website

Example result:

```text
Verifying company: Google
✓ Company name provided
✓ Website provided
✓ Website reachable
✓ Company name found on website
Company status: VERIFIED
```

---

# 🌐 RESEARCH COMPANY

Researches the company's website.

```text
RESEARCH COMPANY
```

Research information can then be used by the AI personalization system.

If research is unavailable or blocked, ReachScript handles the failure instead of assuming that research succeeded.

---

# 🤖 PERSONALIZE EMAIL

Generates a personalized email using the available lead and company information.

```text
PERSONALIZE EMAIL
```

The personalization system considers settings such as:

```text
TONE
LENGTH
SENDER
```

and available company research.

Example:

```text
Hi Rahul,

My team at ReachScript AI helps companies explore the potential
of AI-powered automation to streamline operations.

Would you be open to a quick chat to see if there's a fit for Google?

Best,
ReachScript AI
```

---

# 👀 PREVIEW EMAIL

Displays the generated email before sending.

```text
PREVIEW EMAIL
```

Example:

```text
--- EMAIL PREVIEW ---

Subject: AI Automation for Your Company

Hi Rahul,

...

Best,
ReachScript AI

---------------------
```

---

# 📧 SEND EMAIL

Sends the generated email through the configured email provider.

```text
SEND EMAIL
```

The actual behavior depends on `DRY_RUN`.

---

# 🛡️ DRY RUN MODE

Dry-run mode is enabled by default for safer testing.

```text
SET DRY_RUN = TRUE
```

The email is prepared but not actually sent.

Example:

```text
📧 EMAIL READY TO SEND

From: ReachScript AI
To: rahul@example.com
Subject: AI Automation for Your Company
Status: DRY RUN

Email was NOT actually sent.
```

This makes it possible to test campaigns safely before enabling real delivery.

---

# 📤 REAL EMAIL MODE

To actually send emails:

```text
SET DRY_RUN = FALSE
```

Example:

```text
SET SENDER = "ReachScript AI"
SET SUBJECT = "AI Automation Opportunity"
SET DRY_RUN = FALSE

SEND EMAIL
```

Successful delivery produces:

```text
📧 EMAIL SENT SUCCESSFULLY

From: ReachScript AI
To: recipient@example.com
Subject: AI Automation Opportunity
```

> **Warning:** `DRY_RUN = FALSE` sends real emails. Use a test account and test recipients during development.

---

# 🧩 Conditional Logic

ReachScript supports conditional campaign logic.

## IF

```text
IF VERIFIED
    RESEARCH COMPANY
END
```

---

## IF / ELSE

```text
IF VERIFIED
    RESEARCH COMPANY
ELSE
    LOAD LEADS FROM "failed.csv"
END
```

---

## NOT

```text
IF NOT VERIFIED
    ...
END
```

---

## AND

Multiple conditions can be combined:

```text
IF VERIFIED AND RESEARCH_VALID
    PERSONALIZE EMAIL
END
```

---

## OR

```text
IF VERIFIED OR RESEARCH_VALID
    PERSONALIZE EMAIL
END
```

This allows campaign logic to be expressed directly in the DSL instead of implementing conditional logic in Python.

---

# 📊 Campaign Reporting

After execution, ReachScript generates a campaign report.

Example:

```text
=============================================
           CAMPAIGN REPORT
=============================================

Campaign:          Tech Outreach
Total Leads:       3
Verified:          2
Research Valid:    1
Emails Generated:  1
Emails Sent:       0
Skipped:           1
Failed:            0

=============================================
Campaign completed successfully.
=============================================
```

This gives the user an immediate summary of campaign execution.

---

# 📈 Result Export

Campaign results can also be exported to CSV.

Example:

```text
results/campaign_results.csv
```

Example contents:

```csv
name,company,email,verified,research_valid,email_generated,email_sent,status
Rahul,Google,rahul@example.com,True,True,True,False,SKIPPED
Priya,Microsoft,priya@example.com,True,False,False,False,RESEARCH_FAILED
Amit,DataFlow,amit@example.com,False,False,False,False,NOT_VERIFIED
```

This makes campaign execution auditable and provides data that can be processed by other systems.

---

# 🧪 Testing

ReachScript contains tests for the major components.

## Lexer Test

```bash
python -m tests.test_lexer
```

This verifies that ReachScript source code is correctly converted into tokens.

---

## Parser Test

```bash
python -m tests.test_parser
```

This verifies that tokens are correctly converted into an AST.

---

## Interpreter Test

```bash
python -m tests.test_interpreter
```

This executes a complete ReachScript program.

---

## Email Sender Test

```bash
python -m tests.test_email_sender
```

This tests the email sending layer.

Use dry-run mode while developing to avoid accidentally sending emails.

---

# 📝 Complete Example

A complete ReachScript campaign can look like this:

```text
CAMPAIGN "Tech Outreach"

SET TONE = FRIENDLY
SET LENGTH = SHORT
SET SENDER = "ReachScript AI"
SET SUBJECT = "AI Automation for Your Company"
SET DRY_RUN = TRUE

LOAD LEADS FROM "leads.csv"

FOR EACH LEAD

    VERIFY COMPANY
    RESEARCH COMPANY
    PERSONALIZE EMAIL
    PREVIEW EMAIL
    SEND EMAIL

END
```

This single program represents the complete workflow:

```text
Load
  ↓
Verify
  ↓
Research
  ↓
Personalize
  ↓
Preview
  ↓
Send
  ↓
Report
  ↓
Export
```

---

# 🎯 Example: Conditional Outreach

ReachScript can also express decision-making logic.

```text
CAMPAIGN "Verified Outreach"

SET TONE = FRIENDLY
SET LENGTH = SHORT
SET DRY_RUN = TRUE

LOAD LEADS FROM "leads.csv"

FOR EACH LEAD

    VERIFY COMPANY
    RESEARCH COMPANY

    IF VERIFIED AND RESEARCH_VALID
        PERSONALIZE EMAIL
        PREVIEW EMAIL
        SEND EMAIL
    END

END
```

The important idea is that the **business rule is written directly in the DSL**.

The user does not need to implement the condition in Python.

---

# 🏗️ Architecture

ReachScript is divided into several layers.

### Lexer

Responsible for:

```text
Source Code → Tokens
```

### Parser

Responsible for:

```text
Tokens → AST
```

### AST

Represents the structure of the ReachScript program.

### Interpreter

Responsible for executing the AST.

### Verification Layer

Responsible for checking company information.

### Research Layer

Responsible for obtaining company information from websites.

### AI Personalization Layer

Responsible for generating personalized outreach content.

### Email Layer

Responsible for previewing and delivering emails.

### Reporting Layer

Responsible for campaign statistics and CSV export.

This separation keeps the DSL implementation modular.

---

# 💡 What Makes ReachScript a DSL?

ReachScript is designed around a specific domain:

> **Business outreach and lead automation.**

It does not attempt to replace Python or become a general-purpose programming language.

Instead, it provides specialized abstractions such as:

```text
VERIFY COMPANY
RESEARCH COMPANY
PERSONALIZE EMAIL
SEND EMAIL
```

These operations represent meaningful business actions.

A user can therefore describe **what should happen** without needing to know how each operation is implemented internally.

This is the core idea behind ReachScript.

---

# 🔒 Safety Considerations

ReachScript includes several safeguards.

### Dry-run by default

Email delivery can be tested without actually sending messages.

```text
SET DRY_RUN = TRUE
```

### Runtime validation

Invalid settings generate ReachScript errors instead of silently continuing.

Example:

```text
SET TONE = UNKNOWN
```

can produce:

```text
ReachScript Error:
Invalid tone 'UNKNOWN'.
Allowed values: PROFESSIONAL, FRIENDLY
```

### Missing files

If a lead file cannot be found:

```text
ReachScript Error:
Could not find lead file: abc.csv.
```

### Missing email

If a lead does not contain an email address:

```text
ReachScript Error:
Lead 'Rahul' does not have an email address.
Add an 'email' column to your leads CSV.
```

These errors make failures easier for users to understand.

---

# 🚀 Future Improvements

Possible future versions of ReachScript could include:

* More advanced lead filtering
* Lead scoring
* Campaign scheduling
* Multiple email providers
* LinkedIn outreach
* CRM integrations
* More sophisticated research
* Better retry handling for AI/API failures
* Richer conditional expressions
* Variables and reusable functions
* Campaign analytics dashboard
* Parallel lead processing
* Additional export formats
* Plugin support
* More sophisticated AI personalization rules

These features can expand ReachScript while keeping its core DSL abstraction simple.

---

# 🏆 Hackathon Concept

ReachScript demonstrates how a domain-specific language can simplify a real-world automation problem.

Instead of writing a large automation script, a user can express a campaign in a few readable commands:

```text
LOAD LEADS
VERIFY COMPANY
RESEARCH COMPANY
PERSONALIZE EMAIL
SEND EMAIL
```

The interpreter converts these high-level instructions into an executable workflow.

### Core value proposition

> **ReachScript turns complex outreach automation into a readable, executable language.**

---

# 📌 Current Status

ReachScript currently demonstrates:

* A custom lexer
* A custom parser
* AST-based representation
* An interpreter
* Campaign configuration
* CSV lead processing
* Company verification
* Website research
* AI email personalization
* Email preview
* SMTP email delivery
* Dry-run protection
* Conditional logic
* Runtime error handling
* Campaign reporting
* CSV result export
* End-to-end campaign execution

---

# 👩‍💻 Development

ReachScript is being developed as an experimental DSL for business automation.

The project focuses on exploring how **domain-specific languages, AI, web research, and automation** can be combined into a single developer-friendly workflow.

---

# 📄 License

Add your preferred license here, such as:

```text
MIT License
```

if you decide to release the project under the MIT License.

---

# ⭐ Final Example

The entire idea of ReachScript can be summarized by this:

```text
CAMPAIGN "AI Outreach"

SET TONE = FRIENDLY
SET LENGTH = SHORT
SET DRY_RUN = TRUE

LOAD LEADS FROM "leads.csv"

FOR EACH LEAD

    VERIFY COMPANY

    IF VERIFIED
        RESEARCH COMPANY
        PERSONALIZE EMAIL
        PREVIEW EMAIL
        SEND EMAIL
    END

END
```

**Write the workflow. Let ReachScript execute it.**

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/astha-051/ReachScript.git
cd ReachScript
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_app_password
```

> Never commit your `.env` file to GitHub. Use `.env.example` as a template.

### 5. Run a ReachScript program

ReachScript programs use the `.reach` file extension.

The easiest way to run a program is:

```bash
python run.py examples/basic.reach
```

You can also run the other example programs:

```bash
python run.py examples/conditional.reach
```

```bash
python run.py examples/advanced.reach
```

For the SMTP email demonstration:

```bash
python run.py examples/real_email.reach
```

⚠️ `real_email.reach` contains:

```reach
SET DRY_RUN = FALSE
```

This enables actual email sending. For safe testing, change it to:

```reach
SET DRY_RUN = TRUE
```

### 6. Write your own ReachScript program

Create a `.reach` file inside the `examples/` directory.

For example:

```reach
CAMPAIGN "My First Campaign"

SET TONE = FRIENDLY
SET LENGTH = SHORT
SET SENDER = "ReachScript AI"
SET SUBJECT = "AI Automation Opportunity"
SET DRY_RUN = TRUE

LOAD LEADS FROM "leads.csv"

FOR EACH LEAD

    VERIFY COMPANY
    RESEARCH COMPANY
    PERSONALIZE EMAIL
    PREVIEW EMAIL
    SEND EMAIL

END
```

Then run it with:

```bash
python run.py examples/my_campaign.reach
```

### 📁 Understanding the project structure

```text
ReachScript/
│
├── run.py                    # Main CLI entry point
│
├── reachscript/              # ReachScript language implementation
│   ├── lexer.py              # Converts source code into tokens
│   ├── parser.py             # Builds the program structure
│   ├── interpreter.py        # Executes ReachScript programs
│   ├── verifier.py           # Company verification
│   ├── researcher.py         # Company research
│   ├── personalizer.py       # AI email personalization
│   ├── email_sender.py       # SMTP email sending
│   ├── errors.py             # ReachScript error handling
│   └── ...
│
├── examples/                 # Example ReachScript programs
│   ├── basic.reach
│   ├── conditional.reach
│   ├── advanced.reach
│   └── real_email.reach
│
├── sample_data/              # Sample lead CSV files
│   ├── leads.csv
│   └── demo_leads.csv
│
├── tests/                    # Language and component tests
│
├── results/                  # Generated campaign results
│
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore
└── README.md
```

### 🧪 Running the tests

The examples above demonstrate how to **use ReachScript**.

The test modules are for developers working on the language:

```bash
python -m tests.test_lexer
```

```bash
python -m tests.test_parser
```

```bash
python -m tests.test_interpreter
```

```bash
python -m tests.test_email_sender
```

### ⭐ Which file should I run?

If you are a **new user**, start with:

```bash
python run.py examples/basic.reach
```

If you want to see conditional logic:

```bash
python run.py examples/conditional.reach
```

If you want to see advanced conditions:

```bash
python run.py examples/advanced.reach
```

If you want to demonstrate actual SMTP email sending:

```bash
python run.py examples/real_email.reach
```

**You normally do not need to run anything inside `tests/`.**

The `run.py` file is the main entry point for executing ReachScript programs.

