"""add description to product

Revision ID: 37961ae1533a
Revises: 
Create Date: 2025-07-06 06:32:51.146944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37961ae1533a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "product",
        sa.Column("description", sa.String(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'description')
    # ### end Alembic commands ###
