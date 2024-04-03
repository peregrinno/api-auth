from api import *

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_APP_KEY_API_USER', 'not-secret-flask123')

app.config.from_object(Config)

db.init_app(app)

CORS(app) 

migrate = Migrate(app, db)

load_dotenv()

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('api.health_check',))
    
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        # Executa as migrações antes de iniciar o aplicativo
        dump_database()    
    
    app.run(debug=True, port=os.getenv("PORT", default=8082), use_reloader=True)
    
"""
CÓODIGOS DE RETORNO
RETORNO INTERNO DA API 

CHAVE NOS JSONs "_code"

1000 = USUÁRIO DESATIVADO
1001 = USUÁRIO NÃO ENCONTRADO
1002 = USUÁRIO ENCONTRADO
1003 = USUÁRIO NÃO TEM O DOMINIO DO GRANDE
"""