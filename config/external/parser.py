from json import JSONDecodeError

from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET
from requests import Response

from app.internal.log.log import log


def parse_json(response:Response, title:str):
    """
    요약:
        API로 반환된 JSON을 객체로 파싱하고, 에러를 분석하는 함수

    Parameters:
        response(Response): API의 반환 결과
        title(str): 에러 발생 시 나타날 문구
    """
    try:
        result = response.json()
        if result["code"] != 200:
            # LOG. 시연용 로그
            log.exception(msg=f"\n\nExternal API Error [{title}]\n{result["message"]}\n")
        return result["data"]
    except JSONDecodeError:
        # LOG. 시연용 로그
        log.exception(msg=f"\n\nExternal API Error [{title}]\n{response}\n")
    except KeyError:
        # LOG. 시연용 로그
        log.exception(msg=f"\n\nExternal API Error [{title}]\n{response}\n")

def parse_xml(response: Response, title: str):
    """
    요약:
        공공데이터포털 스타일 XML을 파싱하고, 에러를 분석/로그하는 함수.
        성공 시 {'items': [...], 'meta': {...}} 형태를 반환.

    반환 예:
        {
          'items': [ {'yadmNm': '병원명', 'addr': '주소', ...}, ... ],
          'meta':  {'pageNo': 1, 'numOfRows': 10, 'totalCount': 123}
        }
    """
    def _to_int(x: Optional[str]) -> Optional[int]:
        try:
            return int(x) if x is not None and x.strip() != "" else None
        except ValueError:
            return None

    try:
        xml_bytes = response.content or b""
        root = ET.fromstring(xml_bytes)

        # 네임스페이스 제거(있어도 태그명을 단순화해 접근 가능하게)
        for el in root.iter():
            if "}" in el.tag:
                el.tag = el.tag.split("}", 1)[1]

        # 공통 헤더(성공 코드 확인)
        # - 보통 resultCode == '00' 이면 성공
        result_code = (root.findtext("header/resultCode") or root.findtext("resultCode") or "").strip()
        result_msg  = (root.findtext("header/resultMsg")  or root.findtext("resultMsg")  or "").strip()

        # items 추출: response/body/items/item  또는 바로 items/item
        items_parent = root.find("body/items") or root.find("items")
        items: List[Dict[str, Any]] = []
        if items_parent is not None:
            for item in items_parent.findall("item"):
                row: Dict[str, Any] = {}
                for child in list(item):
                    row[child.tag] = (child.text or "").strip()
                items.append(row)

        # 메타 정보(있을 때만 채움)
        meta = {
            "pageNo":     _to_int(root.findtext("body/pageNo")     or root.findtext("pageNo")),
            "numOfRows":  _to_int(root.findtext("body/numOfRows")  or root.findtext("numOfRows")),
            "totalCount": _to_int(root.findtext("body/totalCount") or root.findtext("totalCount")),
        }

        # 에러 코드 처리: '00' 외 값, 또는 숫자 '200'만 성공으로 간주(서비스별 편차 대응)
        if result_code and result_code not in ("00", "SUCCESS", "200"):
            log.exception(msg=f"\n\nExternal API Error [{title}]\ncode={result_code} msg={result_msg}\n")
            # 실패여도 호출부에서 참고할 수 있게 원본 형태 반환(필요 시 None으로 바꿔도 됩니다)
            return {"items": items, "meta": meta, "error": {"code": result_code, "message": result_msg}}

        return {"items": items, "meta": meta}

    except ET.ParseError:
        log.exception(msg=f"\n\nExternal API Error [{title}]\n(XML ParseError)\n{response.text}\n")
    except Exception as e:
        log.exception(msg=f"\n\nExternal API Error [{title}]\n{e}\n")
