from pathlib import Path
import html,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
def write(path,text):path.write_text(text.strip()+'\n',encoding='utf-8')

def money(x):return f'${x:,.2f}'

def mdtable(rows,columns):
    return '| '+' | '.join(columns)+' |\n|'+'|'.join('---' for _ in columns)+'|\n'+'\n'.join('| '+' | '.join(str(r.get(k,'')) for k in columns)+' |' for r in rows)

def pdf(source,dest,title):
    styles=getSampleStyleSheet()
    styles['Normal'].fontName='Helvetica';styles['Normal'].fontSize=9.2;styles['Normal'].leading=13
    styles['Normal'].spaceAfter=6
    styles.add(ParagraphStyle(name='SmallBody',parent=styles['Normal'],fontSize=8,leading=11))
    story=[]
    for block in source.split('\n\n'):
        block=block.strip()
        if not block:continue
        if block=='<!-- PAGEBREAK -->':story.append(PageBreak());continue
        if block.startswith('|'):
            lines=[x for x in block.splitlines() if x.startswith('|') and not re.match(r'^\|[- :|]+\|$',x)]
            data=[[Paragraph(html.escape(z.strip()).replace('**',''),styles['SmallBody']) for z in line.strip('|').split('|')] for line in lines]
            if data:
                widths=[480/len(data[0])]*len(data[0])
                t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
                t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eef5')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#d5dde7')),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.extend([t,Spacer(1,9)])
            continue
        style=styles['Normal'];text=block
        if block.startswith('# '):style=styles['Title'];text=block[2:]
        elif block.startswith('## '):style=styles['Heading2'];text=block[3:]
        elif block.startswith('### '):style=styles['Heading3'];text=block[4:]
        text=html.escape(text).replace('**','').replace('`','').replace('\n','<br/>')
        story.append(Paragraph(text,style))
    def footer(canvas,doc):
        canvas.saveState();canvas.setStrokeColor(colors.HexColor('#cbd7e5'));canvas.line(42,39,570,39)
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526176'))
        canvas.drawString(42,27,'FIN 43900 | AMZN | AI-assisted educational analysis | Provisional')
        canvas.drawRightString(570,27,str(doc.page));canvas.restoreState()
    SimpleDocTemplate(str(dest),pagesize=(612,792),rightMargin=60,leftMargin=60,topMargin=42,bottomMargin=50,title=title,author='Andrew Pienkos; AI-assisted draft').build(story,onFirstPage=footer,onLaterPages=footer)