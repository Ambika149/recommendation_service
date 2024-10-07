from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.ORM_model import SessionLocal, JobPosting as ORMJobPosting, UserProfile, engine  # Adjusted import for ORM model
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()


# Create the database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


# Pydantic model for Job Posting output
class JobPosting(BaseModel):
    job_title: str
    company: str
    location: str
    job_type: str
    required_skills: List[str]
    experience_level: str

    class Config:
        orm_mode = True  # Enables reading from SQLAlchemy models


# Recommendation logic
def match_jobs(user_profile: UserProfileModel, db: Session) -> List[ORMJobPosting]:
    recommendations = []
    try:
        job_postings = db.query(ORMJobPosting).all()

        for job in job_postings:
            if (
                    user_profile.experience_level == job.experience_level
                    and any(skill in user_profile.skills for skill in job.required_skills)  # No split needed
                    and user_profile.preferences.locations and job.location in user_profile.preferences.locations
                    and user_profile.preferences.job_type == job.job_type
            ):
                recommendations.append(job)

    except Exception as e:
        logger.error("Error occurred while matching jobs: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to match jobs.")

    return recommendations


# API endpoint to accept user profile data and return job recommendations
@app.post("/recommendations", response_model=List[JobPosting])
def recommend_jobs(user_profile: UserProfileModel, db: Session = Depends(get_db)):
    try:
        recommendations = match_jobs(user_profile, db)

        # Uncomment and implement if you want to save user profiles in the database
        # user_profile_data = UserProfile(
        #     name=user_profile.name,
        #     skills=",".join(user_profile.skills),
        #     experience_level=user_profile.experience_level,
        #     preferences=user_profile.preferences.json(),
        # )
        # db.add(user_profile_data)
        # db.commit()

        if not recommendations:
            logger.warning("No job recommendations found for user: %s", user_profile.name)
            raise HTTPException(status_code=404, detail="No job recommendations found")

        logger.info("Successfully found %d job recommendations for user: %s", len(recommendations), user_profile.name)
        return recommendations

    except HTTPException as http_exc:
        logger.error("HTTP Exception: %s", http_exc.detail)
        raise
    except Exception as e:
        logger.error("Error occurred while recommending jobs: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to provide job recommendations.")


# Main entry point for running the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
