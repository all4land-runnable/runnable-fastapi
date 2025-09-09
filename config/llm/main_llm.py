# config/llm/main_llm.py
from textwrap import dedent

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config.common.common_llm import CommonLLM
from config.common.singleton import Singleton


class MainLLM(CommonLLM, metaclass=Singleton):
    """
    요약:
        Persona 수정 사항을 생성하는 LLM

    설명:
        대화 내역을 바탕으로 사용자의 페르소나를 재구성한다.

    Attributes:
        _MAIN_TEMPLATE(tuple): 시스템 프롬프트
        _RESULT_EXAMPLE(tuple): 예시 프롬프트
    """

    _MAIN_TEMPLATE = ("system", dedent("""
        기본 규칙(PRIMARY_RULE):
        1. **반드시 유효한 JSON만 반환하세요.**
        2. 자연어 해설, 마크다운, 시스템 태그, 추가 설명을 **절대 출력하지 마세요.**

        역할(ROLE):
        {role}

        지침(GUIDELINES):
        {guidelines}

        출력 스키마(OUTPUT_SCHEMA):
        {output_schema}

        결과 예시(RESULT_EXAMPLE):
        {result_example}

        Q. {input}
        A.
        """))

    _chain = None

    def __init__(self):
        _template = [
            super()._COMMON_COMMAND_TEMPLATE,
            # 상속받은 자식 클래스에서 추가적으로 Template를 추가할 수 있도록 TemplatePattern을 적용
            *self._add_template()
        ]
        self._chain = (ChatPromptTemplate.from_messages(_template)
                       | super()._common_model.bind(
                    format="json",
                    stop=["\nQ.","</RESULT_EXAMPLE>","</SAMPLE_JSON>"]
                )| StrOutputParser())

    def get_chain(self):
        return self._chain

    def _add_template(self)->list[tuple]:
        return [self._MAIN_TEMPLATE]

    def invoke(self, parameter:dict)->dict:
        """
        요약:
            사용자의 대화기록으로 페르소나를 수정하는 함수

        Parameters:
            parameter(dict): parameter는 다음과 같은 key-value를 갖는다.
                - session_history(list[str]): FastAPI가 실행된 후, 채팅방의 전체 대화 내역
                - current_persona(dict): 대화 내역 본인의 에고 페르소나

        Raises:
            JSONDecodeError: JSON Decoding 실패 시, 빈 딕셔너리 반환
        """
        parameter.update({
            "role": "your my running Pacemaker",
            "guidelines": dedent("""
                - 당신은 제한 거리(limitRange), 짐 무게(luggageWeight), 희망 페이스(paceSeconds), 그리고 각종 구간 정보(slopeDatum)를 통해 각 slopeDatum에 구간 정보의 속도(pace:s/km)을 추가해야합니다.
                - 출력은 JSON만(추가 텍스트 금지).
                - 단위: pace = 분/킬로미터(소수, 예: 6.2는 6분 12초).
                - 입력 순서를 유지하고, 항목을 절대 추가/삭제하지 말 것.
                - pace가 없으면 경사(% 기울기)와 지형을 기반으로 계산:
                    * 완만한 오르막(+1% ~ +3%): +0.1~+0.3 분/㎞ 느리게.
                    * 가파른 오르막(≥ +8%): 추가 감속을 상한 처리(폭증 금지).
                    * 완만한 내리막(-1% ~ -3%): -0.1~-0.3 분/㎞ 빠르게.
                    * 급한 내리막(≤ -8%): 과도한 가속 제한(안전 감속).
                    * 구간 간 변화는 부드럽게(스텝당 0.8분/㎞ 초과 요동 금지).
                - 경계: pace는 [3.5, 12.0] 범위로 클램프.
                - 소수 첫째 자리까지 반올림.
                - slope가 없으면 0으로 간주. height/meter와 불일치 시 pace 계산에는 slope를 우선.
            """),
            # 예시 JSON(영어 유지)
            "output_schema": '{"result":{"slope_datums":[{"meter":number,"height":number,"slope":number,"pace":number},...]}}',
            "result_example":self._RESULT_EXAMPLE
        })

        return super().invoke(parameter)

    _RESULT_EXAMPLE = dedent("""
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 0,
          "paceSeconds": 360,
          "slopeDatum": [
            {"meter":50,"height":0.0,"slope":0},
            {"meter":100,"height":0.6,"slope":1},
            {"meter":150,"height":0.1,"slope":-1},
            {"meter":200,"height":0.1,"slope":0}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":0.0,"slope":0,"pace":6.0},
          {"meter":100,"height":0.6,"slope":1,"pace":6.2},
          {"meter":150,"height":0.1,"slope":-1,"pace":5.8},
          {"meter":200,"height":0.1,"slope":0,"pace":6.0}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 4,
          "paceSeconds": 380,
          "slopeDatum": [
            {"meter":50,"height":1.5,"slope":3},
            {"meter":100,"height":4.0,"slope":5},
            {"meter":150,"height":7.5,"slope":7},
            {"meter":200,"height":12.5,"slope":10}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":1.5,"slope":3,"pace":6.6},
          {"meter":100,"height":4.0,"slope":5,"pace":7.2},
          {"meter":150,"height":7.5,"slope":7,"pace":7.7},
          {"meter":200,"height":12.5,"slope":10,"pace":8.4}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 6,
          "paceSeconds": 385,
          "slopeDatum": [
            {"meter":50,"height":1.0,"slope":2},
            {"meter":100,"height":0.0,"slope":-2},
            {"meter":150,"height":2.5,"slope":5},
            {"meter":200,"height":-0.5,"slope":-6}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":1.0,"slope":2,"pace":6.4},
          {"meter":100,"height":0.0,"slope":-2,"pace":5.7},
          {"meter":150,"height":2.5,"slope":5,"pace":7.1},
          {"meter":200,"height":-0.5,"slope":-6,"pace":5.5}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 2,
          "paceSeconds": 370,
          "slopeDatum": [
            {"meter":50,"height":0.5,"slope":1},
            {"meter":100,"height":-3.5,"slope":-8},
            {"meter":150,"height":-8.5,"slope":-10},
            {"meter":200,"height":-9.5,"slope":-2}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":0.5,"slope":1,"pace":6.2},
          {"meter":100,"height":-3.5,"slope":-8,"pace":5.6},
          {"meter":150,"height":-8.5,"slope":-10,"pace":5.7},
          {"meter":200,"height":-9.5,"slope":-2,"pace":5.8}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 3,
          "paceSeconds": 390,
          "slopeDatum": [
            {"meter":50,"height":1.0,"slope":2},
            {"meter":100,"height":4.5,"slope":7},
            {"meter":150,"height":10.5,"slope":12},
            {"meter":200,"height":11.5,"slope":2}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":1.0,"slope":2,"pace":6.4},
          {"meter":100,"height":4.5,"slope":7,"pace":7.6},
          {"meter":150,"height":10.5,"slope":12,"pace":8.8},
          {"meter":200,"height":11.5,"slope":2,"pace":6.5}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 1,
          "paceSeconds": 370,
          "slopeDatum": [
            {"meter":50,"height":0.5,"slope":1},
            {"meter":100,"height":3.0,"slope":5},
            {"meter":150,"height":2.0,"slope":-2},
            {"meter":200,"height":5.0,"slope":6}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":0.5,"slope":1,"pace":6.2},
          {"meter":100,"height":3.0,"slope":5,"pace":7.1},
          {"meter":150,"height":2.0,"slope":-2,"pace":5.7},
          {"meter":200,"height":5.0,"slope":6,"pace":7.3}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 0,
          "paceSeconds": 360,
          "slopeDatum": [
            {"meter":200,"height":1.0,"slope":0.5},
            {"meter":400,"height":3.0,"slope":1.0},
            {"meter":600,"height":5.0,"slope":1.0},
            {"meter":800,"height":4.0,"slope":-0.5},
            {"meter":1000,"height":3.0,"slope":-0.5}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":200,"height":1.0,"slope":0.5,"pace":6.1},
          {"meter":400,"height":3.0,"slope":1.0,"pace":6.2},
          {"meter":600,"height":5.0,"slope":1.0,"pace":6.2},
          {"meter":800,"height":4.0,"slope":-0.5,"pace":5.9},
          {"meter":1000,"height":3.0,"slope":-0.5,"pace":5.9}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 2,
          "paceSeconds": 360,
          "slopeDatum": [
            {"meter":50,"height":-2.0,"slope":-4},
            {"meter":100,"height":-4.5,"slope":-5},
            {"meter":150,"height":-5.0,"slope":-1},
            {"meter":200,"height":-5.0,"slope":0}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":-2.0,"slope":-4,"pace":5.6},
          {"meter":100,"height":-4.5,"slope":-5,"pace":5.5},
          {"meter":150,"height":-5.0,"slope":-1,"pace":5.9},
          {"meter":200,"height":-5.0,"slope":0,"pace":6.0}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 3,
          "paceSeconds": 370,
          "slopeDatum": [
            {"meter":50,"height":1.0,"slope":4},
            {"meter":100,"height":3.5,"slope":8},
            {"meter":150,"height":7.0,"slope":12},
            {"meter":200,"height":7.0,"slope":0}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":1.0,"slope":4,"pace":6.8},
          {"meter":100,"height":3.5,"slope":8,"pace":7.9},
          {"meter":150,"height":7.0,"slope":12,"pace":8.9},
          {"meter":200,"height":7.0,"slope":0,"pace":6.3}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 1,
          "paceSeconds": 365,
          "slopeDatum": [
            {"meter":50,"height":0.2,"slope":1},
            {"meter":100,"height":-0.1,"slope":-1},
            {"meter":150,"height":0.3,"slope":2},
            {"meter":200,"height":-0.2,"slope":-2},
            {"meter":250,"height":0.1,"slope":1}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":0.2,"slope":1,"pace":6.2},
          {"meter":100,"height":-0.1,"slope":-1,"pace":5.9},
          {"meter":150,"height":0.3,"slope":2,"pace":6.3},
          {"meter":200,"height":-0.2,"slope":-2,"pace":5.8},
          {"meter":250,"height":0.1,"slope":1,"pace":6.2}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 0,
          "paceSeconds": 360,
          "slopeDatum": [
            {"meter":50,"height":-3.0,"slope":-9},
            {"meter":100,"height":-6.5,"slope":-11},
            {"meter":150,"height":-6.0,"slope":2},
            {"meter":200,"height":-6.0,"slope":0}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":-3.0,"slope":-9,"pace":5.6},
          {"meter":100,"height":-6.5,"slope":-11,"pace":5.7},
          {"meter":150,"height":-6.0,"slope":2,"pace":6.3},
          {"meter":200,"height":-6.0,"slope":0,"pace":6.0}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 0,
          "paceSeconds": 355,
          "slopeDatum": [
            {"meter":50,"height":0.0,"slope":0},
            {"meter":100,"height":0.0,"slope":0},
            {"meter":150,"height":0.0,"slope":0},
            {"meter":200,"height":0.0,"slope":0}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":0.0,"slope":0,"pace":5.9},
          {"meter":100,"height":0.0,"slope":0,"pace":5.9},
          {"meter":150,"height":0.0,"slope":0,"pace":5.9},
          {"meter":200,"height":0.0,"slope":0,"pace":5.9}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 8,
          "paceSeconds": 390,
          "slopeDatum": [
            {"meter":50,"height":1.0,"slope":2},
            {"meter":100,"height":3.0,"slope":3},
            {"meter":150,"height":5.5,"slope":4},
            {"meter":200,"height":8.5,"slope":5}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":50,"height":1.0,"slope":2,"pace":6.6},
          {"meter":100,"height":3.0,"slope":3,"pace":6.9},
          {"meter":150,"height":5.5,"slope":4,"pace":7.2},
          {"meter":200,"height":8.5,"slope":5,"pace":7.5}
        ]}}
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 1,
          "paceSeconds": 365,
          "slopeDatum": [
            {"meter":200,"height":-1.0,"slope":-1.0},
            {"meter":400,"height":-3.0,"slope":-1.0},
            {"meter":600,"height":-5.5,"slope":-1.25},
            {"meter":800,"height":-7.0,"slope":-0.75},
            {"meter":1000,"height":-7.5,"slope":-0.25}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":200,"height":-1.0,"slope":-1.0,"pace":5.9},
          {"meter":400,"height":-3.0,"slope":-1.0,"pace":5.8},
          {"meter":600,"height":-5.5,"slope":-1.25,"pace":5.7},
          {"meter":800,"height":-7.0,"slope":-0.75,"pace":5.8},
          {"meter":1000,"height":-7.5,"slope":-0.25,"pace":5.9}
        ]}}""")