"""empty message

Revision ID: 0e433803543f
Revises: 14e89fa9f0bc
Create Date: 2024-12-12 11:53:09.413058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e433803543f'
down_revision: Union[str, None] = '14e89fa9f0bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('category_id', sa.Integer(), nullable=False))
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('fk_tasks_category_categorys', 'tasks', type_='foreignkey')
    op.create_foreign_key(op.f('fk_tasks_category_id_categorys'), 'tasks', 'categorys', ['category_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(op.f('fk_tasks_user_id_users'), 'tasks', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('tasks', 'category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk_tasks_user_id_users'), 'tasks', type_='foreignkey')
    op.drop_constraint(op.f('fk_tasks_category_id_categorys'), 'tasks', type_='foreignkey')
    op.create_foreign_key('fk_tasks_category_categorys', 'tasks', 'categorys', ['category'], ['id'], ondelete='CASCADE')
    op.drop_column('tasks', 'user_id')
    op.drop_column('tasks', 'category_id')
    # ### end Alembic commands ###