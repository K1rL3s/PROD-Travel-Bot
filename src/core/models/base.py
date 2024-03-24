from pydantic import BaseModel, ConfigDict


class BaseCoreModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
    )
