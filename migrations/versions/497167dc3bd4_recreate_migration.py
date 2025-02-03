from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '497167dc3bd4'
down_revision = '75c0464d0d40'
branch_labels = None
depends_on = None


def upgrade():
    # Alter the 'phone' column to change its type to Integer
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.Integer(),
               existing_nullable=False)


def downgrade():
    # Revert the 'phone' column back to VARCHAR type
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
