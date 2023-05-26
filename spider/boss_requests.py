import requests
import pandas as pd
import json
import time
import random

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

session = requests.session()

def get_token():
    url = "https://www.zhipin.com/wapi/zppassport/get/zpToken"
    headers = {
        "user-agent": USER_AGENT,
        "cookie": "wd_guid=01a8dbd7-5ebb-40b5-9c8e-2c242e2a9127; historyState=state; _9755xjdesxxd_=32; YD00951578218230%3AWM_TID=DwZ9BHIW5OJEBQRURAKRXj7lwsOs2JYf; lastCity=101010100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1683525769; _bl_uid=nklq8hdve88fwwsjyjnOjew7Cn2X; gdxidpyhxdE=J8qm6%2BBdEg%5CGSbBXGMudK7z6Ljx%2FvnNTJZpAyS7BTgDS%5CQci7xMyceV03phie3wZGtNj1m7Ix8sy17hqS15UsGeD5iUN%2BOw6g0oGS6cXbTKgb6lqVlaIO6nBwUcpLIkxokkXHh6w1qhKk0UpKP5sRtuoaeZ7b7ODOer4I5ridTiGcNrg%3A1683795358326; YD00951578218230%3AWM_NI=fRuGY4qtxzyjrD81hY5xNWHk5PxJsjZq2f6IDxCYGRuKHCtoeelETmkSVUR0BxZZdpy6bkH0MqwBYenliWNAh1a23eawX8CxYxU082z2vxkwdxejvTwUrHMzMCgTQsnkdWo%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed2ec59a9e9858ed040bae78ea2c44e839a9f86d13b869d8cccf244969cfda5ed2af0fea7c3b92aa68ebba8dc40b3acb89bfc62b29cf8d2eb53f7a882b8cb61f790b8abf2629aaffe87b54388a88dbac65ab79588a4f765a7bba4a6d767a98d9ab6d13c82a896bbe77cbbeaae8ccb3c8fafb9a3dc6faeb4a7b8cd4bacefafd3b26fa3a998d9c2749ba89bd1bb3abaeeba99ea7da8a8ab8bf560b58bbea9d0728f9da9b5d479aeb5acb8ee37e2a3; wt2=DSn_5RgchyYGe5UGkCojZFaPSbDsjNBq_uthMJ2du2Y-b5i9P5cZegrySQqXD7px2CSidVqvzGuPZj-UEu_usfw~~; wbg=0; __zp_seo_uuid__=536c6a61-74af-4f1b-aec1-f5dcd25a8c0d; __g=-; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1684135295; __zp_stoken__=8d86eaQJICQcXP0J4O102BG1yLSpRLQYRbGxGOCkJUBwEOC11BXsMFnVwd3QnT1QFWmNWdUt7XwZhLi1ddy1cE3J2BTltJ3UyYmURElQfJQViBEowdw9sNhcVCR5UKgMWGFpkDkRbfGQ2NCw%3D; __c=1683525769; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dj4w1ZktGT3Zqn_NCvE9bcP7_Au-uUtOOhLEmrxY7ynU9mmVTlkmaIeKqJgLIAJ23%26wd%3D%26eqid%3Dcde58f4b000216a0000000026461dd2c&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%25E6%2595%25B0%25E6%258D%25AE%25E4%25BB%2593%25E5%25BA%2593%26city%3D101010100&s=3&g=&friend_source=0&s=3&friend_source=0; __a=10008462.1582085594.1664242401.1683525769.49.3.28.49",
    }
    
    response = session.get(url=url, headers=headers)
    print(response.url)

    result = json.loads(response.text)
    print(result)
    token = result["zpData"]["token"]
    return token


