import subprocess

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def run_make_data(request):
    try:
        result = subprocess.run(
            ["python", "nfcapp/scripts/make-data.py"],  # Windows環境では 'python' を使用
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return redirect('index')
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"エラー: {e.stderr}")

def run_send_data(request):
    try:
        result = subprocess.run(
            ["python", "nfcapp/scripts/send-nfc-data.py"],  # Windows環境では 'python' を使用
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return redirect('index')
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"エラー: {e.stderr}")

def index(request):
    return render(request, 'nfcapp/index.html')

def register_nfc(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        grade = request.POST.get('grade')
        # ここでデータベースへの保存処理や、その他のロジックを追加します
        result = subprocess.run(['python', 'nfcapp/scripts/make-data.py', grade, name], capture_output=True, text=True)
        return HttpResponse(f"""
        名前: {name}, 学年: {grade} が登録されました。<br>
        <br><br>
        <a href="{reverse('index')}">
            <button>戻る</button>
        </a>
    """)

    return render(request, 'nfcapp/register.html')

def attend(request):
    # `send-nfc-data.py` を実行
    subprocess.run(['python', 'nfcapp/scripts/send-nfc-data.py'], check=True)
    
    # 実行後に表示するページ
    return HttpResponse(f"""
    出席登録がされました。
    <br><br>
        <a href="{reverse('index')}">
            <button>戻る</button>
        </a>
        <script>
            // 5秒後にページを再読み込みして、スクリプトを再実行する
            setTimeout(function() {{
                window.location.reload();
            }}, 500);
        </script>
    """)
