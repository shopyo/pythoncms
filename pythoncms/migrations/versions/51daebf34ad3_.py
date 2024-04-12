"""empty message

Revision ID: 51daebf34ad3
Revises: 
Create Date: 2023-07-03 18:41:32.090382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51daebf34ad3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('message', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('i18n_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('strid', sa.String(length=1024), nullable=True),
    sa.Column('lang', sa.String(length=10), nullable=True),
    sa.Column('string', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('setting', sa.String(length=100), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('setting')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('_password', sa.String(length=128), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('date_registered', sa.DateTime(), nullable=False),
    sa.Column('is_email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('email_confirm_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('role_user_bridge',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role_user_bridge')
    op.drop_table('users')
    op.drop_table('settings')
    op.drop_table('roles')
    op.drop_table('pages')
    op.drop_table('i18n_records')
    op.drop_table('contact')
    # ### end Alembic commands ###