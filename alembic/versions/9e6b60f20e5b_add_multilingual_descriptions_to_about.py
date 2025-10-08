"""add multilingual descriptions to about

Revision ID: 9e6b60f20e5b
Revises: 579d62c71f88
Create Date: 2025-10-03 21:39:21.415237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e6b60f20e5b'
down_revision: Union[str, Sequence[str], None] = '579d62c71f88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("about", "description_uz",
        existing_type=sa.String(),
        nullable=False,
        server_default=""
    )
    op.alter_column("about", "description_ru",
        existing_type=sa.String(),
        nullable=False,
        server_default=""
    )
    op.alter_column("about", "description_en",
        existing_type=sa.String(),
        nullable=False,
        server_default=""
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("about", sa.Column("description", sa.String(), nullable=True))
    op.drop_column("about", "description_uz")
    op.drop_column("about", "description_ru")
    op.drop_column("about", "description_en")
