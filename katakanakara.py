import json
from typing import Dict, List, Any, Tuple, Optional
from langdetect import detect, LangDetectException

def load_language_mapping() -> Dict[str, Dict[str, str]]:
    """
    言語名とそのカタカナ表記のマッピングを読み込みます
    """
    with open('language_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_to_katakana(language: str, mapping: Dict[str, Dict[str, str]]) -> str:
    """
    入力された言語名をカタカナに変換します
    """
    if language in mapping:
        return mapping[language]["katakana"]
    else:
        return f"「{language}」はデータベースにありません"

def get_english_name(language: str, mapping: Dict[str, Dict[str, str]]) -> str:
    """
    入力された言語名の英語名を返します
    """
    if language in mapping:
        return mapping[language]["english"]
    else:
        return ""

def get_all_languages(mapping: Dict[str, Dict[str, str]]) -> List[str]:
    """
    サポートされている全言語のリストを返します
    """
    return list(mapping.keys())

def detect_language(text: str) -> Optional[Tuple[str, float]]:
    """
    テキストの言語を検出します
    戻り値: (言語コード, 信頼度) または None（検出失敗時）
    """
    try:
        lang_code = detect(text)
        # 言語コードから言語名へのマッピング
        lang_code_to_name = {
            'ja': '日本語',
            'en': '英語',
            'fr': 'フランス語',
            'de': 'ドイツ語',
            'es': 'スペイン語',
            'it': 'イタリア語',
            'pt': 'ポルトガル語',
            'ru': 'ロシア語',
            'zh-cn': '中国語',
            'zh-tw': '中国語',
            'ko': '韓国語',
            'ar': 'アラビア語',
            'hi': 'ヒンディー語',
            'bn': 'ベンガル語',
            'ur': 'ウルドゥー語',
            'fa': 'ペルシャ語',
            'tr': 'トルコ語',
            'nl': 'オランダ語',
            'sv': 'スウェーデン語',
            'fi': 'フィンランド語',
            'da': 'デンマーク語',
            'no': 'ノルウェー語',
            'pl': 'ポーランド語',
            'cs': 'チェコ語',
            'sk': 'スロバキア語',
            'hu': 'ハンガリー語',
            'ro': 'ルーマニア語',
            'bg': 'ブルガリア語',
            'el': 'ギリシャ語',
            'uk': 'ウクライナ語',
            'th': 'タイ語',
            'vi': 'ベトナム語',
            'id': 'インドネシア語',
            'ms': 'マレー語',
            'tl': 'タガログ語',
            'sw': 'スワヒリ語',
            'af': 'アフリカーンス語',
            'sq': 'アルバニア語',
            'hy': 'アルメニア語',
            'az': 'アゼルバイジャン語',
            'eu': 'バスク語',
            'be': 'ベラルーシ語',
            'ca': 'カタルーニャ語',
            'hr': 'クロアチア語',
            'et': 'エストニア語',
            'gl': 'ガリシア語',
            'ka': 'ジョージア語',
            'he': 'ヘブライ語',
            'is': 'アイスランド語',
            'kk': 'カザフ語',
            'lv': 'ラトビア語',
            'lt': 'リトアニア語',
            'mk': 'マケドニア語',
            'mn': 'モンゴル語',
            'sr': 'セルビア語',
            'sl': 'スロベニア語',
            'uz': 'ウズベク語'
        }
        
        if lang_code in lang_code_to_name:
            return (lang_code_to_name[lang_code], 0.8)  # 信頼度は仮の値
        else:
            return None
    except LangDetectException:
        return None

if __name__ == "__main__":
    # 動作確認用のコード
    try:
        mapping = load_language_mapping()
        print("カタカナ変換サービスが起動しました")
        print(f"サポートされている言語数: {len(mapping)}")
        
        # テスト
        test_languages = ["英語", "日本語", "フランス語", "存在しない言語"]
        for lang in test_languages:
            english = get_english_name(lang, mapping)
            katakana = convert_to_katakana(lang, mapping)
            print(f"{lang} -> {english} -> {katakana}")
            
        # 言語検出のテスト
        test_texts = [
            "こんにちは、世界",
            "Hello, world",
            "Bonjour le monde",
            "Hola mundo",
            "你好，世界"
        ]
        
        for text in test_texts:
            result = detect_language(text)
            if result:
                lang_name, confidence = result
                print(f"テキスト: {text}")
                print(f"検出された言語: {lang_name} (信頼度: {confidence:.2f})")
                if lang_name in mapping:
                    print(f"英語名: {mapping[lang_name]['english']}")
                    print(f"カタカナ: {mapping[lang_name]['katakana']}")
                print("---")
            else:
                print(f"テキスト: {text} - 言語を検出できませんでした")
    except FileNotFoundError:
        print("language_mapping.jsonファイルが見つかりません。")
        print("先にcreate_mapping.pyを実行してマッピングファイルを作成してください。") 