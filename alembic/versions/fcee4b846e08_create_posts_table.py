"""create posts table

Revision ID: fcee4b846e08
Revises: 
Create Date: 2025-06-03 17:29:23.449424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcee4b846e08'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
