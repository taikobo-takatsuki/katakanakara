from flask import Flask, render_template, request, jsonify
from katakanakara import load_language_mapping, convert_to_katakana, get_all_languages, get_english_name, detect_language
import os

app = Flask(__name__)

# 言語マッピングの読み込み
try:
    language_mapping = load_language_mapping()
    print(f"言語マッピングを読み込みました。言語数: {len(language_mapping)}")
except FileNotFoundError:
    print("language_mapping.jsonが見つかりません。create_mapping.pyを実行してください。")
    language_mapping = {}

@app.route('/')
def index():
    """
    メインページを表示します
    """
    languages = get_all_languages(language_mapping)
    return render_template('index.html', languages=languages)

@app.route('/convert', methods=['POST'])
def convert():
    """
    言語をカタカナに変換するAPIエンドポイント
    """
    data = request.get_json()
    language = data.get('language', '')
    
    if not language:
        return jsonify({'error': '言語が指定されていません'}), 400
    
    english = get_english_name(language, language_mapping)
    katakana = convert_to_katakana(language, language_mapping)
    
    return jsonify({
        'language': language,
        'english': english,
        'katakana': katakana
    })

@app.route('/detect', methods=['POST'])
def detect():
    """
    テキストから言語を検出するAPIエンドポイント
    """
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'テキストが指定されていません'}), 400
    
    result = detect_language(text)
    
    if result:
        language_name, confidence = result
        english = get_english_name(language_name, language_mapping)
        katakana = convert_to_katakana(language_name, language_mapping)
        
        return jsonify({
            'detected': True,
            'language': language_name,
            'confidence': confidence,
            'english': english,
            'katakana': katakana
        })
    else:
        return jsonify({
            'detected': False,
            'error': '言語を検出できませんでした'
        })

@app.route('/languages')
def languages():
    """
    サポートされている言語のリストを返すAPIエンドポイント
    """
    languages = get_all_languages(language_mapping)
    return jsonify({'languages': languages})

# 起動時にマッピングファイルが存在しない場合は作成する
if not os.path.exists('language_mapping.json'):
    print("language_mapping.jsonが見つかりません。create_mapping.pyを実行します。")
    import create_mapping
    create_mapping.create_mapping_file()
    language_mapping = load_language_mapping()

if __name__ == '__main__':
    # ローカル開発環境での実行
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 