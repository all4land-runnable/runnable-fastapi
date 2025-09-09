from textwrap import dedent

from app.routers.temp2.temp2_common_llm import CommonLLM2


class PaceLLM2(CommonLLM2):
    """
    요약:
        대화내역을 기반으로 일기를 생성하는 LLM

    설명:
        SummaryLLM의 반환 값을 토대로 일기를 생성한다.
        일기 내용은 대화 주제(topic)를 기반으로 분리되어 반환된다.

    Attributes:
        _PACE_TEMPLATE(tuple): 대화내역으로 요약된 일기를 생성하기 위한 시스템 프롬프트
        _RESULT_EXAMPLE(tuple): 요약 일기 작성 예시 프롬프트
    """
    _PACE_TEMPLATE = ("system", dedent("""
        <PRIMARY_RULE>
        1. **Return valid JSON only** – no extra text before/after.  
        2. Do **NOT** output explanations, comments or system tags.  
        3. Keys & string values must use straight double-quotes (").
        </PRIMARY_RULE>

        <ROLE>
        * 당신은 제한 거리(limitRange), 짐 무게(luggageWeight), 희망 페이스(paceSeconds), 그리고 각종 구간 정보(slopeDatum)를 통해 각 slopeDatum에 구간 정보의 속도(pace:s/km)을 추가해야합니다.
        * 입력 순서를 유지하고, 항목을 절대 추가/삭제하지 말 것.
        * pace 단위는 초/㎞(s/km)로 한다.
        * pace 허용 범위: [210, 720] s/km (= 3.5–12.0 min/km).
        * 경사 보정(초/㎞):
          - +1% ~ +3%: +6 ~ +18 s/km
          - -1% ~ -3%: -6 ~ -18 s/km
          - ≥ +8%: 추가 감속 상한 +60 s/km
          - ≤ -8%: 가속 상한 -30 s/km
        * 인접 지점 간 pace 변화 절대값 ≤ 48 s/km.
        * pace 값 허용 범위: pace는 [3.5, 12.0] 범위로 제한
        </ROLE>

        <KNOWLEDGE>
        * 맞춤 페이스(pace)를 계산할 때, 짐 무게(luggageWeight), 희망 페이스(paceSeconds), 그리고 각종 구간 정보(list[slopeDatum])들을 통해 계산합니다.
        * 짐 무게(luggageWeight)는 사용자가 들고 달릴 무게이다.
        * 희망 페이스(paceSeconds)는 사용자가 희망하는 평균 페이스이다.
        * 각종 구간정보(list[slopeDatum])는 시작점부터의 거리(meter), 해당 지점의 높이(height), 다음 지점과의 경사도(slope)를 속성으로 갖는다.
        * <INPUT>의 구조는 다음과 같다.
        ```
        {{
          "luggageWeight":float,
          "paceSeconds":int,
          "slopeDatum":[
            {{"meter":float,"height":float,"slope":float}},
            {{"meter":float,"height":float,"slope":float}},
            ... ,
            {{"meter":float,"height":float,"slope":float}}
          ]
        }}
        ```
        </KNOWLEDGE>

        <WRITING_GUIDELINES>
        * 각 slopeDatum에 pace 속성을 추가한다.
        * pace의 값을 계산할 때, luggageWeight, paceSeconds, meter, height, slope를 활용한다.
        * luggageWeight가 높을 수록 pace는 느려진다.
        * 모든 pace의 평균은 paceSeconds와 비슷해야 한다.
        * Each Object:
          - "meter": 기존 이동거리
          - "height": 기존 높이
          - "slope": 기존 경사도
          - "pace": 각종 값을 통해 도출된 결과
        </WRITING_GUIDELINES>

        <OUTPUT_SCHEMA>
        {{
        "result": [
            {{"meter":<이동거리 1>,"height":<해발고도 1>,"slope":<경사도 1>,"pace":<맞춤 페이스 1>}},
            {{"meter":<이동거리 2>,"height":<해발고도 2>,"slope":<경사도 2>,"pace":<맞춤 페이스 2>}},
            {{"meter":<이동거리 3>,"height":<해발고도 3>,"slope":<경사도 3>,"pace":<맞춤 페이스 3>}},
            {{"meter":<이동거리 4>,"height":<해발고도 4>,"slope":<경사도 4>,"pace":<맞춤 페이스 4>}},
            ...
        ]
        }}
        </OUTPUT_SCHEMA>

        <RETURN_EXAMPLE>
       
        Q. <INPUT>{{"limitRange": 5,"luggageWeight": 0,"paceSeconds": 420,"slopeDatum": [{{"meter":50,"height":0.0,"slope":0}},{{"meter":100,"height":0.6,"slope":1}},{{"meter":150,"height":0.1,"slope":-1}},{{"meter":200,"height":0.1,"slope":0}}]}}</INPUT>
        A. {{"result":[{{"meter":50,"height":0.0,"slope":0,"pace":420}},{{"meter":100,"height":0.6,"slope":1,"pace":428}},{{"meter":150,"height":0.1,"slope":-1,"pace":412}},{{"meter":200,"height":0.1,"slope":0,"pace":420}}]}}
        
        Q. <INPUT>{{"limitRange": 5,"luggageWeight": 3,"paceSeconds": 300,"slopeDatum": [{{"meter":50,"height":1.5,"slope":3}},{{"meter":100,"height":4.0,"slope":5}},{{"meter":150,"height":7.5,"slope":7}},{{"meter":200,"height":12.5,"slope":10}}]}}</INPUT>
        A. {{"result":[{{"meter":50,"height":1.5,"slope":3,"pace":318}},{{"meter":100,"height":4.0,"slope":5,"pace":326}},{{"meter":150,"height":7.5,"slope":7,"pace":334}},{{"meter":200,"height":12.5,"slope":10,"pace":346}}]}}
        
        Q. <INPUT>{{"limitRange": 5,"luggageWeight": 6,"paceSeconds": 385,"slopeDatum": [{{"meter":50,"height":1.0,"slope":2}},{{"meter":100,"height":0.0,"slope":-2}},{{"meter":150,"height":2.5,"slope":5}},{{"meter":200,"height":-0.5,"slope":-6}}]}}</INPUT>
        A. {{"result":[{{"meter":50,"height":1.0,"slope":2,"pace":407}},{{"meter":100,"height":0.0,"slope":-2,"pace":387}},{{"meter":150,"height":2.5,"slope":5,"pace":419}},{{"meter":200,"height":-0.5,"slope":-6,"pace":371}}]}}

        Q. <INPUT>{input}</INPUT>
        A.
        """))

    def _add_template(self) ->list[tuple]:
        return [self._PACE_TEMPLATE]

    def invoke(self, parameter:dict)->list[dict]:
        """
        요약:
            대화내역을 바탕으로 일기를 생성하는 함수

        Parameters:
            parameter(dict): parameter는 다음과 같은 key-value를 갖는다.
                - input(str): SummaryLLM()에서 요약된 대화 내역 리스트
        """
        return super().invoke(parameter)