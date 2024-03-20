"""invite_links

Revision ID: 0004
Revises: 0003
Create Date: 2024-03-19 21:45:40.721281

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.create_unique_constraint(op.f("uq_invite_links_id"), "invite_links", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("invite_links")
    # ### end Alembic commands ###