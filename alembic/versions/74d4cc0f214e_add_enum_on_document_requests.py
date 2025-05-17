"""add enum on document requests

Revision ID: 74d4cc0f214e
Revises: 69fef1ac51e6
Create Date: 2025-05-17 11:59:41.499277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74d4cc0f214e'
down_revision: Union[str, None] = '69fef1ac51e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "document_requests",
        "status",
        type_=sa.Enum(
            "pending", "uploaded", "accepted", "rejected", "overdue",
            name="requeststatus"
        ),
        existing_type=sa.Enum(
            "pending", "uploaded", "overdue",
            name="requeststatus"
        ),
        nullable=False,
        existing_nullable=False,
        existing_server_default=sa.text("'pending'")
    )


def downgrade() -> None:
    op.alter_column(
        "document_requests",
        "status",
        type_=sa.Enum(
            "pending", "uploaded", "overdue",
            name="requeststatus"
        ),
        existing_type=sa.Enum(
            "pending", "uploaded", "accepted", "rejected", "overdue",
            name="requeststatus"
        ),
        nullable=False,
        existing_nullable=False,
        existing_server_default=sa.text("'pending'")
    )
