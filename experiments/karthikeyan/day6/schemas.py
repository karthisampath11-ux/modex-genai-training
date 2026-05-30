"""Pydantic v2 schema definitions for example Event, Recipe, and ComplianceCheck models.

This module defines three data models:
- Event: a small event record with title, date, location, and summary_line.
- Recipe: a medium complexity recipe model with ingredients and preparation steps.
- ComplianceCheck: a more complex verdict model with status, evidence, confidence, and optional notes.

Run this file directly to instantiate sample objects and verify validation.
"""

from __future__ import annotations

from datetime import date
from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class Event(BaseModel):
    title: str = Field(..., description="Title of the event")
    date: str = Field(..., description="Event date in ISO format YYYY-MM-DD")
    location: str = Field(..., description="Event location")
    summary_line: str = Field(..., description="One-sentence summary of the event")

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("date must be in ISO format YYYY-MM-DD") from exc
        return value


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient")
    quantity: float = Field(..., description="Quantity of the ingredient")
    unit: str = Field(..., description="Measurement unit, e.g. g, ml, cups, pieces")


class Recipe(BaseModel):
    title: str = Field(..., description="Recipe title")
    servings: int = Field(..., description="Number of servings")
    ingredients: List[Ingredient] = Field(..., description="List of ingredient entries")
    steps: List[str] = Field(..., description="Ordered preparation steps")
    prep_minutes: int = Field(..., description="Preparation time in minutes")


class ComplianceCheck(BaseModel):
    rule_id: str = Field(..., description="Identifier for the compliance rule")
    status: Literal["compliant", "non_compliant", "insufficient_evidence"] = Field(
        ..., description="Verdict status for the check"
    )
    evidence_quotes: List[str] = Field(..., description="Supporting evidence quotes")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0"
    )
    notes: str = Field("", description="Optional notes or comments")


if __name__ == "__main__":
    sample_events = [
        Event(
            title="Open House Launch",
            date="2026-06-15",
            location="Central Library",
            summary_line="A community open house introducing the new downtown arts program.",
        ),
        Event(
            title="Quarterly Planning Meeting",
            date="2026-07-01",
            location="Conference Room B",
            summary_line="Team members review goals and align on the next quarter's priorities.",
        ),
    ]

    sample_recipes = [
        Recipe(
            title="Classic Pancakes",
            servings=4,
            ingredients=[
                Ingredient(name="Flour", quantity=240.0, unit="g"),
                Ingredient(name="Milk", quantity=360.0, unit="ml"),
                Ingredient(name="Eggs", quantity=2.0, unit="pieces"),
            ],
            steps=[
                "Whisk dry ingredients together.",
                "Add milk and eggs, then stir until smooth.",
                "Cook on a greased skillet until golden brown on both sides.",
            ],
            prep_minutes=20,
        ),
        Recipe(
            title="Simple Garden Salad",
            servings=2,
            ingredients=[
                Ingredient(name="Lettuce", quantity=150.0, unit="g"),
                Ingredient(name="Tomato", quantity=1.0, unit="pieces"),
                Ingredient(name="Olive Oil", quantity=15.0, unit="ml"),
            ],
            steps=[
                "Chop the vegetables.",
                "Combine in a bowl and drizzle with olive oil.",
                "Toss gently and serve immediately.",
            ],
            prep_minutes=10,
        ),
    ]

    sample_checks = [
        ComplianceCheck(
            rule_id="NBC-FIRE-001",
            status="compliant",
            evidence_quotes=[
                "All fire extinguishers are inspected monthly.",
                "Emergency exits are clearly marked and unobstructed.",
            ],
            confidence=0.92,
            notes="Routine inspection completed successfully.",
        ),
        ComplianceCheck(
            rule_id="NBC-FIRE-002",
            status="insufficient_evidence",
            evidence_quotes=[
                "No documentation was available for sprinkler maintenance.",
            ],
            confidence=0.55,
        ),
    ]

    print("Sample Event instances:")
    for event in sample_events:
        print(event.model_dump())

    print("\nSample Recipe instances:")
    for recipe in sample_recipes:
        print(recipe.model_dump())

    print("\nSample ComplianceCheck instances:")
    for check in sample_checks:
        print(check.model_dump())
