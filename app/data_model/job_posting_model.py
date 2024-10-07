from typing import List
from pydantic import BaseModel

# Pydantic model for Job Posting output
class JobPosting(BaseModel):
    job_title: str
    company: str
    location: str
    job_type: str
    required_skills: List[str]
    experience_level: str

    class Config:
        orm_mode = True
