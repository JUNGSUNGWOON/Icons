import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urljoin, urlparse

class MapleIconDownloader:
    def __init__(self, base_url="http://10.10.201.224:3030/China/Search", download_folder="maple_icons"):
        self.base_url = base_url
        self.download_folder = download_folder
        self.driver = None
        
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
    
    def _get_chrome_driver_path(self):
        """ChromeDriver 경로를 자동으로 찾거나 None 반환"""
        import shutil
        
        # 시스템 PATH에서 chromedriver 찾기
        chromedriver = shutil.which('chromedriver')
        if chromedriver:
            return chromedriver
        
        # 일반적인 설치 경로들 확인
        common_paths = [
            # Windows
            r"C:\chromedriver.exe",
            r"C:\Program Files\chromedriver.exe",
            r"C:\Program Files (x86)\chromedriver.exe",
            os.path.join(os.getcwd(), "chromedriver.exe"),
            # Mac/Linux
            "/usr/local/bin/chromedriver",
            "/usr/bin/chromedriver",
            os.path.join(os.path.expanduser("~"), "chromedriver"),
            os.path.join(os.getcwd(), "chromedriver"),
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def start_browser(self, headless=False, chromedriver_path=None):
        """
        브라우저를 시작합니다.
        
        Args:
            headless: 헤드리스 모드 사용 여부
            chromedriver_path: ChromeDriver 실행 파일 경로 (None이면 자동 탐색)
        """
        if self.driver is None:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # ChromeDriver 경로 설정
            if chromedriver_path is None:
                chromedriver_path = self._get_chrome_driver_path()
            
            try:
                if chromedriver_path and os.path.exists(chromedriver_path):
                    # ChromeDriver 경로가 있으면 사용
                    service = Service(chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    # 경로가 없으면 webdriver-manager 시도
                    try:
                        from webdriver_manager.chrome import ChromeDriverManager
                        service = Service(ChromeDriverManager().install())
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    except Exception as e:
                        # webdriver-manager도 실패하면 기본 설정으로 시도
                        print(f"⚠️ webdriver-manager 사용 실패: {e}")
                        print("⚠️ 기본 Chrome 드라이버로 시도합니다...")
                        self.driver = webdriver.Chrome(options=chrome_options)
                
                self.driver.set_page_load_timeout(30)
                
            except Exception as e:
                raise Exception(
                    f"Chrome 브라우저 시작 실패: {e}\n\n"
                    "해결 방법:\n"
                    "1. Chrome 브라우저가 설치되어 있는지 확인\n"
                    "2. ChromeDriver를 다운로드하여 프로젝트 폴더에 배치\n"
                    "   다운로드: https://chromedriver.chromium.org/downloads\n"
                    "3. 또는 start_browser(chromedriver_path='경로') 로 직접 지정"
                )
    
    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def download_item_icon(self, item_index):
        if self.driver is None:
            return False, "브라우저가 시작되지 않았습니다"
        
        try:
            search_url = f"{self.base_url}?From=Item&SearchString={item_index}"
            self.driver.get(search_url)
            
            # 페이지 로드 대기
            time.sleep(1.5)
            
            # CN 이름 추출
            cn_name = None
            
            try:
                # 테이블에서 Language 행 찾기
                rows = self.driver.find_elements(By.TAG_NAME, 'tr')
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    if len(cells) >= 2:
                        first_cell = cells[0].text.strip()
                        second_cell = cells[1].text.strip()
                        
                        if first_cell == "Language":
                            if '[CN]' in second_cell:
                                parts = second_cell.split('[CN]')
                                if len(parts) > 1:
                                    cn_text = parts[1].strip()
                                    cn_name = cn_text.split('\n')[0].split('[')[0].strip()
                                    break
            except:
                pass
            
            if not cn_name:
                try:
                    page_source = self.driver.page_source
                    pattern = r'\[CN\]\s*([^\[<\n]+)'
                    match = re.search(pattern, page_source)
                    if match:
                        cn_name = match.group(1).strip()
                except:
                    pass
            
            if not cn_name:
                cn_name = f"item_{item_index}"
            
            # 파일명에 사용할 수 없는 문자 제거
            cn_name = re.sub(r'[<>:"/\\|?*]', '_', cn_name)
            
            # 이미지 찾기
            img_url = None
            try:
                images = self.driver.find_elements(By.TAG_NAME, 'img')
                
                image_sources = []
                for i, img in enumerate(images):
                    src = img.get_attribute('src')
                    alt = img.get_attribute('alt') or ''
                    title = img.get_attribute('title') or ''
                    
                    if src:
                        image_sources.append({
                            'index': i,
                            'src': src,
                            'alt': alt,
                            'title': title
                        })
                
                # 이미지 선택 우선순위
                for img_info in image_sources:
                    src = img_info['src'].lower()
                    alt = img_info['alt'].lower()
                    
                    # 제외할 이미지
                    if any(exclude in src for exclude in ['logo', 'banner', 'header', 'footer']):
                        continue
                    
                    # 우선 선택할 이미지
                    if any(keyword in src for keyword in ['icon', 'item', 'equipment', 'img']):
                        img_url = img_info['src']
                        break
                    
                    if any(keyword in alt for keyword in ['icon', 'item', 'equipment']):
                        img_url = img_info['src']
                        break
                
                # 키워드로 찾지 못한 경우 첫 번째 이미지 사용
                if not img_url and image_sources:
                    img_url = image_sources[0]['src']
            except Exception as e:
                pass
            
            if not img_url:
                return False, "이미지 없음"
            
            # 상대 URL을 절대 URL로 변환
            if img_url.startswith('/'):
                parsed = urlparse(self.base_url)
                img_url = f"{parsed.scheme}://{parsed.netloc}{img_url}"
            elif not img_url.startswith('http'):
                img_url = urljoin(self.base_url, img_url)
            
            # 파일명 생성
            filename = f"{cn_name}_{item_index}.png"
            filepath = os.path.join(self.download_folder, filename)
            
            # 이미지 다운로드
            response = requests.get(img_url, timeout=10)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True, cn_name
            else:
                return False, f"HTTP {response.status_code}"
            
        except Exception as e:
            return False, str(e)
    
    def download_multiple_items(self, item_indices, progress_callback=None, chromedriver_path=None):
        """
        여러 아이템을 다운로드합니다.
        
        Args:
            item_indices: 다운로드할 아이템 인덱스 리스트
            progress_callback: 진행 상황 콜백 함수 (index, total, success, fail, message)
            chromedriver_path: ChromeDriver 실행 파일 경로 (None이면 자동 탐색)
        
        Returns:
            dict: 다운로드 결과 통계
        """
        self.start_browser(headless=True, chromedriver_path=chromedriver_path)
        
        success_count = 0
        fail_count = 0
        results = []
        start_time = time.time()
        
        try:
            for i, item_index in enumerate(item_indices, 1):
                success, message = self.download_item_icon(item_index)
                
                if success:
                    success_count += 1
                    status = "✅"
                else:
                    fail_count += 1
                    status = "❌"
                
                results.append({
                    'index': item_index,
                    'success': success,
                    'message': message
                })
                
                # 진행 상황 콜백 호출
                if progress_callback:
                    progress_callback(i, len(item_indices), success_count, fail_count, 
                                    f"{status} {item_index}: {message}")
                else:
                    print(f"[{i}/{len(item_indices)}] {status} {item_index}: {message}")
                
                if i < len(item_indices):
                    time.sleep(0.3)
        
        finally:
            self.close_browser()
        
        elapsed_time = time.time() - start_time
        
        return {
            'success': success_count,
            'fail': fail_count,
            'total': len(item_indices),
            'elapsed_time': elapsed_time,
            'results': results
        }
