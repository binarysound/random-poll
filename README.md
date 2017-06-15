# random-poll
당신의 모든 질문, 모든 세상이 답변합니다.

# Build & Running
### Prerequisite
- [Docker](https://docs.docker.com/engine/installation/) >= 17.03.1-ce
- [Docker Compose](https://docs.docker.com/compose/install/) >= 1.11.2

### Environment Setup
`./docs/example.env`를 참고해 `.env`를 프로젝트 루트에 생성합니다.

### Running
```bash
cd /path/to/random-poll
docker-compose up
```

이제 어플리케이션에 필요한 모든 컨테이너가 맞물려 실행됩니다.

### Database
#### Initialization
데이터베이스를 초기화하려면 우선 `docker ps`로 `web` 컨테이너의 ID를 확인해 접속합니다.
```bash
docker exec -it <web-container-id> /bin/bash
```

이후 컨테이너 내부에서 `/app`으로 이동해 Python shell을 띄운 후 다음을 실행합니다.

```python
from main import db
db.create_all()
```

#### Interaction
외부에서 `psql`로 접속해 데이터베이스의 상태를 확인할 필요가 있다면, `.env`에서 설정한 `DB_EXTERNAL_PORT` 값에 따라 접속합니다.
```bash
psql -h localhost -p <db-external-port> -U postgres
```
