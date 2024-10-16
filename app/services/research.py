import asyncio
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.models.research import ResearchResponse, Outline, Section
from app.services.language_models import get_fast_llm, get_long_context_llm
from app.services.retrieval import get_retriever


async def conduct_research(topic: str) -> ResearchResponse:
    fast_llm = await get_fast_llm()
    long_context_llm = await get_long_context_llm()
    retriever = await get_retriever()

    # Generate initial outline
    outline_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific."),
        ("user", "{topic}")
    ])
    outline_chain = outline_prompt | fast_llm.with_structured_output(Outline)
    try:
        outline = await outline_chain.ainvoke({"topic": topic})
    except Exception as e:
        if "string too long" in str(e):
            # Fallback to a simpler outline generation
            outline = await generate_simple_outline(topic, fast_llm)
        else:
            raise e

    # Conduct interviews (simplified for this example)
    interview_results = await asyncio.gather(*[
        simulate_interview(topic, fast_llm) for _ in range(3)
    ])

    # Refine outline
    refine_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Refine the outline based on the interviews:\n\n{interviews}"),
        ("user", "Refine this outline:\n\n{outline}")
    ])
    refine_chain = refine_prompt | long_context_llm | StrOutputParser()
    refined_outline_str = await refine_chain.ainvoke({
        "interviews": "\n\n".join(interview_results),
        "outline": outline.model_dump_json()
    })
    refined_outline = parse_outline(refined_outline_str)

    # Generate article
    article_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Write a complete Wikipedia article based on this outline:\n\n{outline}"),
        ("user", "Write the article using markdown format.")
    ])
    article_chain = article_prompt | long_context_llm | StrOutputParser()
    article = await article_chain.ainvoke({"outline": refined_outline.model_dump_json()})

    return ResearchResponse(topic=topic, outline=refined_outline, article=article)


async def simulate_interview(topic: str, llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert on {topic}. Provide some insights."),
        ("user", "What are the key points about {topic}?")
    ])
    chain = prompt | llm | StrOutputParser()
    return await chain.ainvoke({"topic": topic})


async def generate_simple_outline(topic: str, llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Create a simple outline for a Wikipedia page about the given topic. Include only main section titles."),
        ("user", "{topic}")
    ])
    chain = prompt | llm | StrOutputParser()
    result = await chain.ainvoke({"topic": topic})

    # Parse the result into an Outline object
    sections = [Section(section_title=line.strip(), description="")
                for line in result.split('\n') if line.strip()]
    return Outline(page_title=topic, sections=sections)


def parse_outline(outline_str: str) -> Outline:
    lines = outline_str.split('\n')
    page_title = lines[0].strip()
    sections = []
    current_section = None

    for line in lines[1:]:
        if line.startswith('##'):
            if current_section:
                sections.append(current_section)
            current_section = Section(section_title=line.strip(
                '# '), description="", subsections=[])
        elif line.startswith('###'):
            if current_section:
                current_section.subsections.append(line.strip('# '))
        else:
            if current_section:
                current_section.description += line.strip() + " "

    if current_section:
        sections.append(current_section)

    return Outline(page_title=page_title, sections=sections)
