from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/lookup", tags=["lookup"])

@router.get("/survey-types", response_model=List[schemas.SurveyType])
def read_survey_types(db: Session = Depends(get_db)):
    return crud.get_survey_types(db)

@router.get("/survey-statuses", response_model=List[schemas.SurveyStatus])
def read_survey_statuses(db: Session = Depends(get_db)):
    return crud.get_survey_statuses(db)

@router.get("/townships", response_model=List[schemas.Township])
def read_townships(db: Session = Depends(get_db)):
    return crud.get_townships(db)

@router.post("/survey-types", response_model=schemas.SurveyType)
def create_survey_type(survey_type: schemas.SurveyTypeCreate, db: Session = Depends(get_db)):
    return crud.create_survey_type(db=db, survey_type=survey_type)

@router.post("/survey-statuses", response_model=schemas.SurveyStatus)
def create_survey_status(survey_status: schemas.SurveyStatusCreate, db: Session = Depends(get_db)):
    return crud.create_survey_status(db=db, survey_status=survey_status)

@router.post("/townships", response_model=schemas.Township)
def create_township(township: schemas.TownshipCreate, db: Session = Depends(get_db)):
    return crud.create_township(db=db, township=township)
