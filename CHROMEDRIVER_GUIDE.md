# 🔧 ChromeDriver 수동 설치 가이드

## 문제 상황

다음과 같은 오류가 발생했나요?

```
ConnectionError: Could not reach host. Are you offline?
```

이는 회사 네트워크의 방화벽이나 프록시 때문에 ChromeDriver 자동 다운로드가 실패한 것입니다.

---

## ✅ 해결 방법: ChromeDriver 수동 설치

### 📥 Step 1: ChromeDriver 다운로드

#### 방법 1: Chrome 버전 확인 후 다운로드

1. **Chrome 버전 확인**
   - Chrome 브라우저 열기
   - 주소창에 `chrome://version/` 입력
   - 버전 번호 확인 (예: 120.0.6099.109)

2. **ChromeDriver 다운로드**
   - 🔗 [ChromeDriver 다운로드 페이지](https://chromedriver.chromium.org/downloads)
   - 또는 🔗 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
   - Chrome 버전과 일치하는 ChromeDriver 다운로드

#### 방법 2: 최신 안정 버전 다운로드

Chrome 최신 버전을 사용 중이라면:
- 🔗 [최신 ChromeDriver](https://chromedriver.chromium.org/downloads)
- "ChromeDriver XX.X.XXXX.XX" 클릭
- 운영체제에 맞는 파일 다운로드:
  - **Windows**: `chromedriver_win32.zip`
  - **Mac (Intel)**: `chromedriver_mac64.zip`
  - **Mac (M1/M2)**: `chromedriver_mac_arm64.zip`
  - **Linux**: `chromedriver_linux64.zip`

### 📂 Step 2: 압축 해제 및 배치

#### Windows

1. 다운로드한 ZIP 파일 압축 해제
2. `chromedriver.exe` 파일을 다음 중 한 곳에 복사:
   
   **옵션 A: 프로젝트 폴더** (추천)
   ```
   C:\...\프로젝트폴더\chromedriver.exe
   ```
   
   **옵션 B: C 드라이브**
   ```
   C:\chromedriver.exe
   ```
   
   **옵션 C: Program Files**
   ```
   C:\Program Files\chromedriver.exe
   ```

#### Mac

1. 다운로드한 ZIP 파일 압축 해제
2. 터미널에서 실행:
   ```bash
   # 다운로드 폴더에서
   cd ~/Downloads
   
   # 실행 권한 부여
   chmod +x chromedriver
   
   # /usr/local/bin으로 이동 (추천)
   sudo mv chromedriver /usr/local/bin/
   
   # 또는 프로젝트 폴더로 이동
   mv chromedriver /path/to/your/project/
   ```

3. **Mac 보안 설정**
   ```bash
   # Gatekeeper 우회
   xattr -d com.apple.quarantine /usr/local/bin/chromedriver
   ```

#### Linux

```bash
# 다운로드 폴더에서
cd ~/Downloads

# 압축 해제
unzip chromedriver_linux64.zip

# 실행 권한 부여
chmod +x chromedriver

# /usr/local/bin으로 이동 (추천)
sudo mv chromedriver /usr/local/bin/

# 또는 /usr/bin으로 이동
sudo mv chromedriver /usr/bin/
```

### ✅ Step 3: 설치 확인

#### 터미널/명령 프롬프트에서 확인

**Windows (CMD):**
```cmd
chromedriver --version
```

**Mac/Linux:**
```bash
chromedriver --version
```

정상 출력 예시:
```
ChromeDriver 120.0.6099.109
```

---

## 🚀 사용 방법

### 방법 1: 자동 탐색 (프로젝트 폴더 또는 시스템 PATH)

ChromeDriver를 위의 권장 위치에 배치했다면:

```bash
streamlit run streamlit_app.py
```

그냥 실행하면 자동으로 찾습니다!

### 방법 2: Streamlit UI에서 경로 지정

1. Streamlit 앱 실행
2. 왼쪽 사이드바에서 **"ChromeDriver 경로 직접 지정"** 체크
3. ChromeDriver 경로 입력:
   - Windows: `C:\chromedriver.exe`
   - Mac: `/usr/local/bin/chromedriver`
   - Linux: `/usr/local/bin/chromedriver`

### 방법 3: 코드에서 직접 지정

```python
from download_maple_icons_selenium import MapleIconDownloader

downloader = MapleIconDownloader()
downloader.start_browser(chromedriver_path='C:\\chromedriver.exe')
```

---

## 🔍 자동 탐색 경로

프로그램이 자동으로 찾는 경로들:

### Windows
```
C:\chromedriver.exe
C:\Program Files\chromedriver.exe
C:\Program Files (x86)\chromedriver.exe
현재폴더\chromedriver.exe
```

### Mac/Linux
```
/usr/local/bin/chromedriver
/usr/bin/chromedriver
~/chromedriver
현재폴더/chromedriver
```

---

## ❌ 문제 해결

### "chromedriver.exe가 실행되지 않습니다" (Windows)

Windows Defender나 백신 프로그램이 차단할 수 있습니다:

1. Windows 보안 열기
2. 바이러스 및 위협 방지
3. 제외 추가
4. `chromedriver.exe` 파일 추가

### "Permission denied" (Mac/Linux)

```bash
# 실행 권한 부여
chmod +x /path/to/chromedriver
```

### "chromedriver cannot be opened" (Mac)

```bash
# Gatekeeper 우회
xattr -d com.apple.quarantine /path/to/chromedriver

# 또는 시스템 환경설정에서:
# 보안 및 개인 정보 보호 > 일반 > "확인 없이 열기" 클릭
```

### Chrome 버전과 ChromeDriver 버전이 맞지 않음

```
session not created: This version of ChromeDriver only supports Chrome version XX
```

해결:
1. Chrome 버전 확인: `chrome://version/`
2. 일치하는 ChromeDriver 다운로드
3. 교체

---

## 📋 빠른 체크리스트

- [ ] Chrome 브라우저 설치 확인
- [ ] Chrome 버전 확인 (`chrome://version/`)
- [ ] 일치하는 ChromeDriver 다운로드
- [ ] 압축 해제
- [ ] 권장 위치에 배치
- [ ] 실행 권한 부여 (Mac/Linux)
- [ ] 터미널에서 `chromedriver --version` 확인
- [ ] 프로그램 실행

---

## 💡 추가 팁

### 여러 버전 관리

프로젝트 폴더에 배치하면 프로젝트마다 다른 버전 사용 가능:

```
프로젝트A/
  ├── chromedriver.exe (버전 120)
  └── streamlit_app.py

프로젝트B/
  ├── chromedriver.exe (버전 119)
  └── streamlit_app.py
```

### PATH 환경변수에 추가 (고급)

**Windows:**
1. 시스템 환경 변수 편집
2. Path 변수에 ChromeDriver 폴더 추가
3. 재부팅

**Mac/Linux:**
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export PATH="$PATH:/path/to/chromedriver/folder"
```

---

## 🆘 그래도 안 될 때

1. **Chrome 재설치**
2. **ChromeDriver 재다운로드**
3. **백신 프로그램 일시 중지**
4. **관리자 권한으로 실행**
5. **다른 위치에 배치 후 경로 직접 지정**

---

**이제 정상적으로 작동할 거예요! 🎉**
