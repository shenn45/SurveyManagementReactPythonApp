from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional

import crud
import schemas
from models import BoardConfiguration

router = APIRouter(
    prefix="/board-configurations",
    tags=["board-configurations"]
)


@router.post("/", response_model=BoardConfiguration)
def create_board_configuration(board_config: schemas.BoardConfigurationCreate):
    """Create a new board configuration"""
    try:
        db_config = crud.create_board_configuration(board_config)
        if not db_config:
            raise HTTPException(status_code=400, detail="Failed to create board configuration")
        return db_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[BoardConfiguration])
def get_board_configurations():
    """Get all active board configurations"""
    try:
        return crud.get_board_configurations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/default", response_model=BoardConfiguration)
def get_default_board_configuration():
    """Get the default board configuration"""
    try:
        config = crud.get_default_board_configuration()
        if not config:
            raise HTTPException(status_code=404, detail="No default board configuration found")
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/by-slug/{board_slug}", response_model=BoardConfiguration)
def get_board_configuration_by_slug(board_slug: str = Path(..., description="Board URL slug")):
    """Get a board configuration by its URL slug"""
    try:
        config = crud.get_board_configuration_by_slug(board_slug)
        if not config:
            raise HTTPException(status_code=404, detail="Board configuration not found")
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{board_config_id}", response_model=BoardConfiguration)
def get_board_configuration(board_config_id: str = Path(..., description="Board configuration ID")):
    """Get a board configuration by ID"""
    try:
        config = crud.get_board_configuration(board_config_id)
        if not config:
            raise HTTPException(status_code=404, detail="Board configuration not found")
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{board_config_id}", response_model=BoardConfiguration)
def update_board_configuration(
    board_config_id: str, 
    board_config: schemas.BoardConfigurationUpdate
):
    """Update a board configuration"""
    try:
        # First check if the board configuration exists
        existing = crud.get_board_configuration(board_config_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Board configuration not found")
        
        updated_config = crud.update_board_configuration(board_config_id, board_config)
        if not updated_config:
            raise HTTPException(status_code=400, detail="Failed to update board configuration")
        return updated_config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{board_config_id}")
def delete_board_configuration(board_config_id: str = Path(..., description="Board configuration ID")):
    """Soft delete a board configuration (set IsActive to False)"""
    try:
        # First check if the board configuration exists
        existing = crud.get_board_configuration(board_config_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Board configuration not found")
        
        success = crud.delete_board_configuration(board_config_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to delete board configuration")
        
        return {"message": "Board configuration deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")