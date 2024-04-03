from .common import *

from . import api_blueprint


@api_blueprint.route("/", methods=["GET", "POST"])
@require_auth_token
def health_check():
    app_version = os.getenv("APP_VERSION")
    
    context = {
        'Application': 'API de autenticação do Grande Recife',
        'Version': app_version,
        'Environment': os.getenv("ENVIRONMENT")
    }
    
    return jsonify(context), 200


# Valida existência do usuário por email
@api_blueprint.route("/check_user", methods=["GET"])
@require_auth_token
def check_user():
    try:
        email = request.args.get('mail')
    except:
        return jsonify({'message': 'Parametros não reconhecidos'})
    
    
    if re.match(r"[a-zA-Z0-9._%+-]+@granderecife\.pe\.gov\.br$", email):
        user_email = User.query.filter_by(email=email).first()
        
        if not user_email:
            return jsonify({'message': 'Usuário não encontrado na base.','_code':'1001'}), 200
        else:
            return jsonify({'message': 'Usuário encontrado!','_code':'1002'}), 200
    else:
        return jsonify({'message': 'Usuário não faz parte do Grande Recife!','_code':'1003'}), 200


# Autentica usuário
@api_blueprint.route("/auth_user", methods=["POST"])
@require_auth_token
def auth_user():
    try:
        email = request.args.get('mail')
        password = request.args.get('password')
    except:
        return jsonify({'message': 'Parametros não reconhecidos'})
    
    if re.match(r"[a-zA-Z0-9._%+-]+@granderecife\.pe\.gov\.br$", email):
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado na base.'}), 200
        else:
            if user and user.check_password(password):
                if not user.status == 1:
                    return jsonify({'message': 'Usuário desativado', '_code':'1000'})
                else:
                    return jsonify(user.to_dict())
    else:
        return jsonify({'message': 'Usuário não faz parte do Grande Recife!'}), 200

    
    
    

