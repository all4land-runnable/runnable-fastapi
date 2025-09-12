from textwrap import dedent

from config.common.common_llm import CommonLLM


class PaceMakerLLM(CommonLLM):
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
        * 당신은 짐 무게(luggageWeight), 희망 페이스(paceSeconds), 시작 지점명(startPlace), 그리고 경로 정보(sections)를 통해 각 slopeDatum에 구간 정보의 속도(pace:s/km)을 추가해야 한다.
        * 입력 순서를 유지하고, 항목을 절대 추가/삭제하지 말 것.
        * pace 단위는 초/㎞(s/km)로 한다.
        * pace 값 허용 범위: [210, 720] s/km 로 제한
        * 경사 보정(초/㎞):
            - +1% ~ +3%: +6 ~ +18 s/km (선형)
            - -1% ~ -3%: -6 ~ -18 s/km (선형)
            - +3% 초과 +8% 미만: +18에서 +60까지 선형 증가
            - -3% 초과 -8% 미만: -18에서 -30까지 선형 감소
            - ≥ +8%: +60 상한
            - ≤ -8%: -30 상한
        * pace 값 허용 범위: pace는 [3.5, 12.0] 범위로 제한
        </ROLE>

        <KNOWLEDGE>
        * 맞춤 페이스(pace)를 계산할 때, 짐 무게(luggageWeight), 희망 페이스(paceSeconds), 그리고 각종 구간 정보(sections[distance, slope])들을 통해 계산합니다.
        * 짐 무게(luggageWeight)는 사용자가 들고 달릴 무게이다.
        * 희망 페이스(paceSeconds)는 사용자가 희망하는 평균 페이스이다.
        * 각종 구간정보(sections[distance, slope, startPlace])는 시작점부터의 거리(distance), 다음 지점까지의 경사도(slope), 시작 지점의 이름(startPlace)를 속성으로 갖는다.
        * <INPUT>의 구조는 다음과 같다.
        ```
        {{
            "luggageWeight":float,
            "paceSeconds":int,
            "sections": [
                {{"distance":float,"slope":float,"startPlace":str}},
                {{"distance":float,"slope":float,"startPlace":str}},
                ... ,
                {{"distance":float,"slope":float,"startPlace":str}}
            ]
        }}
        ```
        </KNOWLEDGE>

        <WRITING_GUIDELINES>
        * 각 section에 맞는 구간속도 리스트(list[{{distance:float, pace:float, strategies:str}}])를 제공한다.
        * pace의 값을 계산할 때, luggageWeight, paceSeconds, meter, slope를 활용한다.
        * luggageWeight가 높을 수록 pace는 느려진다.
        * 모든 pace의 평균은 paceSeconds와 비슷해야 한다.
        * strategies를 작성할 때, luggageWeight, paceSeconds, meter, slope, startPlace를 활용한다.
        * strategies를 작성할 때, 한 문장을 작성한 후, 줄바꿈을 진행한다.
        * Each Object:
          - "distance":float 시작점에서의 이동거리(Section.distance와 동일)
          - "pace":float 각종 값을 통해 도출된 결과
          - "strategies":list[str] 각종 정보를 통해 도출된 구간별 러닝 전략들
        </WRITING_GUIDELINES>

        <OUTPUT_SCHEMA>
        {{
        "result": [
            {{"distance":<이동거리 1>,"pace":<맞춤 페이스 1>, "strategies":[<맞춤 전략 1-1>, <맞춤 전략 1-2>]}},
            {{"distance":<이동거리 2>,"pace":<맞춤 페이스 2>, "strategies":[<맞춤 전략 2-1>, <맞춤 전략 2-2>, <맞춤 전략 2-3>, <맞춤 전략 2-4>]}},
            {{"distance":<이동거리 3>,"pace":<맞춤 페이스 3>, "strategies":[<맞춤 전략 3-1>, <맞춤 전략 3-2>]}},
            {{"distance":<이동거리 4>,"pace":<맞춤 페이스 4>, "strategies":[<맞춤 전략 4-1>, <맞춤 전략 4-2>, <맞춤 전략 1-3>]}},
            ...
        ]
        }}
        </OUTPUT_SCHEMA>

        <RETURN_EXAMPLE>
        Q. <INPUT>{{"luggageWeight": 0, "paceSeconds": 420, "sections": [{{"distance":50,"slope":0, "startPlace":"여의공원로를 따라 349m 이동"}},{{"distance":100,"slope":1, "startPlace":"은행로, 6m"}},{{"distance":150,"slope":-1, "startPlace": "국회의사당역  1번출구"}},{{"distance":200,"slope":0, "startPlace": "국회의사당"}}]}}</INPUT>        
        A. {{"result":[{{"distance":50,"pace":420,"strategies":["여의공원로를 따라 349m 이동 구간은 평지입니다. 7’00’’ 페이스를 유지하세요!"]}},{{"distance":100,"pace":428,"strategies":["은행로 6m 구간은 완만한 오르막입니다. 7’08’’ 페이스를 유지하세요!"]}},{{"distance":150,"pace":412,"strategies":["국회의사당역 1번출구 구간은 완만한 내리막입니다. 6’52’’ 페이스를 유지해주세요!"]}},{{"distance":200,"pace":420,"strategies":["국회의사당 인근은 평지이며 목적지에 거의 다 도착했습니다. 7’00’’ 페이스를 유지하세요!"]}}]}}

        Q. <INPUT>{{"luggageWeight": 3, "paceSeconds": 300, "sections": [{{"distance":50,"slope":3, "startPlace": "어드롭렛인카페"}},{{"distance":100,"slope":5, "startPlace": "용두동홍쭈꾸미"}},{{"distance":150,"slope":7, "startPlace": "좌회전 후 141m 이동"}},{{"distance":200,"slope":10, "startPlace": "나물먹는곰"}}]}}</INPUT>
        A. {{"result":[{{"distance":50,"pace":318,"strategies":["어드롭렛인카페 앞 오르막 시작 구간입니다. 보폭을 줄이고 5’18’’ 페이스를 유지하세요!"]}},{{"distance":100,"pace":326,"strategies":["용두동홍쭈꾸미 방향 가파른 오르막입니다. 팔 치기를 적극적으로 사용하며 5’26’’ 페이스를 유지하세요!"]}},{{"distance":150,"pace":334,"strategies":["좌회전 후 141m 이동 구간은 더 가파른 오르막입니다. 호흡을 일정하게 유지하며 5’34’’ 페이스로 가세요!"]}},{{"distance":200,"pace":346,"strategies":["나물먹는곰까지 매우 가파른 경사입니다. 과도한 무릎 굴곡을 피하고 5’46’’ 페이스를 유지하세요!"]}}]}}

        Q. <INPUT>{{"luggageWeight": 6, "paceSeconds": 385, "sections": [{{"distance":50,"slope":2, "startPlace": "신길광장공원앞"}},{{"distance":100,"slope":-2, "startPlace": "보행자도로, 24m"}},{{"distance":150,"slope":5, "startPlace": "우신떡방앗간"}},{{"distance":200,"slope":-6, "startPlace": "신길로, 192m"}}]}}</INPUT>
        A. {{"result":[{{"distance":50,"pace":407,"strategies":["신길광장공원앞 구간은 완만한 오르막이며 짐 6kg의 영향이 있습니다. 6’47’’ 페이스를 유지하세요!"]}},{{"distance":100,"pace":387,"strategies":["보행자도로, 24m 구간은 완만한 내리막입니다. 과속을 피하고 6’27’’ 페이스를 유지하세요!"]}},{{"distance":150,"pace":419,"strategies":["우신떡방앗간 앞은 가파른 오르막입니다. 보폭을 줄이고 상체를 약간 세워 6’59’’ 페이스를 유지하세요!"]}},{{"distance":200,"pace":371,"strategies":["신길로, 192m 구간은 가파른 내리막입니다. 착지 충격을 줄이며 6’11’’ 페이스를 유지하세요!"]}}]}}
        </RETURN_EXAMPLE>

        Q. <INPUT>{input}</INPUT>
        A."""))

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