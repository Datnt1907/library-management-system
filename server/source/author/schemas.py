from pydantic import Field

from source.kit.schemas import IDSchema, Schema, TimestampedSchema


class AuthorCreate(Schema):
    name: str = Field(description="Name of author")
    email: str = Field(description="Email of author")
    biography: str | None = Field(default=None, description="Biography of author")


class AuthorUpdate(Schema):
    name: str | None = Field(default=None, description="Name of author")
    email: str | None = Field(default=None, description="Email of author")
    biography: str | None = Field(default=None, description="Biography of author")


class Author(IDSchema, TimestampedSchema):
    name: str = Field(description="Name of author")
    email: str = Field(description="Email of author")
    biography: str | None = Field(default=None, description="Biography of author")
