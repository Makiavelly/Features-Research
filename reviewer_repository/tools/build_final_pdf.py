"""Render the user-approved Markdown verbatim, adding existing figures only."""
from pathlib import Path
import hashlib, html, json, re
from markdown_it import MarkdownIt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'reports/project_history_2026_10_25/report_ru.md'
OUT = ROOT/'output/pdf'
FIGURES = {
 '2.': ['relbench_hm_v1/comparison.png','relbench_hm_v1/learning_curves.png','relbench_hm_v1/test_ap_distribution.png'],
 '3.1.': ['gnn_embeddings_v1/comparison.png'],
 '3.2.': ['two_tower_v1/comparison.png'],
 '4.': ['llmfe_h002_shared_v1/comparison.png','llmfe_h002_shared_v1/search_progress.png','llmfe_h002_shared_v1/ap_histograms.png'],
 '5.': ['hm_llmfe_flat_v1_audit/export/comparison.png','hm_llmfe_flat_v1_audit/export/ap_histograms.png'],
 '6.': ['balance_scale_llama31_diagnostic_v2_audit/export/diagnostic.png'],
 '7.1.': ['contextgnn_small_v1/comparison.png'],
 '7.2.': ['recformer_ablations_v1/comparison.png','recformer_ablations_v1/learning_curves.png'],
 '7.3.': ['tdm_small_v1/comparison.png','tdm_small_v1/search_cost.png'],
 '8.': ['provider_history_v1/comparison_all_methods.png','provider_history_v1/test_histograms.png'],
 '9.': ['medium_followup_v1/final_comparison/comparison.png','medium_followup_v1/final_comparison/ap_histograms.png','medium_followup_v1/final_comparison/api_budget_curves.png'],
 '10.': ['medium_followup_v1/context_combined_test_v1/comparison.png'],
 '11.': ['medium_h011_codex_budget300_v2/comparison.png'],
 '12.1.': ['medium_followup_v1/context_global_aux_v3/comparison.png'],
 '12.2.': ['medium_followup_v1/item_encoder_followup_v1/final_comparison.png'],
 '12.3.': ['medium_followup_v1/context_multi_interest_v2/final_comparison.png'],
 '13.': ['medium_multi_interest_test_v1/comparison_all.png'],
}

def main():
    original=SOURCE.read_bytes(); text=original.decode('utf-8-sig')
    OUT.mkdir(parents=True,exist_ok=True)
    fontdir=Path('C:/Windows/Fonts') if Path('C:/Windows/Fonts').exists() else Path('/usr/share/fonts/truetype/dejavu')
    for name,win,linux in [('Body','arial.ttf','DejaVuSans.ttf'),('Bold','arialbd.ttf','DejaVuSans-Bold.ttf'),('Italic','ariali.ttf','DejaVuSans-Oblique.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(fontdir/(win if (fontdir/win).exists() else linux))))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
    base=ParagraphStyle('body',fontName='Body',fontSize=9.5,leading=13.3,spaceAfter=7,textColor=colors.HexColor('#202936'),splitLongWords=True)
    styles={i:ParagraphStyle(f'h{i}',parent=base,fontName='Bold',fontSize={1:18,2:14,3:11.5}.get(i,10),leading={1:23,2:18,3:15}.get(i,14),spaceBefore=14,spaceAfter=9,keepWithNext=True) for i in range(1,7)}
    cell=ParagraphStyle('cell',parent=base,fontSize=7.7,leading=10,spaceAfter=0)
    md=MarkdownIt('commonmark').enable('table'); tokens=md.parse(text)
    story=[]; expected=[]; inserted=[]; active=None
    def inline(tok):
        out=[]
        for t in tok.children or []:
            if t.type=='text':out.append(html.escape(t.content)); expected.append(t.content)
            elif t.type=='code_inline':out.append('<font color="#354c68">'+html.escape(t.content)+'</font>');expected.append(t.content)
            elif t.type in ('softbreak','hardbreak'):out.append(' ')
            elif t.type=='strong_open':out.append('<b>')
            elif t.type=='strong_close':out.append('</b>')
            elif t.type=='em_open':out.append('<i>')
            elif t.type=='em_close':out.append('</i>')
            elif t.type=='link_open':
                href=t.attrGet('href')
                out.append('<a href="'+html.escape(href,quote=True)+'" color="#245d92">' if href.startswith(('https:','http:')) else '<span>')
            elif t.type=='link_close':out.append('</a>' if False else '</span>')
        # ReportLab has no span tags; reconstruct link closing with a stack.
        result=''.join(out); stack=[]; fixed=[]
        for part in re.split('(<a [^>]+>|<span>|</span>)',result):
            if part.startswith('<a '):stack.append('a');fixed.append(part)
            elif part=='<span>':stack.append('span')
            elif part=='</span>':
                if stack.pop()=='a':fixed.append('</a>')
            else:fixed.append(part)
        return ''.join(fixed)
    def figures():
        for rel in FIGURES.get(active,[]):
            path=ROOT/'reports'/rel
            if not path.exists():raise FileNotFoundError(path)
            img=Image(str(path)); scale=min(487/img.imageWidth,430/img.imageHeight)
            img.drawWidth=img.imageWidth*scale;img.drawHeight=img.imageHeight*scale
            story.extend([Spacer(1,8),img,Spacer(1,10)])
            inserted.append({'section':active,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    i=0
    while i<len(tokens):
        t=tokens[i]
        if t.type=='heading_open':
            content=tokens[i+1].content; key=content.split(' ',1)[0]
            if key in FIGURES or t.tag=='h2' or content.startswith(('Краткие итоги','Какие-либо выводы')):
                figures();active=key
            story.append(Paragraph(inline(tokens[i+1]),styles[int(t.tag[1:])]))
            i+=3;continue
        if t.type=='paragraph_open':
            story.append(Paragraph(inline(tokens[i+1]),base));i+=3;continue
        if t.type=='table_open':
            rows=[];row=[];i+=1
            while tokens[i].type!='table_close':
                if tokens[i].type=='tr_open':row=[]
                if tokens[i].type=='inline':row.append(Paragraph(inline(tokens[i]),cell))
                if tokens[i].type=='tr_close':rows.append(row)
                i+=1
            count=len(rows[0]); widths=([170]+[(487-170)/(count-1)]*(count-1)) if count>1 else [487]
            if count==4:widths=[135,196,78,78]
            if count>=5:widths=[155]+[(487-155)/(count-1)]*(count-1)
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eef5')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#ccd5df')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.extend([table,Spacer(1,9)])
        elif t.type in ('fence','code_block'):
            for line in t.content.splitlines():story.append(Paragraph(html.escape(line),cell));expected.append(line)
        i+=1
    figures()
    target=OUT/'report_ru.pdf'
    def footer(c,doc):
        c.setFont('Body',8);c.setFillColor(colors.HexColor('#607080'));c.drawRightString(541,26,str(doc.page))
    doc=SimpleDocTemplate(str(target),pagesize=(595.28,841.89),leftMargin=54,rightMargin=54,topMargin=43,bottomMargin=45,title=tokens[1].content,author='')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    assert SOURCE.read_bytes()==original,'Source changed during rendering'
    (OUT/'build_manifest.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(original).hexdigest(),'pdf_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'figures':inserted,'source_text_fragments':expected},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pdf':str(target),'figures':len(inserted)},ensure_ascii=False))

if __name__=='__main__':main()
