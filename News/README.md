# Zenith News

현대적인 마크다운 기반 뉴스 퍼블리싱 실습 프로젝트입니다. PostgreSQL 데이터베이스를 사용하며 모든 기사 본문은 Markdown으로 작성된 뒤 서버 측에서 안전하게 렌더링됩니다.

## 필수 요구 사항
- Python 3.11+
- PostgreSQL 13+
- 가상환경 권장

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 데이터베이스 환경 변수
`.env` 혹은 실행 환경에 다음 값을 정의하세요.

```
POSTGRES_DB=zenith_news
POSTGRES_USER=postgres
POSTGRES_PASSWORD=비밀번호
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

초기화:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 주요 기능
- 언론사 구독/해지 (로그인 필요)
- Markdown 기반 기사 작성 및 실시간 미리보기
- `markdown` + `bleach`로 XSS를 차단한 안전한 렌더링
- Class-based Views 기반의 정교한 백엔드 구조
- 반응형 UI/UX, 메시지 피드백, 상태 기반 내비게이션
