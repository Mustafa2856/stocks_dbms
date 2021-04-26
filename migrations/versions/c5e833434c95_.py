"""empty message

Revision ID: c5e833434c95
Revises: 
Create Date: 2021-04-26 20:07:18.022065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5e833434c95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('mobile', sa.String(length=14), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('pan_no', sa.String(length=10), nullable=True),
    sa.Column('aadhar_no', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('aadhar_no'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('pan_no')
    )
    op.create_table('company',
    sa.Column('id', sa.String(length=150), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('sector', sa.String(length=100), nullable=True),
    sa.Column('year_low', sa.Numeric(), nullable=True),
    sa.Column('year_high', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Bank_Details',
    sa.Column('account_no', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('User_id', sa.String(length=120), nullable=True),
    sa.Column('bank_name', sa.String(length=120), nullable=True),
    sa.Column('bank_branch', sa.String(length=120), nullable=True),
    sa.Column('bank_IFSC', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['User_id'], ['User.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('account_no')
    )
    op.create_table('demat',
    sa.Column('account_no', sa.BigInteger(), nullable=False),
    sa.Column('User_id', sa.String(length=120), nullable=True),
    sa.Column('Funds_Avail', sa.Numeric(), nullable=True),
    sa.Column('Funds_Blocked', sa.Numeric(), nullable=True),
    sa.Column('Funds_Invested', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['User_id'], ['User.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('account_no')
    )
    op.create_table('shares',
    sa.Column('share_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.String(length=150), nullable=True),
    sa.Column('prev_close', sa.Numeric(), nullable=True),
    sa.Column('open_price', sa.Numeric(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('day_low', sa.Numeric(), nullable=True),
    sa.Column('day_high', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('share_id')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.String(length=150), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('bid_price', sa.Numeric(), nullable=True),
    sa.Column('demat_ac', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['demat_ac'], ['demat.account_no'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('company_id', sa.String(length=150), nullable=True),
    sa.Column('demat_ac', sa.BigInteger(), nullable=True),
    sa.Column('buy', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['demat_ac'], ['demat.account_no'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('portfolio')
    op.drop_table('shares')
    op.drop_table('demat')
    op.drop_table('Bank_Details')
    op.drop_table('company')
    op.drop_table('User')
    # ### end Alembic commands ###
