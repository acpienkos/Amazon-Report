"""Download public sources, preserving actual retrieval times and failure evidence."""
from pathlib import Path
import urllib.request, json, hashlib
from datetime import datetime, timezone
HERE=Path(__file__).resolve().parent
URLS={
 'amazon_2025':'https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm',
 'amazon_2026q2':'https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm',
 'amazon_release':'https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx',
 'microsoft_release':'https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast',
 'walmart_release':'https://www.sec.gov/Archives/edgar/data/104169/000010416926000032/earningsreleasefy26q4.htm',
 'walmart_10k':'https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm',
 'microsoft_10k':'https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm',
 'treasury':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026',
 'amazon_debt':'https://www.sec.gov/Archives/edgar/data/1018724/000110465926081334/tm2619352d3_fwp.htm',
 'amzn_price':'https://chartexchange.com/symbol/nasdaq-amzn/historical/',
 'msft_price':'https://chartexchange.com/symbol/nasdaq-msft/historical/',
 'wmt_price':'https://chartexchange.com/symbol/nasdaq-wmt/historical/',
 'course_readme':'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/README.md',
 'course_boundary':'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/projects/AI-BOUNDARY-CARD.md',
}
def main():
    log=HERE/'evidence/source_downloads.json'
    records=json.loads(log.read_text()) if log.exists() else []
    for key,url in URLS.items():
        path=HERE/'sources'/(key+'.html')
        if path.exists(): continue
        record={'id':key,'url':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'Academic finance research Andrew student contact via course instructor','Accept':'text/html'})
            with urllib.request.urlopen(request,timeout=25) as response:
                data=response.read(); record['http_status']=response.status
            path.write_bytes(data)
            record.update(path=str(path.relative_to(HERE)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
        except Exception as e: record['error']=str(e)
        records.append(record);print(key,record.get('http_status',record.get('error')))
    (HERE/'evidence/source_downloads.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
if __name__=='__main__': main()
