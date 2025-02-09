"""rename stock_list table to stocks

Revision ID: f71aee9282b2
Revises: 61d64d7c076d
Create Date: 2025-01-29 16:15:45.540752

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "f71aee9282b2"
down_revision: Union[str, None] = "61d64d7c076d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table("stock_list", "stocks")
    op.drop_constraint(
        "stock_share_distribution_stock_symbol_fkey",
        "stock_share_distribution",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "stock_share_distribution", "stocks", ["stock_symbol"], ["stock_symbol"]
    )


def downgrade():
    op.rename_table("stocks", "stock_list")
    op.drop_constraint(None, "stock_share_distribution", type_="foreignkey")
    op.create_foreign_key(
        "stock_share_distribution_stock_symbol_fkey",
        "stock_share_distribution",
        "stock_list",
        ["stock_symbol"],
        ["stock_symbol"],
    )
