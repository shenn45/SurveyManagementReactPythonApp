from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import crud
import schemas

router = APIRouter(prefix="/surveys", tags=["surveys"])

@router.get("/", response_model=schemas.SurveyListResponse)
def read_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None)
):
    surveys, total = crud.get_surveys(skip=skip, limit=limit, search=search)
    return {
        "surveys": surveys,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{survey_id}", response_model=schemas.Survey)
def read_survey(survey_id: str):
    db_survey = crud.get_survey(survey_id=survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@router.post("/", response_model=schemas.Survey)
def create_survey(survey: schemas.SurveyCreate):
    return crud.create_survey(survey=survey)

@router.put("/{survey_id}", response_model=schemas.Survey)
def update_survey(
    survey_id: str,
    survey: schemas.SurveyUpdate
):
    db_survey = crud.update_survey(survey_id=survey_id, survey=survey)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@router.delete("/{survey_id}")
def delete_survey(survey_id: str):
    db_survey = crud.delete_survey(survey_id=survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}

# Survey Notes endpoints
@router.get("/{survey_id}/notes", response_model=List[schemas.SurveyNote])
def read_survey_notes(survey_id: str):
    return crud.get_survey_notes(survey_id=survey_id)

@router.post("/{survey_id}/notes", response_model=schemas.SurveyNote)
def create_survey_note(
    survey_id: str,
    note: schemas.SurveyNoteCreate
):
    note.SurveyId = survey_id
    return crud.create_survey_note(note=note)

@router.delete("/notes/{note_id}")
def delete_survey_note(note_id: str):
    db_note = crud.delete_survey_note(note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

# Survey Documents endpoints
@router.get("/{survey_id}/documents", response_model=List[schemas.SurveyDocument])
def read_survey_documents(survey_id: str):
    return crud.get_survey_documents(survey_id=survey_id)

@router.post("/{survey_id}/documents", response_model=schemas.SurveyDocument)
def create_survey_document(
    survey_id: str,
    document: schemas.SurveyDocumentCreate
):
    document.SurveyId = survey_id
    return crud.create_survey_document(document=document)

@router.delete("/documents/{document_id}")
def delete_survey_document(document_id: str):
    db_document = crud.delete_survey_document(document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}
