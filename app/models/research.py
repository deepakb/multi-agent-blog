from pydantic import BaseModel, Field
from typing import List, Optional


class Subsection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    description: str = Field(..., title="Content of the subsection")


class Section(BaseModel):
    section_title: str = Field(..., description="Section title")
    description: str = Field(..., description="Section content")
    subsections: Optional[List[str]] = Field(
        default=None, description="Subsections")


class Outline(BaseModel):
    page_title: str = Field(..., description="Title of the page")
    sections: List[Section] = Field(
        default_factory=list, description="Sections")


class Editor(BaseModel):
    affiliation: str = Field(
        description="Primary affiliation of the editor.",
    )
    name: str = Field(
        description="Name of the editor.", pattern=r"^[a-zA-Z0-9_-]{1,64}$"
    )
    role: str = Field(
        description="Role of the editor in the context of the topic.",
    )
    description: str = Field(
        description="Description of the editor's focus, concerns, and motives.",
    )


class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The research topic")


class ResearchResponse(BaseModel):
    topic: str
    outline: Outline
    article: str
