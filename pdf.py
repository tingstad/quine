#!/usr/bin/env python3
import re
from typing import Dict, List, Optional, Set, Tuple

obj: Dict[int, str] = {}

pagewidth = 1000
pageheight = 5200

def main() -> None:

    template = """%PDF-1.5
10 0 obj <</Type /Catalog /Pages 11 0 R >> endobj % Content == source code (https://github.com/tingstad/quine)
11 0 obj <</Type /Pages /Kids [12 0 R] /Count 1 /MediaBox [0 0 {pagewidth} {pageheight}] >> endobj\
""".format(pagewidth=pagewidth, pageheight=pageheight)

    maxobj = 89

    obj[0] = ''  # unused
    obj[1] = 'Tj'  # print
    obj[2] = 'Tj T*'  # print + NL
    obj[3] = '(3)'
    obj[4] = 'Tj ( 0 obj << /Length 118 >> stream) Tj T* <28> Tj'
    obj[5] = 'Tj ( 0 obj << /Length ) Tj'
    obj[6] = '(2)'
    obj[7] = '(4)'
    obj[8] = 'Tj ( >> stream) Tj T* <28> Tj'
    obj[9] = 'Tj <29> Tj T* (endstream endobj) Tj T*'
    obj[10] = 'SPECIAL'
    obj[11] = 'SPECIAL'
    obj[12] = 'SPECIAL'
    obj[13] = '(11 0 obj <</Type /Pages /Kids [12 0 R] /Count 1 /MediaBox [0 0 {} {}] >> endobj)'.format(pagewidth, pageheight)
    obj[14] = '(10 0 obj <</Type /Catalog /Pages 11 0 R >> endobj % Content == source code (https://github.com/tingstad/quine))'
    obj[15] = 'BT /F1 11 Tf 50 {y} Td 16 TL (%PDF-1.5)'.format(y=pageheight-68)
    obj[16] = '(16 0 R] >> endobj) Tj T* (startxref) Tj T* (99999) Tj T* (%%EOF) Tj T* ET'
    obj[17] = 'SPECIAL'
    obj[18] = '(BT /F1 11 Tf 50 {y} Td 16 TL (%PDF-1.5))'.format(y=pageheight-68)
    obj[19] = '((16 0 R] >> endobj) Tj T* (startxref) Tj T* (99999) Tj T* (%%EOF) Tj T* ET)'
    obj[20] = '(17 0 obj <</Type /XRef /Root 10 0 R /Size {size} /W [1 2 2] /Filter /ASCIIHexDecode /Length 1999 >> stream)'.format(size=maxobj+1)
    obj[21] = '(12 0 obj <</Type /Page /Parent 11 0 R /Resources <</Font <</F1 <</Type /Font /Subtype /Type1 /BaseFont /Courier>> >> >> /Contents [)'
    obj[22] = '(Tj)'
    obj[23] = '(Tj T*)'
    obj[24] = '(Tj ( 0 obj << /Length 118 >> stream) Tj T* <28> Tj)'
    obj[25] = '(Tj ( >> stream) Tj T* <28> Tj)'
    obj[26] = '(Tj ( 0 obj << /Length ) Tj)'
    obj[27] = '(Tj ( >> stream) Tj T*)'
    obj[28] = '(Tj T* (endstream endobj) Tj T*)'
    obj[29] = 'Tj ( >> stream) Tj T*'
    for i in range(30, 40):
        obj[i] = f'({i - 30})'
    obj[32] = 'Tj T* (endstream endobj) Tj T*'
    obj[33] = '(Tj <29> Tj T* (endstream endobj) Tj T*)'
    obj[34] = '(TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO34)'
    for i in range(40, maxobj):
        obj[i] = f'(TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO{i})'
    obj[maxobj] = f'(TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO{maxobj})'

    for i in (
        [15, 13, 14, 18] +
        [*range(30, 40)] +
        [*range(1, 10)] +
        [*range(19, 30)] +
        [16] +
        [*range(40, maxobj+1)]
    ):
        template += f"""
{i} 0 obj << /Length {len(obj[i])} >> stream
{obj[i]}
endstream endobj"""

    template += """
17 0 obj <</Type /XRef /Root 10 0 R /Size {size} /W [1 2 2] /Filter /ASCIIHexDecode /Length 1999 >> stream
_xref_
endstream endobj
12 0 obj <</Type /Page /Parent 11 0 R /Resources <</Font <</F1 <</Type /Font /Subtype /Type1 /BaseFont /Courier>> >> >> /Contents [
""".format(size=maxobj+1)

    xrefidx = template.index('_xref_')

    # first, use xref placeholder:
    xref = ' '.join(['00 0000 0000'] * (maxobj + 1))
    template = template[:xrefidx] + xref + template[template.index('\n', xrefidx):]

    xref = ['00 0000 FFFF']
    xrefstr = xref[0]
    for i in range(1, maxobj + 1):
        if i % 9 == 0:
            xrefstr += '\n'
        else:
            xrefstr += ' '
        xrefstr += '01 xx{:02} 0000'.format(i)
    xreflines = xrefstr.split('\n')
    if len(xreflines[-1]) != 116:
        raise Exception(f'xref line length != 116: {len(xreflines[-1])}')

    xrefobjs, template = takeobj(obj, template, xreflines)

    for i in range(1, maxobj + 1):
        pattern = '^{} 0 obj'.format(i)
        match = re.search(pattern, template, flags=re.MULTILINE)
        old = 'xx{:02}'.format(i)
        new = '{:04X}'.format(match.start())
        xrefstr = xrefstr.replace(old, new)
        template = template.replace(old, new)
        xref.append(f'01 {new} 0000')

    xreflen = len(xrefstr)
    template = template.replace('1999', '{:04d}'.format(xreflen))
    if xreflen > 9999:
        raise Exception(f'unexpected length: {xreflen}')

    xrefidx = template.index('00 0000 0000')

    template = template[:xrefidx] + xrefstr + template[xrefidx + template[xrefidx:].index('endstream') - 1:]

    def digit(s):
        n = int(s)
        if n == 3:
            return '3'
        elif n == 2:
            return '6'
        elif n == 4:
            return '7'
        return f'3{n}'

    stream = ""
    #          15 0 obj << /Length 40 >> stream
    stream += '15 0 R  2 0 R  14 0 R  2 0 R  13 0 R  2 0 R  31 0 R  1 0 R  35 0 R  5 0 R  7 0 R  1 0 R  30 0 R  29 0 R  18 0 R  32 0 R  '
    #           13 0 obj <</Length 85 >> stream
    stream += '31 0 R  1 0 R  3 0 R  5 0 R  38 0 R  1 0 R  35 0 R  8 0 R  13 0 R  9 0 R  '
    #           14 0 obj <</Length 112 >> stream
    stream += '31 0 R  1 0 R  7 0 R  5 0 R  31 0 R  1 0 R  31 0 R  1 0 R  6 0 R  8 0 R  14 0 R  9 0 R  '
    #           18 0 obj <</Length 42 >> stream
    stream += '31 0 R  1 0 R  38 0 R  5 0 R  7 0 R  1 0 R  6 0 R  8 0 R  18 0 R  9 0 R  '
    #          30 0 obj <</Length 3 >> stream
    stream += '3 0 R  1 0 R  30 0 R  5 0 R  3 0 R  8 0 R  30 0 R  9 0 R  '
    #          31 0 obj <</Length 3 >> stream
    stream += '3 0 R  1 0 R  31 0 R  5 0 R  3 0 R  8 0 R  31 0 R  9 0 R  '
    #          32 0 obj <</Length 30 >> stream
    stream += '3 0 R  1 0 R  6 0 R  5 0 R  3 0 R  1 0 R  30 0 R  29 0 R  28 0 R  32 0 R  '
    #          33 0 obj <</Length 40 >> stream
    stream += '3 0 R  1 0 R  3 0 R  5 0 R  7 0 R  1 0 R  30 0 R  8 0 R  33 0 R  9 0 R  '
    #            34 0 obj <</Length 118 >> stream
    stream += f'{digit("3")} 0 R  1 0 R  {digit("4")} 0 R  4 0 R  34 0 R  9 0 R '
    #          35 0 obj <</Length 3 >> stream
    stream += '3 0 R  1 0 R  35 0 R  5 0 R  3 0 R  8 0 R  35 0 R  9 0 R  '
    stream += '3 0 R  1 0 R  36 0 R  5 0 R  3 0 R  8 0 R  36 0 R  9 0 R  '
    stream += '3 0 R  1 0 R  37 0 R  5 0 R  3 0 R  8 0 R  37 0 R  9 0 R  '
    stream += '3 0 R  1 0 R  38 0 R  5 0 R  3 0 R  8 0 R  38 0 R  9 0 R  '
    stream += '3 0 R  1 0 R  39 0 R  5 0 R  3 0 R  8 0 R  39 0 R  9 0 R  '
    #           1 0 obj <</Length 2 >> stream
    stream += '31 0 R  5 0 R  6 0 R  29 0 R  22 0 R  32 0 R  '
    #          2 0 obj <</Length 5 >> stream
    stream += '6 0 R  5 0 R  35 0 R  29 0 R  23 0 R  32 0 R  '
    #          3 0 obj <</Length 3 >> stream
    stream += '3 0 R  5 0 R  3 0 R  8 0 R  3 0 R  9 0 R  '
    #           4 0 obj <</Length 4 >> stream
    stream += '7 0 R  5 0 R  35 0 R  1 0 R  30 0 R  29 0 R  24 0 R  32 0 R  '
    #           5 0 obj <</Length 26 >> stream
    stream += '35 0 R  5 0 R  6 0 R  1 0 R  36 0 R  29 0 R  26 0 R  32 0 R  '
    #           6 0 obj <</Length 3 >> stream
    stream += '36 0 R  5 0 R  3 0 R  8 0 R  6 0 R  9 0 R  '
    #           7 0 obj <</Length 3 >> stream
    stream += '37 0 R  5 0 R  3 0 R  8 0 R  7 0 R  9 0 R  '
    #           8 0 obj <</Length 29 >> stream
    stream += '38 0 R  5 0 R  6 0 R  1 0 R  39 0 R  29 0 R  25 0 R  32 0 R  '
    #           9 0 obj <</Length 38 >> stream
    stream += '39 0 R  5 0 R  3 0 R  1 0 R  38 0 R  29 0 R  33 0 R  32 0 R  '
    #           19 0 obj <</Length 76 >> stream
    stream += '31 0 R  1 0 R  39 0 R  5 0 R  37 0 R  1 0 R  36 0 R  8 0 R  19 0 R  9 0 R  '
    #          20 0 obj <</Length 104 >> stream
    stream += '6 0 R  1 0 R  30 0 R  5 0 R  31 0 R  1 0 R  30 0 R  1 0 R  7 0 R  8 0 R  20 0 R  9 0 R  '
    #          21 0 obj <</Length 133 >> stream
    stream += '6 0 R  1 0 R  31 0 R  5 0 R  31 0 R  1 0 R  3 0 R  1 0 R  3 0 R  8 0 R  21 0 R  9 0 R '

    for i in [*range(22, 30)]:
        if i == 29:
            #            29 0 obj <</Length 21 >> stream
            stream += f' {digit(str(i)[0])} 0 R  1 0 R  {digit(str(i)[1])} 0 R  5 0 R  6 0 R  1 0 R  31 0 R  29 0 R  27 0 R  32 0 R '
            continue
        stream += f' {digit(str(i)[0])} 0 R  1 0 R  {digit(str(i)[1])} 0 R  5 0 R '
        for n, j in enumerate(str(len(obj[i]))):
            stream += f' 1 0 R ' if n > 0 else ''
            stream += f' {digit(j)} 0 R '
        stream += f' 8 0 R  {i} 0 R  9 0 R '
    #           16 0 obj << /Length 74 >> stream
    stream += " 31 0 R  1 0 R  36 0 R  5 0 R  37 0 R  1 0 R  7 0 R  29 0 R  19 0 R  32 0 R"
    for i in range(40, maxobj):
        if len(obj[i]) == 118:
            #             XX 0 obj <</Length 118 >> stream
            stream += f' {digit(str(i)[0])} 0 R  1 0 R  {digit(str(i)[1])} 0 R  4 0 R  {i} 0 R  9 0 R '
        else:
            raise Exception(f'unexpected obj len: {len(obj[i])}')
    #            89 0 obj <</Length 99 >> stream
    stream += ' 38 0 R  1 0 R  39 0 R  5 0 R  39 0 R  1 0 R  39 0 R  8 0 R  89 0 R  9 0 R '

    #           17 0 obj <</Type /XRef /Root 10 0 R /Size XX /W [1 2 2] /Filter /ASCIIHexDecode /Length 1999 >> stream
    stream += ' 20 0 R'
    for i in xrefobjs:
        stream += f' 2 0 R  {i} 0 R'
    stream += ' 32 0 R  21 0 R '

    while True:
        lines = split(stream.replace("  ", " "), 116)

        if len(lines) < 2:
            break

        streamobjs, template = takeobj(obj, template, lines[:-1])

        template += '\n'.join(lines[:-1])

        template += '\n'

        stream = lines[-1]
        for i in streamobjs:
            stream += f' 2 0 R {i} 0 R'

    # Handle final line(s)

    stream += ' 2 0 R '

    lastobj = maxobj
    stream += '{i} 0 R 2 0 R'.format(i=lastobj)

    idx = template.index('{} 0 obj'.format(lastobj))
    lastobjlen = len(stream) + 2
    lastobjlenstr = '{:02}'.format(lastobjlen)
    template = template[:idx] + template[idx:].replace('99', lastobjlenstr, 1)
    template = template[:template.index('(', idx)+1] + stream + template[template.index(')', idx):]
    template += stream
    template = template.replace(xref[17], '01 {:04X} 0000'.format(template.rfind('17 0 obj')))
    template = template.replace(xref[12], '01 {:04X} 0000'.format(template.rfind('12 0 obj')))
    # 89 0 obj <</Length 99 >> stream
    pattern = ' 0?5 0 R (39) 0 R 0?1 0 R (39) 0 R 8 0 R'.replace(' ', r'\s')
    match = re.search(pattern, template, flags=re.MULTILINE)
    linecount = len(match.group(0).split('\n'))
    if linecount != 1:
        raise Exception('unexpected number of lines for pattern: {}'.format(linecount))
    template = template[:match.span(1)[0] + 1] + lastobjlenstr[0] + template[match.span(1)[1]:]
    template = template[:match.span(2)[0] + 1] + lastobjlenstr[1] + template[match.span(2)[1]:]
    template = re.sub('^(0 R 4 0 R 88 0 R 9 0 R 38 0 R 1 0 R 39 0 R 5 0 R 3)9( 0 R 1 0 R 3)9( 0 R 8 0 R 89 0 R 9 0 R 20 0 R 2 0 R 34 0 R 2 0 R 40)',
        r'\g<1>{}\g<2>{}\3'.format(lastobjlenstr[0], lastobjlenstr[1]),
        template, count=1, flags=re.MULTILINE)

    startxref = template.index('\n17 0 obj <</Type /XRef') + 1

    template += f"""
16 0 R] >> endobj
startxref
{startxref}
%%EOF"""

    if startxref > 99999 or startxref < 10000:
        raise Exception(f'invalid startxref: {startxref}')
    template = template.replace('99999', str(startxref))

    print(template)


