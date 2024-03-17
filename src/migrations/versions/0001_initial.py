"""initial

Revision ID: 0001
Revises: 
Create Date: 2024-03-16 22:28:41.933910

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
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("country", sa.String(length=128), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=True)
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
        sa.UniqueConstraint("title", name=op.f("uq_travels_title")),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("travel_id", sa.Integer(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=1024), nullable=False),
        sa.Column("country", sa.String(length=256), nullable=False),
        sa.Column("city", sa.String(length=256), nullable=False),
        sa.Column("address", sa.String(length=256), nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=True),
        sa.Column("end_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["travel_id"], ["travels.id"], name=op.f("fk_locations_travel_id_travels")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_locations")),
        sa.UniqueConstraint("id", name=op.f("uq_locations_id")),
    )
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("owner_id", sa.BigInteger(), nullable=False),
        sa.Column("travel_id", sa.Integer(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("file_id", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name=op.f("fk_notes_owner_id_users")
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

    op.create_unique_constraint(op.f("uq_locations_id"), "locations", ["id"])
    op.create_unique_constraint(op.f("uq_notes_id"), "notes", ["id"])
    op.create_unique_constraint(op.f("uq_travels_id"), "travels", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_to_travels")
    op.drop_table("notes")
    op.drop_table("locations")
    op.drop_table("travels")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
