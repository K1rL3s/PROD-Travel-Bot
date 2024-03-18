"""message

Revision ID: 0002
Revises: 0001
Create Date: 2024-03-18 18:11:45.703529

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("locations", "order")
    op.alter_column(
        "users",
        "description",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "description",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    op.add_column(
        "locations",
        sa.Column("order", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###