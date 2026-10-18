from pathlib import Path
import urllib.request,json,concurrent.futures
O=Path("/Users/bigd/Obsidian Vault/Сообщество/02 Field (продукт 2.0)/00_brief/HANDOFF — лендинг aicamp6 и A-B варианты — 2026-10-08/outputs/готовое")
W=Path("/Users/bigd/Obsidian Vault/Сообщество/02 Field (продукт 2.0)/00_brief/HANDOFF — лендинг aicamp6 и A-B варианты — 2026-10-08/outputs/рабочее")
items=json.loads("[{\"key\":\"smartgen\",\"name\":\"SMARTGEN\",\"site\":\"https://www.smartgenisrael.com/\",\"asset\":\"https://static.wixstatic.com/media/fc9931_1e8c79a5852b472ebebf13dc67fdb47f~mv2.png/v1/fill/w_136,h_128,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/logo-2.png\"},{\"key\":\"tlvmed\",\"name\":\"Tel Aviv Medical Center\",\"site\":\"https://tlvmed.co.il/\",\"asset\":\"https://tlvmed.co.il/wp-content/uploads/2018/10/logo.png\"},{\"key\":\"olim\",\"name\":\"Всеизраильская Федерация репатриантов\",\"site\":\"https://olimisrael.org.il/\",\"asset\":\"https://olimisrael.org.il/wp-content/uploads/2024/08/Fed_Light.svg\"},{\"key\":\"wave\",\"name\":\"WAVE\",\"site\":\"https://wave-network.com/\",\"asset\":\"https://wave-network.com/web/image/website/1/logo/Wave-Network?unique=29dd1b1\"},{\"key\":\"yaar\",\"name\":\"YAAR\",\"site\":\"https://yaarbar.com/\",\"asset\":\"https://yaarbar.com/wp-content/uploads/2026/01/YAAR_Simple_Logo-removebg-preview-transparent.png\"},{\"key\":\"londoncult\",\"name\":\"London Cult\",\"site\":\"https://londoncult.co.uk/\",\"asset\":\"https://londoncult.co.uk/wp-content/uploads/2022/11/london_cult-logo.svg\"}]")
def get(item):
 req=urllib.request.Request(item['asset'],headers={'User-Agent':'Mozilla/5.0','Accept':'image/png,image/svg+xml,image/webp,*/*'})
 with urllib.request.urlopen(req,timeout=25) as r:
  mime=r.headers.get_content_type();data=r.read()
 ext={'image/png':'png','image/webp':'webp','image/svg+xml':'svg','image/avif':'avif','image/jpeg':'jpg'}.get(mime)
 if not ext: raise ValueError((item['key'],mime))
 item['file']='assets/partner-'+item['key']+'-v4-4.'+ext
 (O/item['file']).write_bytes(data)
 item['bytes']=len(data);item['mime']=mime
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 result=list(pool.map(get,items))
(W/'partner-sources-v4-4.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))