def get_job_list(key_word, page=1, page_size=30):
    # url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=%E6%95%B0%E6%8D%AE%E4%BB%93%E5%BA%93&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=1&pageSize=30"
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway="

    headers = {
        "user-agent": USER_AGENT,
        "cookie": "wd_guid=01a8dbd7-5ebb-40b5-9c8e-2c242e2a9127; historyState=state; _9755xjdesxxd_=32; YD00951578218230%3AWM_TID=DwZ9BHIW5OJEBQRURAKRXj7lwsOs2JYf; lastCity=101010100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1683525769; _bl_uid=nklq8hdve88fwwsjyjnOjew7Cn2X; gdxidpyhxdE=J8qm6%2BBdEg%5CGSbBXGMudK7z6Ljx%2FvnNTJZpAyS7BTgDS%5CQci7xMyceV03phie3wZGtNj1m7Ix8sy17hqS15UsGeD5iUN%2BOw6g0oGS6cXbTKgb6lqVlaIO6nBwUcpLIkxokkXHh6w1qhKk0UpKP5sRtuoaeZ7b7ODOer4I5ridTiGcNrg%3A1683795358326; YD00951578218230%3AWM_NI=fRuGY4qtxzyjrD81hY5xNWHk5PxJsjZq2f6IDxCYGRuKHCtoeelETmkSVUR0BxZZdpy6bkH0MqwBYenliWNAh1a23eawX8CxYxU082z2vxkwdxejvTwUrHMzMCgTQsnkdWo%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed2ec59a9e9858ed040bae78ea2c44e839a9f86d13b869d8cccf244969cfda5ed2af0fea7c3b92aa68ebba8dc40b3acb89bfc62b29cf8d2eb53f7a882b8cb61f790b8abf2629aaffe87b54388a88dbac65ab79588a4f765a7bba4a6d767a98d9ab6d13c82a896bbe77cbbeaae8ccb3c8fafb9a3dc6faeb4a7b8cd4bacefafd3b26fa3a998d9c2749ba89bd1bb3abaeeba99ea7da8a8ab8bf560b58bbea9d0728f9da9b5d479aeb5acb8ee37e2a3; wt2=DSn_5RgchyYGe5UGkCojZFaPSbDsjNBq_uthMJ2du2Y-b5i9P5cZegrySQqXD7px2CSidVqvzGuPZj-UEu_usfw~~; wbg=0; __zp_seo_uuid__=536c6a61-74af-4f1b-aec1-f5dcd25a8c0d; __g=-; collection_pop_window=1; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dj4w1ZktGT3Zqn_NCvE9bcP7_Au-uUtOOhLEmrxY7ynU9mmVTlkmaIeKqJgLIAJ23%26wd%3D%26eqid%3Dcde58f4b000216a0000000026461dd2c&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%25E6%2595%25B0%25E6%258D%25AE%25E4%25BB%2593%25E5%25BA%2593%26city%3D101010100%26page%3D1&s=3&g=&friend_source=0&s=3&friend_source=0; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1684397122; __c=1683525769; __a=10008462.1582085594.1664242401.1683525769.72.3.51.72; __zp_stoken__=059deWyAybi1qYHdJQCF9a39lZitdJTV6Sn9%2FJCdKElhHEScUaFRhbToaaDQiPl1sLTsPRzdsID5ub3cELERuY0syBUpoQhAzBG0eSxkqWVkNXEsjOFhdGDMUQwIpeSsnbwI9PDhEVFx4NCU%3D; geek_zp_token=V1Q9ogGO30219gXdNhyx4RLiK16TzXxA~~; __zp_sseed__=QC4VJGf0l3Py+Wsb7K39qoBQV0/5TeEgRxuo581TE2I=; __zp_sname__=c8e6fbc4; __zp_sts__=1684397431533",
        "Connection": "keep-alive",
        "referer": "https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E4%BB%93%E5%BA%93&city=101010100",
        "Host": "www.zhipin.com",
    }

    data = {
        "query": key_word,
        "page": page,
        "pageSize": page_size
    }

    response = session.get(url=url, params=data, headers=headers)
    print(response.url)

    result = json.loads(response.text)
    # {"code":37,"message":"您的访问行为异常.","zpData": {}}
    
    if result["code"] != 0:
        raise Exception(result)

    data = result["zpData"]

    print("-" * 100)
    print("resCount:", data["resCount"], ", totalCount:", data["totalCount"])

    job_list = data["jobList"]

    df = pd.DataFrame(job_list)
    return df

