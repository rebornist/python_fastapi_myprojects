import http
import time

from fastapi import UploadFile, File

from typing import List
from fastapi import Response
from starlette.responses import FileResponse

from lib.df_converter import DfConverter
from service.retrieve_kakao_map import RetrieveKakaoMap
from service.retrieve_naver_map import RetrieveNaverMap


class GisConvertController:

    def __init__(self, file: UploadFile = File(...), target: List[str] = ['adrs_nm']):
        self.file = file
        self.target = target
        self.kakao_map_api = RetrieveKakaoMap()
        self.naver_map_api = RetrieveNaverMap()

    def address_based_method(self):
        # 업로드 된 파일 pandas로 읽기
        # for file in self.files:
        content = self.file.file.read()
        df = DfConverter(file=self.file, content=content, encode_type='cp949').set_column_titles()
        new_df = []
        for i, col in df.get_column(self.target[0]).iteritems():

            resp, err = self.kakao_map_api.address_based(col)
            if err is not None:
                continue
            if len(resp['documents']) > 0:
                docs = resp['documents'][0]
                address = docs['address'] if docs else None
                address_nm = address['address_name'] if address else None  # 전체 주소
                admd_cd = address['h_code'] if address_nm else None  # 행정동코드
                bubn_cd = address['b_code'] if address_nm else None  # 법정동코드

                road_address = docs['road_address'] if docs['road_address'] else None
                rd_adrs_nm = road_address['address_name'] if road_address else None  # 전체 도로명 주소

                x = docs['x']  # 경도
                y = docs['y']  # 위도

                new_df.append([address_nm, rd_adrs_nm, admd_cd, bubn_cd, x, y])

            else:
                new_df.append([None, None, None, None, None, None])

        df2 = df.add_column(['지번주소_변환', '도로명주소_변환', '행정동코드', '법정동코드', 'x좌표', 'y좌표'], new_df)
        output = f'data/[완료]{int(time.time())}_{self.file.filename}'
        if df.get_content_type() == 'text/csv':
            df2.to_csv(output, encoding='euc-kr', index=False)
        elif df.get_content_type() == 'application/vnd.ms-excel' or df.get_content_type() == 'application/haansoftxlsx':
            df2.to_excel(output, encoding='euc-kr', index=False)
        else:
            res = Response(status_code=400)
            return res

        headers = {"Content-Type": df.get_content_type()}

        # 파일 다운로드
        return FileResponse(output, filename=output.replace('data/', ''), status_code=http.HTTPStatus.OK, headers=headers)

    def coordinate_based_method(self):
        # 업로드 된 파일 pandas로 읽기
        # for file in self.files:
        content = self.file.file.read()
        df = DfConverter(file=self.file, content=content)
        new_df = []

        for i, k in df.get_content().iteritems():

            print(k.iloc[0])

        # for i, col in df.get_column(self.target).iteritems():
        #
        #
        #     print(type(col))

            # resp, err = self.naver_map_api.coordinate_based(col)
            # if err is not None:
            #     continue
            #
            # if resp is not None:
            #     addr_full_list = []
            #
            #     res_message = resp['status']['message']
            #     addr = resp['results'][0] if res_message else None
            #     addr_code = addr['code']['id'] if addr else None
            #     addr_region = addr['region'] if addr_code else None
            #     addr_si_nm = addr_region['area1']['name'] if addr_region else None
            #     addr_gu_nm = addr_region['area2']['name'] if addr_region else None
            #     addr_dong_nm = addr_region['area3']['name'] if addr_region else None
            #     addr_etc_nm = addr_region['area4']['name'] if addr_region else None
            #     addr_land = addr['land'] if addr else None
            #     addr_land_type = addr_land['type'] if addr_land else None
            #     addr_land_num_1 = addr_land['number1'] if addr_land else None
            #     addr_land_num_2 = addr_land['number2'] if addr_land else None
            #     if addr_si_nm:
            #         addr_full_list.append(addr_si_nm)
            #     if addr_gu_nm:
            #         addr_full_list.append(addr_gu_nm)
            #     if addr_dong_nm:
            #         addr_full_list.append(addr_dong_nm)
            #     if addr_etc_nm:
            #         addr_full_list.append(addr_etc_nm)
            #     if addr_land['type'] != '1':
            #         addr_full_list.append('산')
            #     if addr_land_num_1:
            #         if addr_land_num_2:
            #             addr_full_list.append(f'{addr_land_num_1}-{addr_land_num_2}')
            #         else:
            #             addr_full_list.append(addr_land_num_1)
            #
            # adrs = ' '.join(addr_full_list)
            #
            #     new_df.append([address_nm, rd_adrs_nm, admd_cd, bubn_cd, x, y])
            #
            # else:
            #     new_df.append([None, None, None, None, None, None])

