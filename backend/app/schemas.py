from pydantic import BaseModel, Field


class CarAnalysis(BaseModel):
    make: str = Field(..., description="Vehicle manufacturer, e.g. Toyota")
    model: str = Field(..., description="Vehicle model, e.g. Corolla")
    production_date: str = Field(
        ..., description="Best estimated production year/date in ISO format or 'unknown'"
    )
    country_of_origin: str = Field(..., description="Country where make originates")
    confidence: float = Field(..., ge=0.0, le=1.0)
    notes: str = Field(..., description="Short explanation of assumptions or uncertainty")
