from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração do diretório de upload e logging
UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "public/uploads/resultados"  # Caminho correto da pasta de resultados
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)  # Cria o diretório para os resultados

logging.basicConfig(level=logging.INFO)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER


@app.route('/conciliar', methods=['POST'])
def conciliar():
    # Recebe os arquivos e dados do formulário
    base_funcional = request.files.get('baseFuncional')
    base_distribuidor = request.files.get('baseDistribuidor')
    industria = request.form.get('industria', '').lower()
    distribuidor = request.form.get('distribuidor', '').strip().upper()

    # Verifica se os arquivos foram fornecidos
    if not base_funcional or not base_distribuidor:
        return jsonify({"error": "Ambos os arquivos são necessários."}), 400

    # Salva os arquivos localmente com nomes seguros
    base_funcional_path = os.path.join(UPLOAD_FOLDER, secure_filename(base_funcional.filename))
    base_distribuidor_path = os.path.join(UPLOAD_FOLDER, secure_filename(base_distribuidor.filename))
    base_funcional.save(base_funcional_path)
    base_distribuidor.save(base_distribuidor_path)

    try:
        # Seleciona e executa o script Python com base na indústria e no distribuidor
        if industria == 'msd' and distribuidor == 'GSC':
            subprocess.run(['python', 'scripts/conciliacao_msd_gsc.py'], check=True)
        elif industria == 'bayer' and distribuidor == 'GSC':
            subprocess.run(['python', 'scripts/conciliacao_bayer_gsc.py'], check=True)
        else:
            return jsonify({"error": "Indústria ou distribuidor não reconhecido."}), 400

        return jsonify({"message": "Conciliação realizada com sucesso!"})
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar script: {e}")
        return jsonify({"error": "Erro na execução do script de conciliação."}), 500
    except Exception as e:
        logging.exception("Erro inesperado")
        return jsonify({"error": "Erro interno. Por favor, contate o suporte."}), 500


@app.route('/download/conciliacao_finalizada', methods=['GET'])
def download_conciliacao():
    # Caminho do arquivo final gerado pela conciliação
    final_file_path = os.path.join(RESULTS_FOLDER, 'Conciliacao_Finalizada.xlsx')

    # Verifica se o arquivo final existe
    if not os.path.exists(final_file_path):
        return jsonify({"error": "Arquivo final não encontrado."}), 404

    # Serve o arquivo final para download
    return send_from_directory(
        RESULTS_FOLDER,
        'Conciliacao_Finalizada.xlsx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run(debug=True)