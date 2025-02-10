from openai import OpenAI
from dotenv import load_dotenv
import os
import deepl
import requests
import json

load_dotenv()  # .envファイルから環境変数を読み込む
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
deepl_api_key=os.getenv('DEEPL_KEY')
slack_webhook_url=os.getenv('WEBHOOK_URL')
LANG_ZH = '中国語(繁体字)'
LANG_ZH_CODE = 'ZH'
LANG_EN_US = '英語'
LANG_EN_US_CODE = 'EN-US'

def first_translate(text, pre_language='日本語', target_language='英語'):

    # 翻訳
    system_text_translate = f"""
    あなたはキャンプ用品レンタル、かつキャンプ場予約サービスのカスタマーサポートです。以下のメール文章に記載されているメール文章は、お客様に送るメールの{pre_language}の文章です。{target_language}でメールを送りたいので、文章を{target_language}に翻訳してください。翻訳結果以外は表示しないでください。
    # メール文章
    {text}
    """

    # DEEPLテスト
    target_language_code = 'EN-US'
    if target_language == '英語':
        target_language_code = 'EN-US'
    elif target_language == '中国語(繁体字)':
        target_language_code = 'ZH'
    # DEEPL接続
    auth_key = deepl_api_key
    translator = deepl.Translator(auth_key)
    result_text = translator.translate_text(text, target_lang=target_language_code)

    '''
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_text_translate}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    return f'{response.choices[0].message.content.strip()}'
    '''

    slack_data = {'text': f"# 文章\n{text}\n\n# 翻訳\n{result_text}"}

    slack_response = requests.post(
        slack_webhook_url,
        data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    if slack_response.status_code != 200:
        raise ValueError(f'リクエストに失敗しました: {response.status_code}, {response.text}')

    return f'{result_text}'


def compare_translated(text, translated_text, pre_language='日本語', target_language='英語'):
    # チェック
    system_text_translate_check = f"""
    あなたはキャンプ用品レンタル、かつキャンプ場予約サービスのカスタマーサポートです。以下の2つの文章は、{pre_language}と{target_language}の同じ内容の文章です。2つを比較して意味やニュアンスが同じになっているかを確認し、{pre_language}に合わせて{target_language}の文章を、{target_language}で修正してください。修正結果以外は表示しないでください。
    # 文章1
    {text}
    # 文章2
    {translated_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_text_translate_check}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return f'{response.choices[0].message.content.strip()}'

def get_reason(user_input, translate_text, compare_translated_text, pre_language='日本語', target_language='英語'):
    # チェック
    system_text_translate_check = f"""
    あなたはキャンプ用品レンタル、かつキャンプ場予約サービスのカスタマーサポートです。文章1は{pre_language}、文章2は{target_language}、文章3は{target_language}で、文章3は文章2より、より文章1の言いたいことやニュアンスに近くなっている文章のはずです。その理由を教えてください。理由以外は表示しないでください。
    # 文章1
    {user_input}
    # 文章2
    {translate_text}
    # 文章3
    {compare_translated_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_text_translate_check}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return f'{response.choices[0].message.content.strip()}'

def revert_translated(text, pre_language='日本語'):
    # チェック
    system_text_translate_check = f"""
    以下の文章を{pre_language}に翻訳してください
    # 文章
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_text_translate_check}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return f'{response.choices[0].message.content.strip()}'

def ja_translated(text):
    # チェック
    system_text_translate_check = f"""
    以下の文章を日本語に翻訳してください
    # 文章
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_text_translate_check}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return f'{response.choices[0].message.content.strip()}'