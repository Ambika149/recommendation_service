from typing import List
from pydantic import BaseModel


# Define Pydantic models for the input and output data
class Preferences(BaseModel):
    desired_roles: List[str]
    locations: List[str]
    job_type: str


class UserProfileModel(BaseModel):
    name: str
    skills: List[str]
    experience_level: str
    preferences: Preferences
