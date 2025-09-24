from fastapi import APIRouter, HTTPException, status
from typing import List
import crud
import schemas

router = APIRouter()

# Default user ID for now (since we don't have user authentication)
DEFAULT_USER_ID = "default_user"

@router.get("/user-settings/{settings_type}", response_model=schemas.UserSettings)
async def get_user_settings(settings_type: str):
    """Get user settings by type"""
    settings = crud.get_user_settings(DEFAULT_USER_ID, settings_type)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Settings not found for type: {settings_type}"
        )
    return settings


@router.get("/user-settings", response_model=List[schemas.UserSettings])
async def get_all_user_settings():
    """Get all user settings"""
    return crud.get_all_user_settings(DEFAULT_USER_ID)


@router.post("/user-settings", response_model=schemas.UserSettings)
async def create_user_settings(settings_data: schemas.UserSettingsCreate):
    """Create new user settings"""
    # Override the UserId to use default user
    settings_data.UserId = DEFAULT_USER_ID
    
    settings = crud.create_user_settings(settings_data)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user settings"
        )
    return settings


@router.put("/user-settings/{settings_type}", response_model=schemas.UserSettings)
async def update_user_settings(settings_type: str, settings_data: schemas.UserSettingsUpdate):
    """Update user settings by type"""
    # First get the existing settings
    existing_settings = crud.get_user_settings(DEFAULT_USER_ID, settings_type)
    if not existing_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Settings not found for type: {settings_type}"
        )
    
    updated_settings = crud.update_user_settings(existing_settings.UserSettingsId, settings_data)
    if not updated_settings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user settings"
        )
    return updated_settings


@router.put("/user-settings/{settings_type}/upsert", response_model=schemas.UserSettings)
async def upsert_user_settings(settings_type: str, settings_data: dict):
    """Create or update user settings"""
    settings = crud.upsert_user_settings(DEFAULT_USER_ID, settings_type, settings_data)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to save user settings"
        )
    return settings


@router.delete("/user-settings/{settings_type}")
async def delete_user_settings(settings_type: str):
    """Delete user settings by type"""
    # First get the existing settings
    existing_settings = crud.get_user_settings(DEFAULT_USER_ID, settings_type)
    if not existing_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Settings not found for type: {settings_type}"
        )
    
    success = crud.delete_user_settings(existing_settings.UserSettingsId)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user settings"
        )
    return {"message": "Settings deleted successfully"}