import time

from fastapi import UploadFile, File

from typing import List
from fastapi import Response
from starlette.responses import FileResponse

from lib.df_converter import DfConverter
from service.retrieve_kakao_map import RetrieveKakaoMap


class GisConvertController:

    def __init__(self, file: UploadFile = File(...)):
        self.file = file
        self.map_api = RetrieveKakaoMap()

    def address_based_method(self):
        # 업로드 된 파일 pandas로 읽기
        # for file in self.files:
        content = self.file.file.read()
        df = DfConverter(file=self.file, content=content)
        print(df.get_content_type())
        new_df = []
        for i, col in df.get_column('adrs_nm').iteritems():

            resp, err = self.map_api.address_based(col)
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

        df2 = df.add_column(['new_adrs_nm', 'rd_adrs_nm', 'adrs_cd', 'bub_cd', 'x', 'y'], new_df)
        output = f'data/[완료]{int(time.time())}_{self.file.filename}'
        if df.get_content_type() == 'text/csv':
            df2.to_csv(output, encoding='euc-kr', index=False)
        elif df.get_content_type() == 'application/vnd.ms-excel' or df.get_content_type() == 'application/haansoftxlsx':
            df2.to_excel(output, encoding='euc-kr', index=False)
        else:
            res = Response(status_code=400)
            return res

        # 파일 다운로드
        return FileResponse(output, media_type='text/csv', filename=output.replace('data/', ''))