#!/usr/bin/env python3
"""
Test script to create sample township data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import crud
from schemas import TownshipCreate

def create_sample_townships():
    """Create sample township data for testing"""
    sample_townships = [
        TownshipCreate(
            TownshipName="Spring Township",
            County="Montgomery",
            State="PA",
            IsActive=True
        ),
        TownshipCreate(
            TownshipName="Upper Merion Township",
            County="Montgomery", 
            State="PA",
            IsActive=True
        ),
        TownshipCreate(
            TownshipName="Lower Providence Township",
            County="Montgomery",
            State="PA", 
            IsActive=True
        ),
        TownshipCreate(
            TownshipName="Whitpain Township",
            County="Montgomery",
            State="PA",
            IsActive=True
        ),
        TownshipCreate(
            TownshipName="Horsham Township",
            County="Montgomery",
            State="PA",
            IsActive=True
        )
    ]
    
    print("Creating sample townships...")
    for township_data in sample_townships:
        try:
            township = crud.create_township(township=township_data)
            if township:
                print(f"✓ Created: {township.TownshipName}, {township.County} County, {township.State}")
            else:
                print(f"✗ Failed to create: {township_data.TownshipName}")
        except Exception as e:
            print(f"✗ Error creating {township_data.TownshipName}: {e}")
    
    print("\nTesting township retrieval...")
    try:
        townships, total = crud.get_townships()
        print(f"✓ Retrieved {total} townships:")
        for township in townships:
            print(f"  - {township.TownshipName}, {township.County} County, {township.State}")
    except Exception as e:
        print(f"✗ Error retrieving townships: {e}")

if __name__ == "__main__":
    create_sample_townships()