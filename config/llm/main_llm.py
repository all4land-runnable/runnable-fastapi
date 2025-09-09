# config/llm/main_llm.py
from textwrap import dedent

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
        <PRIMARY_RULE>
        1. **Return strictly valid JSON only.**
        2. Do **NOT** output any natural-language commentary, markdown, system tags, or explanations.
        </PRIMARY_RULE>

        <ROLE>
        {role}
        </ROLE>

        <GUIDELINES>
        {guidelines}
        </GUIDELINES>

        <OUTPUT_SCHEMA>
        {output_schema}
        </OUTPUT_SCHEMA>

        <SAMPLE_JSON>
        {sample_json}
        </SAMPLE_JSON>

        <RESULT_EXAMPLE>
        {result_example}
        </RESULT_EXAMPLE>

        Q. <INPUT>{input}</INPUT>
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
                ))

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
                - Output JSON only (no extra text).
                - Units: pace = minutes per km (decimal, e.g., 6.2 means 6 min 12 s).
                - Keep input order; NEVER add/remove items.
                - If pace is null, compute it from slope (% grade) and terrain:
                    * Gentle uphill (+1% ~ +3%): slow down by +0.1~+0.3 min/km.
                    * Steep uphill (≥ +8%): cap extra slowdown; avoid explosive values.
                    * Gentle downhill (-1% ~ -3%): speed up by -0.1~-0.3 min/km.
                    * Steep downhill (≤ -8%): limit speed-up (safety braking).
                    * Smooth changes between points (avoid jitter > 0.8 min/km per step).
                - Bounds: clamp pace to [3.5, 12.0].
                - Round to one decimal place.
                - If slope is missing, treat as 0. If height/meter inconsistent, prefer slope for pacing.
            """),
            "output_schema": '{"result":{"slope_datums":[{"meter":number,"height":number,"slope":number,"pace":number}]}}',
            "sample_json":  '{"result":{"slope_datums":[{"meter":50,"height":1,"slope":1,"pace":6.2},{"meter":100,"height":3,"slope":5,"pace":7.1},{"meter":150,"height":0,"slope":-8,"pace":5.6}]}}',
            "result_example":self._RESULT_EXAMPLE
        })

        return super().invoke(parameter)

    def stream(self, parameter: dict, session_id: int = 1):
        """
        - LangChain LCEL의 chain.stream(...)을 직접 사용
        - 공용 세마포(self._semaphore)로 동시 호출 제한
        - 스트리밍 중 코드펜스(````json ... ````)와 <think>...</think>를 제거
        - 최소 수정 원칙: 외부 구조/시그니처 변경 없음
        """
        parameter.update({
            "role": "your my running Pacemaker",
            "guidelines": "takling to informally and using korean",
            "output_schema": '{"result":{"message": {"slope_datums": [{"meter":number, "height":number, "slope":number,"pace":number},{"meter":number, "height":number, "slope":number,"pace":number}]}}',
            "sample_json": '{"result":{"slope_datums": [{"meter":50, "height":1, "slope":1,"pace":6.2},{"meter":100, "height":3, "slope":5,"pace":7.1},{"meter":150, "height":0, "slope":-8,"pace":5.6}]}}',
            "result_example": 'Q.{limitRange: 5, luggageWeight: 4, paceSeconds: 380, slopeDatum:[{"meter":50, "height":1, "slope":1,"pace":null},{"meter":100, "height":3, "slope":5,"pace":null},{"meter":150, "height":0, "slope":-8,"pace":null}]} A. {"result":{"slope_datums": [{"meter":50, "height":1, "slope":1,"pace":6.2},{"meter":100, "height":3, "slope":5,"pace":7.1},{"meter":150, "height":0, "slope":-8,"pace":5.6}]}}'
        })

        inside_think = False  # 스트림 중 <think> 블록 제거용 상태
        with self._semaphore:
            for chunk in self.get_chain().stream(
                    parameter,
                    config={"configurable": {"session_id": session_id}},
            ):
                # chunk가 AIMessageChunk거나 str일 수 있음
                text = getattr(chunk, "content", str(chunk))

                # 코드펜스 마커 제거 (스트림 중간에 끊겨도 누적 무해)
                if "```json" in text or "```" in text:
                    text = text.replace("```json", "").replace("```", "")

                # <think> ... </think> 구간 제거 (스트리밍-safe, 상태 기반)
                out_parts = []
                while text:
                    if not inside_think:
                        start = text.find("<think>")
                        end = text.find("</think>")
                        if start != -1 and (end == -1 or start < end):
                            out_parts.append(text[:start])
                            text = text[start + len("<think>"):]
                            inside_think = True
                        else:
                            if end != -1:
                                out_parts.append(text[:end])
                                text = text[end + len("</think>"):]
                            else:
                                out_parts.append(text)
                                text = ""
                    else:
                        end = text.find("</think>")
                        if end == -1:
                            # 닫는 태그가 다음 청크에 올 것: 이번 청크는 버림
                            text = ""
                        else:
                            text = text[end + len("</think>"):]
                            inside_think = False

                cleaned = "".join(out_parts).strip()
                if cleaned:
                    yield cleaned

    _RESULT_EXAMPLE = dedent("""
        Q. <INPUT>{
          "limitRange": 5,
          "luggageWeight": 0,
          "paceSeconds": 360,
          "slopeDatum": [
            {"meter":50,"height":0.0,"slope":0,"pace":null},
            {"meter":100,"height":0.6,"slope":1,"pace":null},
            {"meter":150,"height":0.1,"slope":-1,"pace":null},
            {"meter":200,"height":0.1,"slope":0,"pace":null}
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
            {"meter":50,"height":1.5,"slope":3,"pace":null},
            {"meter":100,"height":4.0,"slope":5,"pace":null},
            {"meter":150,"height":7.5,"slope":7,"pace":null},
            {"meter":200,"height":12.5,"slope":10,"pace":null}
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
            {"meter":50,"height":1.0,"slope":2,"pace":null},
            {"meter":100,"height":0.0,"slope":-2,"pace":null},
            {"meter":150,"height":2.5,"slope":5,"pace":null},
            {"meter":200,"height":-0.5,"slope":-6,"pace":null}
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
            {"meter":50,"height":0.5,"slope":1,"pace":null},
            {"meter":100,"height":-3.5,"slope":-8,"pace":null},
            {"meter":150,"height":-8.5,"slope":-10,"pace":null},
            {"meter":200,"height":-9.5,"slope":-2,"pace":null}
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
            {"meter":50,"height":1.0,"slope":2,"pace":null},
            {"meter":100,"height":4.5,"slope":7,"pace":null},
            {"meter":150,"height":10.5,"slope":12,"pace":null},
            {"meter":200,"height":11.5,"slope":2,"pace":null}
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
            {"meter":50,"height":0.5,"slope":1,"pace":null},
            {"meter":100,"height":3.0,"slope":5,"pace":null},
            {"meter":150,"height":2.0,"slope":-2,"pace":null},
            {"meter":200,"height":5.0,"slope":6,"pace":null}
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
            {"meter":200,"height":1.0,"slope":0.5,"pace":null},
            {"meter":400,"height":3.0,"slope":1.0,"pace":null},
            {"meter":600,"height":5.0,"slope":1.0,"pace":null},
            {"meter":800,"height":4.0,"slope":-0.5,"pace":null},
            {"meter":1000,"height":3.0,"slope":-0.5,"pace":null}
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
            {"meter":50,"height":-2.0,"slope":-4,"pace":null},
            {"meter":100,"height":-4.5,"slope":-5,"pace":null},
            {"meter":150,"height":-5.0,"slope":-1,"pace":null},
            {"meter":200,"height":-5.0,"slope":0,"pace":null}
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
            {"meter":50,"height":1.0,"slope":4,"pace":null},
            {"meter":100,"height":3.5,"slope":8,"pace":null},
            {"meter":150,"height":7.0,"slope":12,"pace":null},
            {"meter":200,"height":7.0,"slope":0,"pace":null}
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
            {"meter":50,"height":0.2,"slope":1,"pace":null},
            {"meter":100,"height":-0.1,"slope":-1,"pace":null},
            {"meter":150,"height":0.3,"slope":2,"pace":null},
            {"meter":200,"height":-0.2,"slope":-2,"pace":null},
            {"meter":250,"height":0.1,"slope":1,"pace":null}
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
            {"meter":50,"height":-3.0,"slope":-9,"pace":null},
            {"meter":100,"height":-6.5,"slope":-11,"pace":null},
            {"meter":150,"height":-6.0,"slope":2,"pace":null},
            {"meter":200,"height":-6.0,"slope":0,"pace":null}
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
            {"meter":50,"height":0.0,"slope":0,"pace":null},
            {"meter":100,"height":0.0,"slope":0,"pace":null},
            {"meter":150,"height":0.0,"slope":0,"pace":null},
            {"meter":200,"height":0.0,"slope":0,"pace":null}
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
            {"meter":50,"height":1.0,"slope":2,"pace":null},
            {"meter":100,"height":3.0,"slope":3,"pace":null},
            {"meter":150,"height":5.5,"slope":4,"pace":null},
            {"meter":200,"height":8.5,"slope":5,"pace":null}
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
            {"meter":200,"height":-1.0,"slope":-1.0,"pace":null},
            {"meter":400,"height":-3.0,"slope":-1.0,"pace":null},
            {"meter":600,"height":-5.5,"slope":-1.25,"pace":null},
            {"meter":800,"height":-7.0,"slope":-0.75,"pace":null},
            {"meter":1000,"height":-7.5,"slope":-0.25,"pace":null}
          ]
        }</INPUT>
        A. {"result":{"slope_datums":[
          {"meter":200,"height":-1.0,"slope":-1.0,"pace":5.9},
          {"meter":400,"height":-3.0,"slope":-1.0,"pace":5.8},
          {"meter":600,"height":-5.5,"slope":-1.25,"pace":5.7},
          {"meter":800,"height":-7.0,"slope":-0.75,"pace":5.8},
          {"meter":1000,"height":-7.5,"slope":-0.25,"pace":5.9}
        ]}}""")

main_llm = MainLLM()