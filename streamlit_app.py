import streamlit as st
import os
import time
import zipfile
from io import BytesIO
from download_maple_icons_selenium import MapleIconDownloader
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="메이플스토리 아이템 아이콘 다운로더",
    page_icon="🍁",
    layout="wide"
)

# 세션 상태 초기화
if 'downloaded_items' not in st.session_state:
    st.session_state.downloaded_items = []
if 'download_folder' not in st.session_state:
    st.session_state.download_folder = "maple_icons"
if 'is_downloading' not in st.session_state:
    st.session_state.is_downloading = False

# 타이틀
st.title("🍁 메이플스토리 아이템 아이콘 다운로더")
st.markdown("---")

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    base_url = st.text_input(
        "서버 URL",
        value="http://10.10.201.224:3030/China/Search",
        help="메이플스토리 아이템 검색 서버 URL"
    )
    
    download_folder = st.text_input(
        "다운로드 폴더",
        value="maple_icons",
        help="이미지를 저장할 폴더명"
    )
    st.session_state.download_folder = download_folder
    
    st.markdown("---")
    st.markdown("### 🔧 ChromeDriver 설정")
    
    use_custom_chromedriver = st.checkbox(
        "ChromeDriver 경로 직접 지정",
        help="자동 탐색이 실패할 경우 직접 경로를 지정하세요"
    )
    
    chromedriver_path = None
    if use_custom_chromedriver:
        chromedriver_path = st.text_input(
            "ChromeDriver 경로",
            placeholder="C:\\chromedriver.exe 또는 /usr/local/bin/chromedriver",
            help="ChromeDriver 실행 파일의 전체 경로"
        )
        
        if chromedriver_path and not os.path.exists(chromedriver_path):
            st.warning(f"⚠️ 파일을 찾을 수 없습니다: {chromedriver_path}")
    
    if 'chromedriver_path' not in st.session_state:
        st.session_state.chromedriver_path = None
    
    if use_custom_chromedriver and chromedriver_path:
        st.session_state.chromedriver_path = chromedriver_path
    else:
        st.session_state.chromedriver_path = None
    
    st.markdown("---")
    st.markdown("### 📊 통계")
    if st.session_state.downloaded_items:
        total = len(st.session_state.downloaded_items)
        success = sum(1 for item in st.session_state.downloaded_items if item['success'])
        fail = total - success
        
        st.metric("총 다운로드", total)
        st.metric("성공", success)
        st.metric("실패", fail)
        
        if total > 0:
            st.progress(success / total)
    else:
        st.info("아직 다운로드한 아이템이 없습니다.")

# 메인 컨텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 아이템 인덱스 입력")
    
    # 탭으로 입력 방법 선택
    tab1, tab2 = st.tabs(["직접 입력", "파일 업로드"])
    
    with tab1:
        item_text = st.text_area(
            "아이템 인덱스 (한 줄에 하나씩)",
            height=300,
            placeholder="113302\n113303\n7119\n7120",
            help="아이템 인덱스를 한 줄에 하나씩 입력하세요. '작업 전' 같은 텍스트는 자동으로 건너뜁니다."
        )
    
    with tab2:
        uploaded_file = st.file_uploader(
            "item_list.txt 파일 업로드",
            type=['txt'],
            help="아이템 인덱스가 적힌 텍스트 파일을 업로드하세요."
        )
        
        if uploaded_file is not None:
            item_text = uploaded_file.read().decode('utf-8')
            st.text_area("파일 내용 미리보기", item_text, height=200, disabled=True)

