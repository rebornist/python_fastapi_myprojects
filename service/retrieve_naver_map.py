from lib.naver_map_api import NaverMapAPI


# 네이버 Map API 정보를 불러오는 기능
class RetrieveNaverMap:

    # 주소 정보를 입력받아 JSON으로 반환하는 함수
    def address_based(self, addr):
        return NaverMapAPI().geomecoding(f'query={addr}')

    # 좌표 정보를 입력받아 JSON으로 반환하는 함수
    def coordinate_based(self, x, y):
        return NaverMapAPI().reverse_geomecoding(f'coords={x},{y}')