def split(stream: str, n: int = 116) -> List[str]:
    lines = []
    while len(stream) > n:
        i = stream.rfind(' ', 0, n+1)
        if i < 0:
            raise Exception(f'did not find space: {stream}')
        line = stream[:i]
        stream = stream[i + 1:]
        if len(line) > n:
            raise Exception(f'invalid len>{n}: {len(line)}')
        while len(line) < n:
            match = re.search(r' \d 0 R', line)
            if not match:
                raise Exception(f'pattern not found: {line}')
            line = re.sub(r' (\d 0 R)', r' 0\1', line, count=1)
        lines.append(line)
    if len(stream) > 0:
        lines.append(stream)
    return lines


def takeobj(obj, template, lines):
    objs = []
    for idx, line in enumerate(lines):
        found = -1
        for i in range(1, len(obj)):
            if not obj[i].startswith('(TODOOOOOOOOOOOOOOO'):
                continue
            found = i
            j = template.index(obj[found]) + 1
            obj[i] = f'({line})'
            end = template.index(')', j) - j
            template = template[:j] + line + template[j+end:]
            if len(line) != 116:
                raise Exception(f'invalid len: {len(line)}')
                j = template[:j].rindex('/Length 118')
                template = template[:j+8] + str(len(line)) + template[j+11:]
                # raise Exception(f'invalid len: {len(line)}')
            break
        if found == -1:
            raise Exception(f'no (TODOOOOOOOOOOOOOOO found for {idx}')
        if found == 83:
            lines.insert(idx + 1, '82 0 R 2 0 R 84 0 R 2 0 R 73 0 R 2 0 R 78 0 R 2 0 R 71 0 R 2 0 R 83 0 R 2 0 R 84 0 R 2 0 R 65 0 R 2 0 R 68 0 R 2 0 R')
        if found == 84:
            continue
        objs.append(found)
    return objs, template


if __name__ == '__main__':
    main()
