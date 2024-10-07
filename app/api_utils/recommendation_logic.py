from app.data_model.user_profile_model import UserProfileModel
from app.db_model.orm_model import JobPosting as ORMJobPosting
from sqlalchemy.orm import Session
from typing import List
import logging
from fastapi import FastAPI, HTTPException, Depends


# Recommendation logic
def match_jobs(user_profile: UserProfileModel, db: Session) -> List[ORMJobPosting]:
    recommendations = []
    try:
        logging.info("running recommendation logic......")
        job_postings = db.query(ORMJobPosting).all()
        for job in job_postings:
            if (
                    user_profile.experience_level == job.experience_level
                    and any(skill in user_profile.skills for skill in job.required_skills)
                    and user_profile.preferences.locations and job.location in user_profile.preferences.locations
                    and user_profile.preferences.job_type == job.job_type
            ):
                recommendations.append(job)

    except Exception as e:
        logging.error("Error occurred while matching jobs: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to match jobs.")

    return recommendations
