"""add user table

Revision ID: 0fed36eb808a
Revises: 4a89d16b44a5
Create Date: 2025-06-03 17:56:42.913100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fed36eb808a'
down_revision: Union[str, None] = '4a89d16b44a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"), 
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
