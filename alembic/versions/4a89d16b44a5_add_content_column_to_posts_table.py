"""add content column to posts table

Revision ID: 4a89d16b44a5
Revises: fcee4b846e08
Create Date: 2025-06-03 17:45:28.709827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a89d16b44a5'
down_revision: Union[str, None] = 'fcee4b846e08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
