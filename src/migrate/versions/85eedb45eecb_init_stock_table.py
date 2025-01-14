"""init stock table

Revision ID: 85eedb45eecb
Revises: 
Create Date: 2025-01-14 20:38:03.620222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85eedb45eecb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stock_list",
        sa.Column("stock_symbol",sa.String(length=4),),
        sa.Column("stock_name",sa.UnicodeText(),),
        sa.Column("last_updated_at",sa.TIMESTAMP())
    )

def downgrade() -> None:
    op.drop_table("stock_list")

