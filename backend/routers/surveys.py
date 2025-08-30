from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/surveys", tags=["surveys"])

@router.get("/", response_model=schemas.SurveyListResponse)
def read_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    surveys, total = crud.get_surveys(db, skip=skip, limit=limit, search=search)
    return {
        "surveys": surveys,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{survey_id}", response_model=schemas.Survey)
def read_survey(survey_id: int, db: Session = Depends(get_db)):
    db_survey = crud.get_survey(db, survey_id=survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@router.post("/", response_model=schemas.Survey)
def create_survey(survey: schemas.SurveyCreate, db: Session = Depends(get_db)):
    return crud.create_survey(db=db, survey=survey)

@router.put("/{survey_id}", response_model=schemas.Survey)
def update_survey(
    survey_id: int,
    survey: schemas.SurveyUpdate,
    db: Session = Depends(get_db)
):
    db_survey = crud.update_survey(db, survey_id=survey_id, survey=survey)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@router.delete("/{survey_id}")
def delete_survey(survey_id: int, db: Session = Depends(get_db)):
    db_survey = crud.delete_survey(db, survey_id=survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}

# Survey Notes endpoints
@router.get("/{survey_id}/notes", response_model=List[schemas.SurveyNote])
def read_survey_notes(survey_id: int, db: Session = Depends(get_db)):
    return crud.get_survey_notes(db, survey_id=survey_id)

@router.post("/{survey_id}/notes", response_model=schemas.SurveyNote)
def create_survey_note(
    survey_id: int,
    note: schemas.SurveyNoteCreate,
    db: Session = Depends(get_db)
):
    note.SurveyId = survey_id
    return crud.create_survey_note(db=db, note=note)

@router.delete("/notes/{note_id}")
def delete_survey_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.delete_survey_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

# Survey Documents endpoints
@router.get("/{survey_id}/documents", response_model=List[schemas.SurveyDocument])
def read_survey_documents(survey_id: int, db: Session = Depends(get_db)):
    return crud.get_survey_documents(db, survey_id=survey_id)

@router.post("/{survey_id}/documents", response_model=schemas.SurveyDocument)
def create_survey_document(
    survey_id: int,
    document: schemas.SurveyDocumentCreate,
    db: Session = Depends(get_db)
):
    document.SurveyId = survey_id
    return crud.create_survey_document(db=db, document=document)

@router.delete("/documents/{document_id}")
def delete_survey_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.delete_survey_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}
