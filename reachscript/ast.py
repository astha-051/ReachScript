from dataclasses import dataclass, field
from typing import List
from dataclasses import dataclass, field


class ASTNode:
    """Base class for all ReachScript AST nodes."""
    pass


@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]


@dataclass
class CampaignNode(ASTNode):
    name: str


@dataclass
class LoadLeadsNode(ASTNode):
    filename: str


@dataclass
class VerifyCompanyNode(ASTNode):
    pass


@dataclass
class ResearchCompanyNode(ASTNode):
    pass


@dataclass
class PersonalizeEmailNode(ASTNode):
    tone: str = "PROFESSIONAL"
    length: str = "SHORT"
    use_verified_research: bool = False

@dataclass
class PreviewEmailNode(ASTNode):
    pass


@dataclass
class SendEmailNode(ASTNode):
    pass


@dataclass
class ForEachNode(ASTNode):
    variable: str
    body: List[ASTNode]


@dataclass
class IfNode:
    condition: str
    body: list
    else_if: list = field(default_factory=list)
    else_body: list = field(default_factory=list)

@dataclass
class SetNode(ASTNode):

    variable: str
    value: str