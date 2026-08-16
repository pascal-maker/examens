from pydantic import BaseModel


class MetricPoint(BaseModel):
    label: str
    value: float


class TimeSeriesPoint(BaseModel):
    date: str
    count: int
