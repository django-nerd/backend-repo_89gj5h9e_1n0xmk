from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents
from schemas import Contact, CaseStudy, Service

app = FastAPI(title="Zhurme Marketing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactResponse(BaseModel):
    status: str
    message: str


@app.get("/", tags=["root"])
async def root():
    return {"status": "ok", "service": "Zhurme Marketing API"}


@app.post("/contact", response_model=ContactResponse, tags=["contact"])
async def submit_contact(contact: Contact):
    try:
        create_document("contact", contact.dict())
        return {"status": "success", "message": "Thanks! We'll reach out within 24 hours."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/services", response_model=List[Service], tags=["content"])
async def list_services():
    # Seed default services if none exist
    existing = get_documents("service", {}, limit=100)
    if not existing:
        defaults: List[Service] = [
            Service(
                name="Performance Marketing",
                description="ROI-focused campaigns across search, social, and programmatic.",
                highlights=["Google & Meta Ads", "Conversion Tracking", "A/B Testing"],
                icon="trending-up",
            ),
            Service(
                name="Brand & Creative",
                description="Distinct brand systems and scroll-stopping creative.",
                highlights=["Visual Identity", "Art Direction", "Motion"],
                icon="sparkles",
            ),
            Service(
                name="Web & Product",
                description="Fast, accessible websites and interactive experiences.",
                highlights=["React/Next.js", "SEO", "Analytics"],
                icon="code-2",
            ),
        ]
        for s in defaults:
            create_document("service", s.dict())
        existing = get_documents("service", {}, limit=100)
    # Map to Service models (drop mongo fields)
    cleaned: List[Service] = []
    for it in existing:
        cleaned.append(
            Service(
                name=it.get("name", ""),
                description=it.get("description", ""),
                highlights=it.get("highlights", []),
                icon=it.get("icon"),
            )
        )
    return cleaned


@app.get("/case-studies", response_model=List[CaseStudy], tags=["content"])
async def list_case_studies():
    existing = get_documents("casestudy", {}, limit=100)
    if not existing:
        defaults: List[CaseStudy] = [
            CaseStudy(
                title="10x ROAS in 90 Days",
                client="Acme DTC",
                summary="Scaled paid social and rebuilt landing funnel for profitable growth.",
                impact=["+310% revenue", "-42% CPA", "+1.4s faster LCP"],
                image=None,
                url="#",
            ),
            CaseStudy(
                title="From Zero to Category Leader",
                client="Nimbus SaaS",
                summary="Positioning, brand system, and demand engine to dominate SERPs.",
                impact=["#1 for 18 keywords", "+220% demo volume", "5x organic traffic"],
                image=None,
                url="#",
            ),
        ]
        for c in defaults:
            create_document("casestudy", c.dict())
        existing = get_documents("casestudy", {}, limit=100)
    cleaned: List[CaseStudy] = []
    for it in existing:
        cleaned.append(
            CaseStudy(
                title=it.get("title", ""),
                client=it.get("client", ""),
                summary=it.get("summary", ""),
                impact=it.get("impact", []),
                image=it.get("image"),
                url=it.get("url"),
            )
        )
    return cleaned
