"""init

Revision ID: 0001
Revises:
Create Date: 2024-03-24 20:09:42.006805

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("alpha2", sa.String(length=2), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_countries")),
        sa.UniqueConstraint("alpha2", name=op.f("uq_countries_alpha2")),
        sa.UniqueConstraint("id", name=op.f("uq_countries_id")),
        sa.UniqueConstraint("title", name=op.f("uq_countries_title")),
    )
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("timezone", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
            name=op.f("fk_cities_country_id_countries"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cities")),
        sa.UniqueConstraint("id", name=op.f("uq_cities_id")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("tg_username", sa.String(length=32), nullable=True),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(
            ["city_id"], ["cities.id"], name=op.f("fk_users_city_id_cities")
        ),
        sa.ForeignKeyConstraint(
            ["country_id"], ["countries.id"], name=op.f("fk_users_country_id_countries")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("id", name=op.f("uq_users_id")),
    )
    op.create_table(
        "travels",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("owner_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name=op.f("fk_travels_owner_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_travels")),
        sa.UniqueConstraint("id", name=op.f("uq_travels_id")),
    )
    op.create_table(
        "invite_links",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("travel_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["travel_id"],
            ["travels.id"],
            name=op.f("fk_invite_links_travel_id_travels"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invite_links")),
        sa.UniqueConstraint("id", name=op.f("uq_invite_links_id")),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("travel_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=1024), nullable=False),
        sa.Column("address", sa.String(length=512), nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["city_id"], ["cities.id"], name=op.f("fk_locations_city_id_cities")
        ),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
            name=op.f("fk_locations_country_id_countries"),
        ),
        sa.ForeignKeyConstraint(
            ["travel_id"], ["travels.id"], name=op.f("fk_locations_travel_id_travels")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_locations")),
        sa.UniqueConstraint("id", name=op.f("uq_locations_id")),
    )
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("travel_id", sa.Integer(), nullable=False),
        sa.Column("creator_id", sa.BigInteger(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["creator_id"], ["users.id"], name=op.f("fk_notes_creator_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["travel_id"], ["travels.id"], name=op.f("fk_notes_travel_id_travels")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notes")),
        sa.UniqueConstraint("id", name=op.f("uq_notes_id")),
    )
    op.create_table(
        "users_to_travels",
        sa.Column("member_id", sa.BigInteger(), nullable=False),
        sa.Column("travel_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["users.id"],
            name=op.f("fk_users_to_travels_member_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["travel_id"],
            ["travels.id"],
            name=op.f("fk_users_to_travels_travel_id_travels"),
        ),
        sa.PrimaryKeyConstraint(
            "member_id", "travel_id", name=op.f("pk_users_to_travels")
        ),
    )

    op.create_unique_constraint(op.f("uq_cities_id"), "cities", ["id"])
    op.create_unique_constraint(op.f("uq_countries_id"), "countries", ["id"])
    op.create_unique_constraint(op.f("uq_invite_links_id"), "invite_links", ["id"])
    op.create_unique_constraint(op.f("uq_locations_id"), "locations", ["id"])
    op.create_unique_constraint(op.f("uq_notes_id"), "notes", ["id"])
    op.create_unique_constraint(op.f("uq_travels_id"), "travels", ["id"])
    op.create_unique_constraint(op.f("uq_users_id"), "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_to_travels")
    op.drop_table("notes")
    op.drop_table("locations")
    op.drop_table("invite_links")
    op.drop_table("travels")
    op.drop_table("users")
    op.drop_table("cities")
    op.drop_table("countries")
    # ### end Alembic commands ###