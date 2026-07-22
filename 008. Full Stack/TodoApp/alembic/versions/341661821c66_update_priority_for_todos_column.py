"""Update priority for todos column

Revision ID: 341661821c66
Revises: 949fcbcc4014
Create Date: 2026-07-21 13:10:39.919742
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "341661821c66"
down_revision: Union[str, Sequence[str], None] = "949fcbcc4014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "todos",
        "priority",
        existing_type=sa.String(length=20),
        type_=sa.Integer(),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "todos",
        "priority",
        existing_type=sa.Integer(),
        type_=sa.String(length=20),
        existing_nullable=True,
    )