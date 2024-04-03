"""empty message

Revision ID: 103d4c9de94e
Revises: 
Create Date: 2024-03-21 10:37:33.765981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '103d4c9de94e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coordenacoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sigla', sa.String(length=10), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diretorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sigla', sa.String(length=10), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('divisoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sigla', sa.String(length=10), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gerencias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sigla', sa.String(length=10), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=False),
    sa.Column('matricula', sa.Integer(), nullable=False),
    sa.Column('cargo', sa.String(length=50), nullable=False),
    sa.Column('contrato', sa.String(length=50), nullable=False),
    sa.Column('apps_permissoes', sa.JSON(), nullable=False),
    sa.Column('criado', sa.DateTime(), nullable=False),
    sa.Column('ultima_mod', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('ligacao', sa.String(length=100), nullable=True),
    sa.Column('id_diretoria_asc', sa.Integer(), nullable=True),
    sa.Column('id_coord_asc', sa.Integer(), nullable=True),
    sa.Column('id_gerencia_asc', sa.Integer(), nullable=True),
    sa.Column('id_divisao_asc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_coord_asc'], ['coordenacoes.id'], ),
    sa.ForeignKeyConstraint(['id_diretoria_asc'], ['diretorias.id'], ),
    sa.ForeignKeyConstraint(['id_divisao_asc'], ['divisoes.id'], ),
    sa.ForeignKeyConstraint(['id_gerencia_asc'], ['gerencias.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contrato'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('log_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('app', sa.String(length=50), nullable=False),
    sa.Column('data_hora', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_usuario'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log_user')
    op.drop_table('user')
    op.drop_table('gerencias')
    op.drop_table('divisoes')
    op.drop_table('diretorias')
    op.drop_table('coordenacoes')
    # ### end Alembic commands ###