def get_job_detail(encryptJobId):
    # encryptJobId
    url = "https://www.zhipin.com/wapi/zpitem/web/competitive/jobDetail.json?encryptJobId=2d014a07bb5914211XF_3t-8GFRZ"
    
    headers = {
        "user-agent": USER_AGENT,
        "cookie": "wd_guid=01a8dbd7-5ebb-40b5-9c8e-2c242e2a9127; historyState=state; _9755xjdesxxd_=32; YD00951578218230%3AWM_TID=DwZ9BHIW5OJEBQRURAKRXj7lwsOs2JYf; lastCity=101010100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1683525769; _bl_uid=nklq8hdve88fwwsjyjnOjew7Cn2X; gdxidpyhxdE=J8qm6%2BBdEg%5CGSbBXGMudK7z6Ljx%2FvnNTJZpAyS7BTgDS%5CQci7xMyceV03phie3wZGtNj1m7Ix8sy17hqS15UsGeD5iUN%2BOw6g0oGS6cXbTKgb6lqVlaIO6nBwUcpLIkxokkXHh6w1qhKk0UpKP5sRtuoaeZ7b7ODOer4I5ridTiGcNrg%3A1683795358326; YD00951578218230%3AWM_NI=fRuGY4qtxzyjrD81hY5xNWHk5PxJsjZq2f6IDxCYGRuKHCtoeelETmkSVUR0BxZZdpy6bkH0MqwBYenliWNAh1a23eawX8CxYxU082z2vxkwdxejvTwUrHMzMCgTQsnkdWo%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed2ec59a9e9858ed040bae78ea2c44e839a9f86d13b869d8cccf244969cfda5ed2af0fea7c3b92aa68ebba8dc40b3acb89bfc62b29cf8d2eb53f7a882b8cb61f790b8abf2629aaffe87b54388a88dbac65ab79588a4f765a7bba4a6d767a98d9ab6d13c82a896bbe77cbbeaae8ccb3c8fafb9a3dc6faeb4a7b8cd4bacefafd3b26fa3a998d9c2749ba89bd1bb3abaeeba99ea7da8a8ab8bf560b58bbea9d0728f9da9b5d479aeb5acb8ee37e2a3; wt2=DSn_5RgchyYGe5UGkCojZFaPSbDsjNBq_uthMJ2du2Y-b5i9P5cZegrySQqXD7px2CSidVqvzGuPZj-UEu_usfw~~; wbg=0; __zp_seo_uuid__=536c6a61-74af-4f1b-aec1-f5dcd25a8c0d; __g=-; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1684135295; __c=1683525769; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dj4w1ZktGT3Zqn_NCvE9bcP7_Au-uUtOOhLEmrxY7ynU9mmVTlkmaIeKqJgLIAJ23%26wd%3D%26eqid%3Dcde58f4b000216a0000000026461dd2c&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%25E6%2595%25B0%25E6%258D%25AE%25E4%25BB%2593%25E5%25BA%2593%26city%3D101010100&s=3&g=&friend_source=0&s=3&friend_source=0; __a=10008462.1582085594.1664242401.1683525769.49.3.28.49; __zp_stoken__=8d86eaQJICQcXaX19GQR9BG1yLSpROBBtam9GOCkJUFolTmRuBXsMFnVwdjpsQFAKWmNWdUt7XxwKBC1dZlpfYyU0DQI1QFgeaGQxElQfJQViBEU0eEQiNxcVCR5UKgMWGFpkDkRbfGQ2NCw%3D; geek_zp_token=V1Q9ogGO30219gXdNhyxwbIS617DzTxA~~; __zp_sseed__=QC4VJGf0l3Py+Wsb7K39ql3cxQBedVDRo3xk8smkrVA=; __zp_sname__=1ddcad1d; __zp_sts__=1684138028747",
    }
    
    data = {"encryptJobId": encryptJobId}
    response = session.get(url=url, params=data, headers=headers)
    print(response.url)
    
    result = json.loads(response.text)
    # {"code":37,"message":"您的访问行为异常.","zpData": {}}
    
    if result["code"] != 0:
        raise Exception(result)

    data = result["zpData"]

if __name__ == '__main__':
    # get_token()
    
    key_word = "数据仓库"
    df = pd.DataFrame()
    try:
        for i in range(100):
            print(i)
            df_part = get_job_list(key_word, i)
            df = pd.concat([df, df_part], ignore_index=True, sort=False)
            time.sleep(random.randint(3,6))
    finally:
        df.to_excel("boss_" + key_word + "_requests.xlsx", index=False)
    