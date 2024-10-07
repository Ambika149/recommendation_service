from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from sqlalchemy.orm import sessionmaker

# Create the base class for declarative models
Base = declarative_base()


# Model for JobPostings
class JobPosting(Base):
    __tablename__ = 'job_postings'

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    required_skills = Column(JSON, nullable=False)  # List of skills stored as JSON
    location = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)

    def __repr__(self):
        return f"<JobPosting(job_title='{self.job_title}', company='{self.company}')>"


# Model for UserProfile
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    skills = Column(JSON, nullable=False)  # List of skills stored as JSON
    experience_level = Column(String, nullable=False)

    # Relationship to job postings, if needed
    # You could use backref to create a bidirectional relationship
    job_posting_id = Column(Integer, ForeignKey('job_postings.job_id'), nullable=True)
    job_posting = relationship('JobPosting', backref='profiles')

    def __repr__(self):
        return f"<UserProfile(name='{self.name}', experience_level='{self.experience_level}')>"


# Database connection setup (replace with your actual database URL)
DATABASE_URL = "postgresql://admin:1234@localhost/tech_jobs_db"
engine = create_engine(DATABASE_URL)

# Create all tables in the database (this should be run once)
Base.metadata.create_all(engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