with col2:
    st.header("🚀 다운로드")
    
    # 아이템 인덱스 파싱
    def parse_item_indices(text):
        """텍스트에서 아이템 인덱스 추출"""
        if not text:
            return []
        
        item_indices = []
        for line in text.strip().split('\n'):
            line = line.strip()
            
            # 빈 줄 건너뛰기
            if not line:
                continue
            
            # "작업 전" 같은 텍스트 건너뛰기
            if '작업' in line and '전' in line:
                continue
            
            # 숫자만 추출
            if line.isdigit():
                item_indices.append(int(line))
        
        return item_indices
    
    item_indices = parse_item_indices(item_text)
    
    if item_indices:
        st.success(f"✅ {len(item_indices)}개의 아이템이 입력되었습니다.")
        
        # 처음 10개 표시
        with st.expander("📋 아이템 목록 미리보기 (처음 10개)"):
            for i, idx in enumerate(item_indices[:10], 1):
                st.write(f"{i}. {idx}")
            if len(item_indices) > 10:
                st.write(f"... 외 {len(item_indices) - 10}개")
    else:
        st.warning("⚠️ 아이템 인덱스를 입력해주세요.")
    
    st.markdown("---")
    
    # 다운로드 버튼
    if st.button("🎯 다운로드 시작", type="primary", disabled=not item_indices or st.session_state.is_downloading):
        st.session_state.is_downloading = True
        st.session_state.downloaded_items = []
        
        # 진행 상황 표시 영역
        progress_bar = st.progress(0)
        status_text = st.empty()
        log_container = st.container()
        
        with log_container:
            st.markdown("### 📋 다운로드 로그")
            log_area = st.empty()
            logs = []
        
        # 다운로더 생성
        downloader = MapleIconDownloader(
            base_url=base_url,
            download_folder=download_folder
        )
        
        # 진행 상황 콜백 함수
        def progress_callback(current, total, success, fail, message):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"진행 중... {current}/{total} ({int(progress*100)}%)")
            
            logs.append(f"[{current}/{total}] {message}")
            log_area.code('\n'.join(logs[-10:]), language='text')  # 최근 10개만 표시
        
        # 다운로드 실행
        start_time = time.time()
        results = downloader.download_multiple_items(
            item_indices, 
            progress_callback,
            chromedriver_path=st.session_state.chromedriver_path
        )
        elapsed_time = time.time() - start_time
        
        # 결과 저장
        st.session_state.downloaded_items = results['results']
        st.session_state.is_downloading = False
        
        # 완료 메시지
        progress_bar.progress(1.0)
        status_text.text("✅ 다운로드 완료!")
        
        st.success(f"""
        ### 🎉 다운로드 완료!
        - **성공**: {results['success']}개
        - **실패**: {results['fail']}개
        - **소요 시간**: {elapsed_time:.1f}초
        - **평균 속도**: {elapsed_time/results['total']:.1f}초/개
        """)
        
        # 실패한 아이템 표시
        if results['fail'] > 0:
            with st.expander("⚠️ 실패한 아이템 목록"):
                for result in results['results']:
                    if not result['success']:
                        st.write(f"- {result['index']}: {result['message']}")

# 다운로드된 이미지 표시
if st.session_state.downloaded_items:
    st.markdown("---")
    st.header("🖼️ 다운로드된 이미지")
    
    # ZIP 다운로드 버튼
    def create_zip():
        """다운로드된 이미지를 ZIP으로 압축"""
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename in os.listdir(download_folder):
                if filename.endswith('.png'):
                    filepath = os.path.join(download_folder, filename)
                    zip_file.write(filepath, filename)
        zip_buffer.seek(0)
        return zip_buffer
    
    if os.path.exists(download_folder):
        image_files = [f for f in os.listdir(download_folder) if f.endswith('.png')]
        
        if image_files:
            st.download_button(
                label="📦 모든 이미지 ZIP으로 다운로드",
                data=create_zip(),
                file_name=f"maple_icons_{int(time.time())}.zip",
                mime="application/zip"
            )
            
            st.markdown("---")
            
            # 이미지 그리드 표시
            cols = st.columns(5)
            for i, filename in enumerate(sorted(image_files)):
                filepath = os.path.join(download_folder, filename)
                try:
                    img = Image.open(filepath)
                    
                    with cols[i % 5]:
                        st.image(img, caption=filename, use_container_width=True)
                        
                        # 개별 다운로드 버튼
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                label="💾",
                                data=f,
                                file_name=filename,
                                mime="image/png",
                                key=f"download_{filename}"
                            )
                except Exception as e:
                    st.error(f"이미지 로드 실패: {filename}")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>메이플스토리 아이템 아이콘 다운로더 v1.0</p>
    <p>문제가 발생하면 서버 URL과 네트워크 연결을 확인해주세요.</p>
</div>
""", unsafe_allow_html=True)
