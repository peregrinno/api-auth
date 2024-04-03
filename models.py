from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz
import json
import secrets

db = SQLAlchemy()

class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(30), nullable=False)
    value = db.Column(db.String(150), nullable=False) 
    
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Diretorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    
    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome
        
    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nome': self.nome
        }

class Coordenacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    
    
    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome
        
    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nome': self.nome
        }

class Gerencias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    
    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome
        
    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nome': self.nome
        }

class Divisoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    
    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome
        
    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nome': self.nome
        }
     
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    matricula = db.Column(db.Integer, nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    contrato = db.Column(db.String(50), unique=True, nullable=False)
    apps_permissoes = db.Column(db.JSON, nullable=False)
    criado = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ultima_mod = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=False)  
    ligacao = db.Column(db.String(100), nullable=True)
    id_diretoria_asc = db.Column(db.Integer, db.ForeignKey(Diretorias.__tablename__ + '.id'), nullable=True)
    id_coord_asc = db.Column(db.Integer, db.ForeignKey(Coordenacoes.__tablename__ + '.id'), nullable=True)
    id_gerencia_asc = db.Column(db.Integer, db.ForeignKey(Gerencias.__tablename__ + '.id'), nullable=True)
    id_divisao_asc = db.Column(db.Integer, db.ForeignKey(Divisoes.__tablename__ + '.id'), nullable=True)
    
    diretoria = db.relationship('Diretorias', backref='user', foreign_keys=[id_diretoria_asc])   
    coordenacao = db.relationship('Coordenacoes', backref='user', foreign_keys=[id_coord_asc])
    gerencia = db.relationship('Gerencias', backref='user', foreign_keys=[id_gerencia_asc])
    divisao = db.relationship('Divisoes', backref='user', foreign_keys=[id_divisao_asc])
    
    def __init__(self, username, email, password, matricula, cargo, contrato, apps_permissoes, id_diretoria_asc, id_coord_asc, id_gerencia_asc, id_divisao_asc):
        tz_recife = pytz.timezone('America/Recife')
        
        self.username = username
        self.email = email
        self.set_password(password)
        self.matricula = matricula
        self.cargo = cargo
        self.contrato = contrato
        self.apps_permissoes = apps_permissoes  
        self.criado = datetime.now(tz_recife)
        self.ultima_mod = datetime.now(tz_recife)
        self.status = 1
        self.id_diretoria_asc = id_diretoria_asc
        self.id_coord_asc = id_coord_asc
        self.id_gerencia_asc = id_gerencia_asc
        self.id_divisao_asc = id_divisao_asc
        self.set_ligacao(id_diretoria_asc, id_coord_asc, id_gerencia_asc, id_divisao_asc)
    
    #Passando os setores (set_ligacao('DTI', 'CTI', 'GINF', 'DIAP')), faz algo como isso: DTI > CTI > GINF > DIAP
    def set_ligacao(self, id_diretoria_asc, id_coord_asc, id_gerencia_asc, id_divisao_asc):
        id = id_diretoria_asc
        diretoria = Diretorias.query.get_or_404(id)
        
        id = id_coord_asc
        coordenacao = Coordenacoes.query.get_or_404(id)
        
        id=id_gerencia_asc
        gerencia = Gerencias.query.get_or_404(id)
        
        id=id_divisao_asc
        divisao = Divisoes.query.get_or_404(id)
        
        hierarquia = [diretoria.sigla, coordenacao.sigla, gerencia.sigla, divisao.sigla]
        
        lig = ""
        
        for item in hierarquia:
            if item != '':
                lig += f"{item} > "
        
        self.ligacao = lig[:-2]
    
    def to_dict(self):
         return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'matricula': self.matricula,
            'cargo': self.cargo,
            'contrato': self.contrato,
            'apps_permissoes': self.apps_permissoes,
            'criado': self.criado.isoformat(),
            'ultima_mod': self.ultima_mod.isoformat(),  
            'status': self.status,
            'setor': {
                'diretoria': self.diretoria.sigla,
                'coordenacao': self.coordenacao.sigla,
                'gerencia': self.gerencia.sigla,
                'divisao': self.divisao.sigla,
            },
            'ligacao': self.ligacao
    }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
        
class LogUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey(User.__tablename__ + '.id'), nullable=False)
    app = db.Column(db.String(50), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    usuario = db.relationship('User', backref='log', foreign_keys=[id_usuario])
    
    def __init__(self, id_usuario):
        tz_recife = pytz.timezone('America/Recife')
        
        self.id_usuario = id_usuario
        self.data_hora =  datetime.now(tz_recife)
        
    def to_dict(self):
        return {
            'id_log': self.id,
            'usuario': {
                'id': self.usuario.id,
                'username': self.usuario.username,
                'setor': self.usuario.setor.ligacao,
            },
            'data_hora': self.data_hora,
        }
        
