from lib.kakao_map_api import KaKaoMapAPI


# 카카오 Map API 정보를 불러오는 기능
class RetrieveKakaoMap:

    # 주소 정보를 입력받아 JSON으로 반환하는 함수
    def address_based(self, addr):
        return KaKaoMapAPI().search_address(f'query={addr}')
