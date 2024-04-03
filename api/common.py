from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for, Blueprint
from flask_migrate import Migrate, upgrade
from flask_cors import CORS
from flask_paginate import Pagination
from config import Config
from models import db
from functools import wraps
from sqlalchemy import desc, func, inspect
import subprocess
import os, re
from datetime import date
from dotenv import load_dotenv

from models import *

def dump_database():
    
    # Executa flask db init
    subprocess.run(['flask', 'db', 'init'])
    
    # Executa flask db migrate
    subprocess.run(['flask', 'db', 'migrate'])

    # Executa flask db upgrade
    subprocess.run(['flask', 'db', 'upgrade'])
    
    existing_token = Tokens.query.filter_by(key='api_token').first()
    
    if not existing_token:
        
        token = Tokens(
            key='api_token',
            value=os.getenv("TOKEN_API_ACESS_KEY")
        )
        
        db.session.add(token)
        db.session.commit()
    
    #CHECAR DIRETORIAS
    existing_diretorias = Diretorias.query.filter_by(sigla='DTI').first()
    
    if not existing_diretorias:
        
        diretorias = [
            ['ADMIN', 'SUDO'],
            ['DIRETOR PRESIDENTE','DP'],
            ['DIRETORIA DE ENGENHARIA E MANUTENÇÃO','DEM'],
            ['DIRETORIA DE PLANEJAMENTO','DPL'],
            ['DIRETORIA DE OPERAÇÕES','DOP'],
            ['DIRETORIA DE GESTÃO ORGANIZACIONAL','DGO'],
            ['DIRETORIA DE PROJETOS ESPECIAIS','DPE'],
            ['DIRETORIA DE TECNOLOGIA DA INFORMÇÃO','DTI'],
            ]
        
        for nome, sigla in diretorias:
            # Se o setor não existir, cria um novo setor padrão
            default_setor = Diretorias(
                nome=nome,
                sigla=sigla,
            )
            db.session.add(default_setor)
            db.session.commit()
    
    # CHECAR COORDENACOES
    existing_coordenacoes = Coordenacoes.query.filter_by(sigla='OUV').first()

    if not existing_coordenacoes:

        coordenacoes = [
            ['ADMIN', 'SUDO'],
            ['OUVIDORIA', 'OUV'],
            ['CONSELHO FISCAL', 'CF'],
            ['CHEFE DE GABINETE', 'GAB'],
            ['COORDENADORIA DE GESTÃO E LICITAÇÃO', 'CGL'],
            ['COORDENADORIA DE ENGENHARIA E MANUTENÇÃO', 'CEM'],
            ['COORDENADORIA DE PLANEJAMENTO', 'CPO'],
            ['COORDENADORIA DE OPERAÇÕES', 'COP'],
        ]

        for nome, sigla in coordenacoes:
            # Se a coordenacao não existir, cria uma nova coordenacao padrão
            default_coordenacao = Coordenacoes(
                nome=nome,
                sigla=sigla,
            )
            db.session.add(default_coordenacao)
            db.session.commit()

    # CHECAR GERENCIAS
    existing_gerencias = Gerencias.query.filter_by(sigla='GTEP').first()

    if not existing_gerencias:

        gerencias = [
            ['ADMIN', 'SUDO'],
            ['GERÊNCIA DE MANUTENÇÃO DE TERMINAIS, ESTAÇÕES E PARADAS', 'GTEP'],
            ['GERÊNCIA DE PROJETOS E OBRAS', 'GEPO'],
            ['GERÊNCIA ESTRATÉGICA DE STPP', 'GEST'],
            ['GERÊNCIA DE INFORMAÇÃO E PESQUISA', 'GIPE'],
            ['GERÊNCIA DE PROGRAMAÇÃO E INFRAESTRUTURA DO STPP/RMR', 'GPIS'],
            ['GERÊNCIA DE FISCALIZAÇÃO', 'GFIS'],
            ['GERÊNCIA DE MONITORAMENTO', 'GMON'],
            ['GERÊNCIA DE TERMINAIS', 'GTES'],
            ['GERÊNCIA DE BRT E FLUVIAL', 'GEBF'],
            ['GERÊNCIA DE CONTRATOS E CONCESSÃO', 'GECO'],
            ['GERÊNCIA DE SEGURANÇA E INTELIGÊNCIA', 'GESI'],
            ['GERÊNCIA DE INFRAESTRUTURA DE TI', 'GINF'],
            ['GERÊNCIA DE PATRIMÔNIO E LOGÍSTICA', 'GPLO'],
            ['GERÊNCIA FINANCEIRA', 'GFIN'],
            ['GERÊNCIA DE CAPITAL HUMANO', 'GECH'],
            ['GERÊNCIA DE GESTÃO E ORÇAMENTO', 'GGOR'],
            ['GERÊNCIA DE PROJETOS E ADEQUAÇÃO', 'GEPA'],
            ['GERÊNCIA TÉCNICA DO MEIO AMBIENTE', 'GTMA'],
            ['GERÊNCIA DE CRÍTICAS E RECEBIMENTO', 'GECR'],
            ['GERÊNCIA DE INTERFACE', 'GEIN'],
            ['GERÊNCIA DE RELACIONAMENTO', 'GERE'],
            ['GERÊNCIA DE IMPRENSA', 'GIMP'],
            ['GERÊNCIA DE MARKETING', 'GMKT'],
        ]

        for nome, sigla in gerencias:
            # Se a gerencia não existir, cria uma nova gerencia padrão
            default_gerencia = Gerencias(
                nome=nome,
                sigla=sigla,
            )
            db.session.add(default_gerencia)
            db.session.commit()

    # CHECAR DIVISOES
    existing_divisoes = Divisoes.query.filter_by(sigla='DIFO').first()

    if not existing_divisoes:

        divisoes = [
            ['ADMIN', 'SUDO'],
            ['DIVISÃO DE FISCALIZAÇÃO E OBRAS', 'DIFO'],
            ['DIVISÃO DE MANUTENÇÃO DE EQUIPAMENTOS URBANOS', 'DIME'],
            ['DIVISÃO DE MANUTENÇÃO DE EQUIPAMENTOS ELETRO ELETRONICOS E MECÂNICOS', 'DIEM'],
            ['DIVISÃO DE ORÇAMENTO E CONTROLE DE OBRAS', 'DOCO'],
            ['DIVISÃO DE PROJETOS ARQUITETURA E URBANISMO', 'DPAR'],
            ['DIVISÃO DE ORÇAMENTO, CONTRATOS E PROJETOS DE ENGENHARIA', 'DOCP'],
            ['DIVISÃO DE DESENVOLVIMENTO DO SISTEMA', 'DIDE'],
            ['DIVISÃO DE PLANEJAMENTO DO SISTEMA', 'DIPS'],
            ['DIVISÃO DE INFORMAÇÕES GERENCIAIS', 'DIGE'],
            ['DIVISÃO DE PESQUISA', 'DIPE'],
            ['DIVISÃO DE AVALIAÇÃO DO SISTEMA', 'DIAS'],
            ['DIVISÃO DE AVALIAÇÃO DE DESEMPENHO DAS OPERADORAS', 'DADO'],
            ['DIVISÃO DE PROGRAMAÇÃO DO STPPIRMR', 'DPRO'],
            ['DIVISÃO DE CIRCULAÇÃO E INFRAESTRUTURA DO STPP/RMR', 'DCIS'],
            ['DIVISÃO DE FISCALIZAÇÃO DA OPERAÇÃO', 'DIFI'],
            ['DIVISÃO DE VISTORIA DA FROTA', 'DIVI'],
            ['DIVISÃO DE CONTROLE DA INFRAÇÃO', 'DICI'],
            ['DIVISÃO DE MONITORAMENTO DA PROGRAMAÇÃO', 'DIMP'],
            ['DIVISÃO DE CONTROLE E MONITORAMENTO OPERACIONAL', 'DCMO'],
            ['DIVISÃO DE TERMINAIS', 'DITE'],
            ['DIVISÃO DE GESTÃO OPERACIONAL DOS CONTRATOS', 'DGOC'],
            ['DIVISÃO DE GESTÃO FINANCEIRA DOS CONTRATOS', 'DGFC'],
            ['DIVISÃO DE SUPORTE À INFRAESTRUTURA', 'DISU'],
            ['DIVISÃO DE APLICATIVOS', 'DIAP'],
            ['DIVISÃO DE AQUISIÇÃO DE BENS', 'DABS'],
            ['DIVISÃO DE PATRIMÔNIO E MATERIAL', 'DIPM'],
            ['DIVISÃO DE CONTABILIDADE', 'DICO'],
            ['DIVISÃO DE TESOURARIA', 'DITE'],
            ['DIVISÃO DE ADMINISTRAÇÃO DE CAPITAL HUMANO', 'DACH'],
            ['DIVISÃO DE DESENVOLVIMENTO DO CAPITAL HUMANO', 'DDCH'],
            ['DIVISÃO DE PLANEJAMENTO ORÇAMENTÁRIO', 'DIPO'],
            ['DIVISÃO DE DESENVOLVIMENTO ORGANIZACIONAL', 'DIDO'],
            ['DIVISÃO DE BILHETAGEM ELETRÔNICA', 'DBEL'],
            ['DIVISÃO DE LOGÍSTICA', 'DLOG'],
            ['DIVISÃO DE CONTROLE DE DESPESA', 'DICD'],
            ['DIVISÃO DE BENEFÍCIOS', 'DIBE'],
            ['DIVISÃO DE DOCUMENTAÇÃO', 'DDOC'],
            ['DIVISÃO DE CONTROLE DE RECEITA', 'DICR'],
            ['DIVISÃO DE COMERCIALIZAÇÃO', 'DCOM'],
            ['DIVISÃO DE CONCESSÃO DE ABATIMENTOS E GRATUIDADES', 'DIAG'],
            ['DIVISÃO DE RESGATE DE CRÉDITOS', 'DREC'],
            ['ANALISTA TÉCNICO DE PROJEÇÃO E ADEQUAÇÃO', 'ATPA'],
            ['ANALISTA TÉCNICO DE ACOMPANHAMENTO', 'ATAC'],
            ['ANALISTA TÉCNICO DE CRÍTICAS E RECEBIMENTO', 'ATCR'],
            ['ANALISTA TÉCNICO DE ACOMPANHAMENTO', 'ATAC'],
            ['DIVISÃO DE EDUCAÇÃO', 'DIED'],
            ['DIVISÃO DE DIVULGAÇÃO E MARKETING', 'DDMK'],
            ['DIVISÃO DE CONTENCIOSO', 'DICT'],
            ['DIVISÃO DE ATENDIMENTO ÀS COMUNIDADES', 'DIAC'],
            ['DIVISÃO DE COMUNICAÇÃO VISUAL', 'DICV'],
            ['DIVISÃO DE CONTRATOS E CONVÊNIOS', 'DICC'],
            ['DIVISÃO DE ATENDIMENTO AO CLIENTE', 'DCAC'],
        ]

        for nome, sigla in divisoes:
            # Se a divisao não existir, cria uma nova divisao padrão
            default_divisao = Divisoes(
                nome=nome,
                sigla=sigla,
            )
            db.session.add(default_divisao)
            db.session.commit()


    existing_user = User.query.filter_by(username='admin').first()
    
    
    if not existing_user:
        # Se o usuário não existir, cria um novo usuário padrão
        apps = {
            'sudo_apps': 'sudo_apps'
        }
        
        default_user = User(
            username='admin',
            email='dti@granderecife.pe.gov.br',
            password='#@granderecife_apps@#',
            matricula='999999',
            cargo='Administrador',
            contrato='Não se Aplica',
            apps_permissoes=apps,
            id_diretoria_asc=1,
            id_coord_asc=1,
            id_gerencia_asc=1,
            id_divisao_asc=1,
        )
        db.session.add(default_user)
        db.session.commit()
    
    
def require_auth_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Auth-Token')
        if auth_token == os.getenv("TOKEN_API_ACESS_KEY"):
            return f(*args, **kwargs)
        else:
            context = {
                'Situacao': 'Seu acesso é proibido!'
            }
            return jsonify(context), 405
    return decorated_function