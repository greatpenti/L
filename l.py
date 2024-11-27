import streamlit as st
import google.generativeai as genai
from pptx import Presentation

def pdf_to_text(uploaded_file):
    try:
        import PyPDF2
        
        # PDF 파일 읽기
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        # 모든 페이지의 텍스트 추출
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
            
        return text_content
        
    except Exception as e:
        st.error(f"PDF 처리 중 오류 발생: {str(e)}")
        return ""

def create_ppt(slides_content):
    # Implementation of create_ppt function
    pass

def main():
    st.title("PDF to PPT Converter with Gemini AI")
    
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file:
            # 진행 상태 표시
            with st.spinner('PDF 텍스트를 추출하는 중...'):
                text_content = pdf_to_text(uploaded_file)
                st.success('PDF 텍스트 추출 완료!')
                # 추출된 텍스트 길이 확인
                st.write(f"추출된 텍스트 길이: {len(text_content)} 문자")
            
            if st.button("PPT 생성하기"):
                try:
                    with st.spinner('Gemini AI로 컨텐츠 생성 중...'):
                        model = genai.GenerativeModel('gemini-pro')
                        
                        # 텍스트가 너무 길 경우 분할 처리
                        if len(text_content) > 10000:
                            st.warning('텍스트가 너무 깁니다. 처음 10000자만 처리합니다.')
                            text_content = text_content[:10000]
                        
                        prompt = f"""
                        다음 텍스트를 PPT 슬라이드 형식으로 구조화해주세요:
                        {text_content}
                        
                        각 슬라이드는 제목과 내용을 포함해야 합니다.
                        결과를 다음과 같은 파이썬 리스트 형식으로 반환해주세요:
                        [
                            {{"title": "슬라이드 제목", "content": "슬라이드 내용"}},
                            {{"title": "다음 슬라이드 제목", "content": "다음 슬라이드 내용"}},
                        ]
                        """
                        
                        response = model.generate_content(prompt)
                        st.success('AI 컨텐츠 생성 완료!')
                        
                        with st.spinner('PPT 생성 중...'):
                            slides_content = eval(response.text)
                            prs = create_ppt(slides_content)
                            output_file = "output.pptx"
                            prs.save(output_file)
                            
                            with open(output_file, "rb") as file:
                                st.download_button(
                                    label="PPT 다운로드",
                                    data=file,
                                    file_name="converted_presentation.pptx",
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")
                    st.error("응답 내용:")
                    st.write(response.text)  # 실제 응답 내용 확인

if __name__ == "__main__":
    main()