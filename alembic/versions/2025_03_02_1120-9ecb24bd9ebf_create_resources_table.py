"""Create resources table

Revision ID: 9ecb24bd9ebf
Revises: 3354f8920788
Create Date: 2025-03-02 11:20:04.907228

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # added


# revision identifiers, used by Alembic.
revision: str = "9ecb24bd9ebf"
down_revision: Union[str, None] = "3354f8920788"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "item",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("power", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "MATERIAL",
                "MELEE_WEAPON",
                "RANGED_WEAPON",
                "ARMOR",
                "CLOTHING",
                "POTION",
                "SCROLL",
                "MAGIC_ITEM",
                "JEWELRY",
                "TOOL",
                "INSTRUMENT",
                "MISC",
                name="itemtype",
            ),
            nullable=False,
        ),
        sa.Column(
            "quality",
            sa.Enum(
                "COMMON",
                "UNCOMMON",
                "RARE",
                "EPIC",
                "MAGNIFICENT",
                "LEGENDARY",
                "ARTEFACT",
                name="itemquality",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_item_id"), "item", ["id"], unique=False)
    op.create_table(
        "resource",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "item_type",
            sa.Enum(
                "MATERIAL",
                "MELEE_WEAPON",
                "RANGED_WEAPON",
                "ARMOR",
                "CLOTHING",
                "POTION",
                "SCROLL",
                "MAGIC_ITEM",
                "JEWELRY",
                "TOOL",
                "INSTRUMENT",
                "MISC",
                name="itemtype",
            ),
            nullable=False,
        ),
        sa.Column("recipe", sa.JSON(), nullable=True),
        sa.Column("base_price", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_resource_id"), "resource", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_resource_id"), table_name="resource")
    op.drop_table("resource")
    op.drop_index(op.f("ix_item_id"), table_name="item")
    op.drop_table("item")
    # ### end Alembic commands ###
