from pathlib import Path
import json,re,hashlib
import pymupdf
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'output/pdf/build_manifest.json').read_text(encoding='utf8'))
doc=pymupdf.open(root/'output/pdf/report_ru.pdf')
out=root/'tmp/pdfs';out.mkdir(parents=True,exist_ok=True)
text=''.join(p.get_text(clip=pymupdf.Rect(0,0,p.rect.width,800)) for p in doc)
norm=lambda s:re.sub(r'\s+','',s).replace('\u00ad','')
full=norm(text)
missing=[s for s in manifest['source_text_fragments'] if norm(s) not in full]
assert not missing,repr(missing[:10])
thumbs=[];bad=[]
for i,page in enumerate(doc):
    pix=page.get_pixmap(matrix=pymupdf.Matrix(1.2,1.2)); path=out/f'page-{i+1:02}.png';pix.save(path)
    img=Image.open(path).convert('RGB');img.thumbnail((238,337))
    tile=Image.new('RGB',(258,365),'#dce1e6');tile.paste(img,((258-img.width)//2,5));ImageDraw.Draw(tile).text((10,346),str(i+1),fill='black');thumbs.append(tile)
    for block in page.get_text('dict')['blocks']:
        if block['type']==0:
            x0,y0,x1,y1=block['bbox']
            if x0<45 or x1>550 or y0<30 or y1>820:bad.append([i+1,block['bbox']])
for start in range(0,len(thumbs),12):
    group=thumbs[start:start+12];sheet=Image.new('RGB',(258*4,365*3),'white')
    for k,img in enumerate(group):sheet.paste(img,((k%4)*258,(k//4)*365))
    sheet.save(out/f'contact-{start//12+1}.png')
assert not bad,bad
qa={'pages':len(doc),'embedded_images':sum(len(p.get_images()) for p in doc),'all_source_fragments_found':True,'text_fragments':len(manifest['source_text_fragments']),'bounds_check':True,'source_unchanged':hashlib.sha256((root/manifest['source']).read_bytes()).hexdigest()==manifest['source_sha256']}
(root/'output/pdf/verification.json').write_text(json.dumps(qa,indent=2),encoding='utf8')
print(qa)
