# random-poll
당신의 모든 질문, 모든 세상이 답변합니다.

# Build & Running
## With Docker
여기부터 기술된 모든 bash 명령은 **프로젝트 루트에서 실행**합니다.

#### Preparing Images
```bash
docker pull postgres
docker build -t randompoll .
```

#### Running Database
```bash
docker run --name rp-postgres -e POSTGRES_PASSWORD=<db-password> -d postgres
```

`<db-password>`는 원하는 값으로 적절히 선택합니다.
다음 명령어로 `rp-postgres` 컨테이너의 `bridge` 네트워크상에서의 IP 주소를 알아냅니다.

```bash
docker network inspect bridge
```

#### Running Server
위에서 알아낸 `rp-postgres`의 주소와 직접 설정한 `<db-password>`를 바탕으로 `dev.cfg`를 프로젝트 루트에 생성한 후(`./docs/example.dev.cfg`를 참고), 원하는 포트에 서버를 실행합니다. 아래 예시에선 7654번 포트에 띄웠습니다.

```bash
docker run --rm -it -v `pwd`:/src -p 7654:80 randompoll
```

#### Initializing Database
`randompoll` 컨테이너에 접속합니다. 우선 다음 명령어로 현재 실행중인 컨테이너의 ID를 확인합니다.

```bash
docker ps
```

ID를 확인했으면 이제 컨테이너 내에서 `bash` 쉘을 실행합니다.

```bash
docker exec -it <randompoll-container-id> /bin/bash
```

이제 `/src`로 이동한 후, `python` 쉘을 띄우고 다음을 실행합니다.

```python
from main import db
db.create_all()
```

#### Test
브라우저로 `localhost:7654`에 접속해봅니다.

## Without Docker
#### Installing Dependencies
```plain
pip install -r requirements.txt
```

#### Initializing Database
PostgreSQL을 먼저 설치하신 후, 적절한 데이터베이스를 생성합니다. 준비가 다 되었다면 테이블을 만들 차례입니다. Working directory에서 Python shell을 띄운 후 다음을 실행합니다.
```python
from main import db
db.create_all()
```

#### Running Server
`dev.cfg`를 환경에 맞게 적절히 작성한 후 다음을 실행합니다.
```bash
python main.py
```