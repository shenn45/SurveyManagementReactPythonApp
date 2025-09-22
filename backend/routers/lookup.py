from fastapi import APIRouter
from typing import List
import crud
import schemas

router = APIRouter(prefix="/lookup", tags=["lookup"])

@router.get("/survey-types", response_model=List[schemas.SurveyType])
def read_survey_types():
    return crud.get_survey_types()

@router.get("/survey-statuses", response_model=List[schemas.SurveyStatus])
def read_survey_statuses():
    return crud.get_survey_statuses()

@router.get("/townships", response_model=List[schemas.Township])
def read_townships():
    return crud.get_townships()

@router.post("/survey-types", response_model=schemas.SurveyType)
def create_survey_type(survey_type: schemas.SurveyTypeCreate):
    return crud.create_survey_type(survey_type=survey_type)

@router.post("/survey-statuses", response_model=schemas.SurveyStatus)
def create_survey_status(survey_status: schemas.SurveyStatusCreate):
    return crud.create_survey_status(survey_status=survey_status)

@router.post("/townships", response_model=schemas.Township)
def create_township(township: schemas.TownshipCreate):
    return crud.create_township(township=township)
