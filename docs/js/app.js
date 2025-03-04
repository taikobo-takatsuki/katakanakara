document.addEventListener('DOMContentLoaded', function() {
    const languageInput = document.getElementById('languageInput');
    const textInput = document.getElementById('textInput');
    const convertBtn = document.getElementById('convertBtn');
    const detectBtn = document.getElementById('detectBtn');
    const resultCard = document.getElementById('resultCard');
    const originalLanguage = document.getElementById('originalLanguage').querySelector('span');
    const detectedInfo = document.getElementById('detectedInfo');
    const detectedLanguage = document.querySelector('.detected-language');
    const confidenceValue = document.querySelector('.confidence-value');
    const englishResult = document.getElementById('englishResult');
    const katakanaResult = document.getElementById('katakanaResult');
    const languageList = document.getElementById('languageList');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // 言語リストを生成
    populateLanguageList();

    // 言語リストからの選択
    languageList.addEventListener('click', function(e) {
        if (e.target.classList.contains('language-item')) {
            const language = e.target.textContent;
            languageInput.value = language;
            convertLanguage(language);
        }
    });

    // 変換ボタンのクリック
    convertBtn.addEventListener('click', function() {
        const language = languageInput.value.trim();
        if (language) {
            convertLanguage(language);
        }
    });

    // 検出ボタンのクリック
    detectBtn.addEventListener('click', function() {
        const text = textInput.value.trim();
        if (text) {
            detectLanguage(text);
        }
    });

    // Enterキーでの変換
    languageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const language = languageInput.value.trim();
            if (language) {
                convertLanguage(language);
            }
        }
    });

    // 言語リストを生成する関数
    function populateLanguageList() {
        const languages = Object.keys(languageData).sort();
        languages.forEach(language => {
            const div = document.createElement('div');
            div.className = 'language-item';
            div.textContent = language;
            languageList.appendChild(div);
        });
    }

    // 言語変換関数
    function convertLanguage(language) {
        showLoading();
        
        if (languageData[language]) {
            const result = {
                language: language,
                english: languageData[language].english,
                katakana: languageData[language].katakana
            };
            
            setTimeout(() => {
                hideLoading();
                displayResult(result);
            }, 500);
        } else {
            setTimeout(() => {
                hideLoading();
                displayError(`「${language}」はデータベースにありません`);
            }, 500);
        }
    }

    // 言語検出関数
    function detectLanguage(text) {
        showLoading();
        
        // 言語検出APIの代わりにランダムな言語を選択（デモ用）
        setTimeout(() => {
            // 実際のAPIを使用する場合はここを変更
            // ここでは簡易的な言語検出ロジックを実装
            let detectedCode = detectLanguageCode(text);
            
            if (detectedCode && langCodeToName[detectedCode]) {
                const languageName = langCodeToName[detectedCode];
                
                if (languageData[languageName]) {
                    const result = {
                        detected: true,
                        language: languageName,
                        confidence: 0.8,
                        english: languageData[languageName].english,
                        katakana: languageData[languageName].katakana
                    };
                    
                    hideLoading();
                    displayDetectionResult(text, result);
                } else {
                    hideLoading();
                    displayError('検出された言語はサポートされていません');
                }
            } else {
                hideLoading();
                displayError('言語を検出できませんでした');
            }
        }, 1000);
    }
    
    // 簡易的な言語検出ロジック
    function detectLanguageCode(text) {
        // 日本語（ひらがな、カタカナ、漢字）
        if (/[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/.test(text)) {
            return 'ja';
        }
        
        // 中国語（簡体字、繁体字）
        if (/[\u4E00-\u9FFF]/.test(text) && !/[\u3040-\u309F\u30A0-\u30FF]/.test(text)) {
            return 'zh';
        }
        
        // 韓国語（ハングル）
        if (/[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]/.test(text)) {
            return 'ko';
        }
        
        // キリル文字（ロシア語など）
        if (/[\u0400-\u04FF]/.test(text)) {
            return 'ru';
        }
        
        // アラビア文字
        if (/[\u0600-\u06FF]/.test(text)) {
            return 'ar';
        }
        
        // タイ語
        if (/[\u0E00-\u0E7F]/.test(text)) {
            return 'th';
        }
        
        // ヒンディー語（デーヴァナーガリー文字）
        if (/[\u0900-\u097F]/.test(text)) {
            return 'hi';
        }
        
        // 英語（デフォルト）
        return 'en';
    }

    // 結果表示関数
    function displayResult(data) {
        originalLanguage.textContent = data.language;
        englishResult.textContent = data.english;
        katakanaResult.textContent = data.katakana;
        detectedInfo.style.display = 'none';
        resultCard.style.display = 'block';
    }

    // 検出結果表示関数
    function displayDetectionResult(text, data) {
        originalLanguage.textContent = text;
        detectedLanguage.textContent = data.language;
        confidenceValue.textContent = (data.confidence * 100).toFixed(0) + '%';
        englishResult.textContent = data.english;
        katakanaResult.textContent = data.katakana;
        detectedInfo.style.display = 'block';
        resultCard.style.display = 'block';
    }

    // エラー表示関数
    function displayError(message) {
        originalLanguage.textContent = '';
        englishResult.textContent = '';
        katakanaResult.textContent = message;
        detectedInfo.style.display = 'none';
        resultCard.style.display = 'block';
    }
    
    // ローディング表示
    function showLoading() {
        loadingIndicator.style.display = 'block';
        resultCard.style.display = 'none';
    }
    
    // ローディング非表示
    function hideLoading() {
        loadingIndicator.style.display = 'none';
    }
}); 