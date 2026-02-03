"""increase transaction.amount precision

Revision ID: dd21522ec958
Revises: 4fe02299585f
Create Date: 2026-02-03 14:18:35.294945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd21522ec958'
down_revision: Union[str, Sequence[str], None] = '4fe02299585f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        'ALTER TABLE "transaction" ALTER COLUMN amount TYPE NUMERIC(60,18);'
    )


def downgrade() -> None:
    op.execute(
        'ALTER TABLE "transaction" ALTER COLUMN amount TYPE NUMERIC(38,18);'
    )
