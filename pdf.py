#!/usr/bin/env python3
import re
from typing import Dict, List, Optional, Set, Tuple

obj: Dict[int, str] = {}

# Default user space units: 1 point = 1/72 inch
# Letter width: 8.5 inches (215.9 mm)
# => 72 * 8.5 = 612
#
# A4: 210 mm × 297 mm (8.27 in × 11.7 in)
# 595 842

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
            stream += f' {digit(str(i)[0])} 0 R  1 0 R  {digit(str(i)[1])} 0 R  5 0 R '
            for n, j in enumerate(str(len(obj[i]))):
                stream += f' 1 0 R ' if n > 0 else ''
                stream += f' {digit(j)} 0 R '
            stream += f' 8 0 R  {i} 0 R  9 0 R '
    #            89 0 obj <</Length 99 >> stream
    stream += ' 38 0 R  1 0 R  39 0 R  5 0 R  39 0 R  1 0 R  39 0 R  8 0 R  89 0 R  9 0 R '
    # for i in range(maxobj, maxobj+1):
    #     stream += f' 3{str(i)[0]} 0 R 1 0 R 3{str(i)[1]} 0 R 5 0 R'
    #     for n, j in enumerate(str(len(obj[i]))):
    #         stream += f' 1 0 R' if n > 0 else ''
    #         stream += f' 3{j} 0 R'
    #     stream += f' 8 0 R {i} 0 R 9 0 R'

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
    lines = split(stream.replace("  ", " "), 116)

    if False and len(stream) >= 116: #+ len(' 2 0 R {i} 0 R 2 0 R'.format(i=99)) > 118:
        streamobjs, template = takeobj(obj, template, lines[:])

        template += '\n'.join(lines[:])

        template += '\n'

        stream = ''
        for i in streamobjs:
            stream += f'{i} 0 R 2 0 R '

    lastobj = maxobj # streamobjs[-1] + 1
    stream += '{i} 0 R 2 0 R'.format(i=lastobj)

    if len(stream) == 116 and False:
        template, n = re.subn(r'(TODO*{})'.format(lastobj), stream, template, count=1)
        obj[lastobj] = f'({stream})'
        lastobj += 1
        stream = ''
    # if len(stream) > 99:
    #     raise Exception(f'invalid stream len: {len(stream)}')
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
    if linecount == 2:
        firstlineidx = template[:match.start()].rfind('\n') + 1
        secndlineidx = template[:match.end()].rfind('\n') + 1
        firstline = template[firstlineidx:secndlineidx-1]
        secndline = template[secndlineidx:template.index('\n', secndlineidx)]
        template = template[:match.span(1)[0] + 1] + lastobjlenstr[0] + template[match.span(1)[1]:]
        template = template[:match.span(2)[0] + 1] + lastobjlenstr[1] + template[match.span(2)[1]:]
        template = template.replace(firstline,
            'R 9 0 R 39 0 R 1 0 R 36 0 R 41 0 R 96 0 R 9 0 R 39 0 R 1 0 R 37 0 R 41 0 R 97 0 R 9 0 R 39 0 R 1 0 R 38 0 R 5 0 R 3{}'.format(
                lastobjlenstr[0]))
        template = template.replace(secndline,
            '0 R 1 0 R 3{} 0 R 1 0 R 3{} 0 R 8 0 R 98 0 R 9 0 R 20 0 R 2 0 R 43 0 R 2 0 R 44 0 R 2 0 R 45 0 R 2 0 R 46 0 R 2 0 R 47'.format(
                lastobjlenstr[1], lastobjlenstr[2]))
    elif linecount == 1:
        template = template[:match.span(1)[0] + 1] + lastobjlenstr[0] + template[match.span(1)[1]:]
        template = template[:match.span(2)[0] + 1] + lastobjlenstr[1] + template[match.span(2)[1]:]
        template = re.sub('^(0 R 4 0 R 88 0 R 9 0 R 38 0 R 1 0 R 39 0 R 5 0 R 3)9( 0 R 1 0 R 3)9( 0 R 8 0 R 89 0 R 9 0 R 20 0 R 2 0 R 34 0 R 2 0 R 40)',
            r'\g<1>{}\g<2>{}\3'.format(lastobjlenstr[0], lastobjlenstr[1]),
            template, count=1, flags=re.MULTILINE)
    else:
        raise Exception('unexpected number of lines for pattern: {}'.format(linecount))

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
    exit()


    # fill obj[i] with some data for i<100 so that all '(NN)' objs have same obj num length (3):
    xrefi = 101-len(obj)
    xref = []
    for i in range(1, xrefi):
        idx = len(obj)
        obj[idx] = '({:010d} 00000 n )'.format(i)
        xref += [f'{idx} 0 R', '4 0 R']

    for i in range(0, 10):
        obj[len(obj)] = f'(0{i})'
    for i in range(10, 100):
        obj[len(obj)] = f'({i})'

    xrefs = 300
    for i in range(xrefi, xrefs):
        idx = len(obj)
        obj[idx] = '({:010d} 00000 n )'.format(i)
        xref += [f'{idx} 0 R', '4 0 R']

    #f'{root} 0 obj << /Type /Catalog  /Pages {pagesobj} 0 R >> endobj',
    #f'{pagesobj} 0 obj <</Type /Pages  /Kids [{array}] ' +
    #f'/Count {count}  /MediaBox [0 0 595 12420] >> endobj'

    n = len(obj)

    def acc(u: List[int], d: List[int]) -> List[int]:
        u += d
        return d

    used: List[int] = []

    pages: List[int] = []

    pages.append(printpage(1, obj, [20, 14], acc(used, [
        20,
    ]), []))
    k = 60
    pages.append(printpage(2, obj, [], acc(used, [
        2, 6, 4, 41, 11, 12,
        9, 8, 1, 3, 5, 7,
        14,
        *range(30, 40),
        *range(42, k),
    ]), []))
    k2 = 114
    pages.append(printpage(3, obj, [], acc(used, [
        *range(k, k2),
    ]), []))
    pages.append(printpage(4, obj, [], acc(used, [
        *range(k2, 152),
        *range(153, 163),
    ]), []))
    k3 = 207
    pages.append(printpage(5, obj, [], acc(used, [
        *({*range(163, k3)} - set(pages)),
    ]), []))
    k4 = 248
    pages.append(printpage(6, obj, [], acc(used, [
        *({*range(k3, k4)} - set(pages)),
    ]), []))
    k5 = 289
    pages.append(printpage(7, obj, [], acc(used, [
        *range(k4, k5),
    ]), []))
    pages.append(printpage(8, obj, [], acc(used, [
       *range(k5, 332),  # n
    ]), []))
    pages.append(printpage(9, obj, [], acc(used, []), xref))

    for line in layout(pages, len(obj) + len(pages)):
        print(line)

    print()

    # temp:
    for i in {*range(1, n + 1)} - set(used) - set(pages):
        printdef(obj, i)
    for i in range(idx - xrefs + 1, idx + 1):
        printdef(obj, i)


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


def updatelines(generatedlines: List[str], generatedline: str, m: int) -> List[str]:
    reallen = streamnum(len(generatedline) + 2)
    pattern = f'150 0 R 2 0 R 24 0 R {m} 0 R 9 0 R'  # see getdefstreamof(50
    generatedlines += [generatedline]
    all = ' '.join(generatedlines)
    all = all.replace(pattern, ' '.join(reallen) + f' 24 0 R {m} 0 R 9 0 R')
    lines = []
    idx = 0
    for i, line in enumerate(generatedlines):
        n = len(line)
        lines.append(all[idx:idx + n])
        idx += n + 1
    return lines


# PAGE                       RENDER ORDER
# head                       1
# obj defs                   2
# generated obj defs         A  <--,
# obj /Type /Page            B     |
# stream (head, obj defs)    B     |
# generated stream           C  <--+- two lists
# endobj                     D
def printpage(num: int, obj: Dict[int, str], head: List[int], defs: List[int], xref: List[str]) -> int:
    for i in head:
        print(obj[i][1:-1])
    for i in defs:
        printdef(obj, i)
    stream = []
    for i in head:
        stream += [f'{i} 0 R', '4 0 R']
    for i in defs:
        stream += getdefstream(obj, i)

    n = 1 + sorted(obj.keys())[-1]
    pageobj = n
    obj[n] = 'page'  # placeholder

    streamhead = stream  # static beginnings
    streamneck = []  # generated obj defs
    streambody = []  # page obj
    streamlegs = []  # generated stream
    streamtail = []  # endobj

    # page:
    for c in str(n):
        streambody += [f'3{c} 0 R', '2 0 R']
    parent = 16
    begin = 17
    if num == 1:
        parent = 13
        begin = 22
    elif len(xref) > 0:
        parent = 18
        begin = 29
    streambody += [f'{parent} 0 R', '4 0 R', f'{begin} 0 R', '4 0 R']

    lines: List[str] = []

    m = n
    prev = -1
    final = False
    while True:
        streamlegs = []
        for i in range(pageobj + 1, m + 1):
            streamlegs += [f'{i} 0 R', '4 0 R']
        selflinedef = getdefstreamof(50, m + 1)  # placeholder, see updatelines
        streamneck += selflinedef
        streamtail = [f'{m + 1} 0 R', '4 0 R', '21 0 R', '4 0 R'] + xref
        stream = streamhead + streamneck + streambody + streamlegs + streamtail
        generatedlines, generateddefstrm, streamrest = dostream(n + 1, stream)
        m = n + len(generatedlines)
        streamneck = generateddefstrm
        if len(generatedlines) == prev:
            if final:
                break
            else:
                final = True
        prev = len(generatedlines)

    generatedline, generateddefstrm, _ = dostream(m, streamrest, userest=True)
    generatedlines = updatelines(generatedlines, generatedline[0], m + 1)

    for i, line in enumerate(generatedlines):
        leng = len(line)
        if i == len(generatedlines) - 1:
            obj[n + 1 + i] = f'({line})'
        elif leng < 74:
            raise Exception(f'unexpected length: {leng}')
        elif leng < 80:
            obj[n + 1 + i] = f'({line}' + ' ' * (leng - len(line)) + ')'
        else:
            obj[n + 1 + i] = f'({line}' + ' ' * (80 - 2 - len(line)) + ')'

    del obj[n]
    for i in [j for j in sorted(obj.keys()) if j > n]:
        printdef(obj, i)

    lines.append('{}{}'.format(n, obj[parent][1:-1]))
    lines.append(obj[begin][1:-1])
    for line in generatedlines:
        lines.append(line)
    lines.append(obj[21][1:-1])

    for i in lines:
        print(i)

    return n


def layout(page: List[int], m) -> List[str]:
    root = m
    pagesroot = m + 1
    pagesobj1 = m + 2
    pagesobj2 = m + 3
    pagesobj3 = m + 4
    array = ' '.join([f'{p} 0 R' for p in page[1:-1]])
    count = len(page)
    return [
        f'{root} 0 obj << /Type /Catalog /Pages {pagesroot} 0 R >> endobj',

        f'{pagesroot} 0 obj <</Type /Pages /Kids [{pagesobj1} 0 R {pagesobj2} 0 R {pagesobj3} 0 R] ' +
        f'/Count {count} >> endobj',

        f'{pagesobj1} 0 obj <</Type /Pages /Kids [{page[0]} 0 R] ' +
        f'/Count 1 /MediaBox [0 0 595 842] >> endobj',

        f'{pagesobj2} 0 obj <</Type /Pages /Kids [{array}] ' +
        f'/Count {count-2} /MediaBox [0 0 595 14400] >> endobj',

        f'{pagesobj3} 0 obj <</Type /Pages /Kids [{page[-1]} 0 R] ' +
        f'/Count 1 /MediaBox [0 0 595 {pageheight}] >> endobj',
    ]


def dostream(n: int, stream: List[str], userest=False) -> Tuple[List[str], List[str], List[str]]:
    stream = ' '.join(stream).split(' ')
    lines = []
    defs = []
    while True:
        tail = []
        while True:
            if len(' '.join(stream)) <= 78 and not userest:
                break
            for i in range(len(stream) + 1):
                if len(' '.join(stream[0: i])) > 78 or userest and len(' '.join(stream[0: i])) <= 78:
                    if userest:
                        line = ' '.join(stream)
                    else:
                        line = ' '.join(stream[0:i - 1])
                    lines.append(line)
                    stream = stream[i - 1:]
                    size = 80
                    leng = len(line)
                    if leng < 74 and not userest:
                        raise Exception(f'unexpected length: {leng}')
                    if leng < 80:
                        size = leng + 2
                    defs += getdefstreamof(size, n)
                    tail += [n]
                    n += 1
                    break
            if userest:
                stream = []
                break
        if len(tail) == 0:
            break
        if userest:
            break
    return lines, defs, stream


def getdefstream(obj: Dict[int, str], num: int) -> List[str]:
    size = len(obj[num])

    return getdefstreamof(size, num, stringobj(obj, num))


def getdefstreamof(size: int, num: int, strobj: int = 0) -> List[str]:
    if num in obj and obj[num] == r'(\\)':  # 41
        lst = streamnum(num)
        # obj[6] = r'( 0 obj << /Length )'
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        # obj[24] = r'( >> stream) Tj T* (\050) Tj'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        lst += ['24 0 R', f'{num} 0 R', '2 0 R', f'{num} 0 R', '9 0 R']
        return lst
    if num == 9:
        lst = streamnum(num)
        # obj[6] = r'( 0 obj << /Length )'
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        # obj[26] = r'( >> stream) Tj T*'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        # obj[48] = r'(Tj )'  # obj 9 str 1
        # obj[49] = r'( Tj T* (endstream endobj) Tj T*)'  # obj 9 str 2
        # obj[50] = r'(\050)'
        # obj[51] = r'(\051)'
        # obj[len(obj)] = r'(\\)'  # 41
        # obj[27] = r'Tj T* (endstream endobj) Tj T*'
        lst += ['26 0 R', '48 0 R', '2 0 R', '50 0 R', '2 0 R', '41 0 R', '2 0 R',
                '30 0 R', '2 0 R', '35 0 R', '2 0 R', '31 0 R', '2 0 R',
                '51 0 R', '2 0 R', '49 0 R', '27 0 R']
        return lst
    if num == 50:
        lst = streamnum(num)
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        lst += ['24 0 R', '41 0 R', '2 0 R', '30 0 R', '2 0 R', '35 0 R', '2 0 R', '30 0 R', '9 0 R']
        return lst
    if num == 51:
        lst = streamnum(num)
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        lst += ['24 0 R', '41 0 R', '2 0 R', '30 0 R', '2 0 R', '35 0 R', '2 0 R', '31 0 R', '9 0 R']
        return lst
    if num == 8:
        # obj[8] = r'Tj ( 0 obj << /Length 80 >> stream) Tj T* (\050) Tj'
        lst = streamnum(num)
        # obj[6] = r'( 0 obj << /Length )'
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        # obj[26] = r'( >> stream) Tj T*'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        # obj[27] = r'Tj T* (endstream endobj) Tj T*'
        # obj[44] = r'( 0 obj << /Length )'  # obj 8 str part 2
        # obj[45] = r'( >> stream)'  # obj 8 str part 3
        # obj[46] = r'( Tj T* )'  # obj 8 str part 4
        # obj[47] = r'( Tj'  # obj 8 str part 5
        # obj[48] = r'(Tj )'  # obj 9 str part 1, obj 8 str part 1
        lst += ['26 0 R',
                '48 0 R', '2 0 R',  # Tj
                '50 0 R', '2 0 R',  # (
                '44 0 R', '2 0 R',  # 0 obj << / Length
                '38 0 R', '2 0 R', '30 0 R', '2 0 R',  # 80
                '45 0 R', '2 0 R',  # >> stream
                '51 0 R', '2 0 R',  # )
                '46 0 R', '2 0 R',  # Tj T*
                '50 0 R', '2 0 R', '41 0 R', '2 0 R', '30 0 R', '2 0 R', '35 0 R', '2 0 R', '30 0 R', '2 0 R', '51 0 R',
                '2 0 R',
                '47 0 R',  # Tj
                '27 0 R']
        return lst
    if num == 1:  # obj[1] = r'Tj ( 0 obj << /Length 79 >> stream) Tj T* (\050) Tj'
        lst = streamnum(num)
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        lst += ['26 0 R', '48 0 R', '2 0 R', '50 0 R', '2 0 R', '44 0 R', '2 0 R', '37 0 R', '2 0 R', '39 0 R', '2 0 R',
                '45 0 R', '2 0 R', '51 0 R', '2 0 R', '46 0 R', '2 0 R', '50 0 R', '2 0 R', '41 0 R', '2 0 R',
                '30 0 R', '2 0 R', '35 0 R', '2 0 R', '30 0 R', '2 0 R', '51 0 R', '2 0 R', '47 0 R', '27 0 R']
        return lst
    if num == 3:  # 'Tj ( 0 obj << /Length 78 >> stream) Tj T* (\050) Tj'
        lst = streamnum(num)
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        lst += ['26 0 R', '48 0 R', '2 0 R', '50 0 R', '2 0 R', '44 0 R', '2 0 R', '37 0 R', '2 0 R', '38 0 R', '2 0 R',
                '45 0 R', '2 0 R', '51 0 R', '2 0 R', '46 0 R', '2 0 R', '50 0 R', '2 0 R', '41 0 R', '2 0 R',
                '30 0 R', '2 0 R', '35 0 R', '2 0 R', '30 0 R', '2 0 R', '51 0 R', '2 0 R', '47 0 R', '27 0 R']
        return lst
    if num == 5:  # 'Tj ( 0 obj << /Length 77 >> stream) Tj T* (\050) Tj'
        lst = streamnum(num)
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        lst += ['26 0 R', '48 0 R', '2 0 R', '50 0 R', '2 0 R', '44 0 R', '2 0 R', '37 0 R', '2 0 R', '37 0 R', '2 0 R',
                '45 0 R', '2 0 R', '51 0 R', '2 0 R', '46 0 R', '2 0 R', '50 0 R', '2 0 R', '41 0 R', '2 0 R',
                '30 0 R', '2 0 R', '35 0 R', '2 0 R', '30 0 R', '2 0 R', '51 0 R', '2 0 R', '47 0 R', '27 0 R']
        return lst
    if num == 7:  # 'Tj ( 0 obj << /Length 76 >> stream) Tj T* (\050) Tj'
        lst = streamnum(num)
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(len(obj[num]))
        lst += ['26 0 R', '48 0 R', '2 0 R', '50 0 R', '2 0 R', '44 0 R', '2 0 R', '37 0 R', '2 0 R', '36 0 R', '2 0 R',
                '45 0 R', '2 0 R', '51 0 R', '2 0 R', '46 0 R', '2 0 R', '50 0 R', '2 0 R', '41 0 R', '2 0 R',
                '30 0 R', '2 0 R', '35 0 R', '2 0 R', '30 0 R', '2 0 R', '51 0 R', '2 0 R', '47 0 R', '27 0 R']
        return lst

    if size == 80:
        lst = []
        lst += streamnum(num)
        lst = lst[:-1]
        # obj[8] = r'Tj ( 0 obj << /Length 80 >> stream) Tj T* (\050) Tj'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        lst += ['8 0 R', f'{num} 0 R', '9 0 R']
        return lst
    elif size == 79:
        lst = []
        lst += streamnum(num)
        lst = lst[:-1]
        # obj[1] = r'Tj ( 0 obj << /Length 79 >> stream) Tj T* (\050) Tj'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        lst += ['1 0 R', f'{num} 0 R', '9 0 R']
        return lst
    elif size == 78:
        lst = []
        lst += streamnum(num)
        lst = lst[:-1]
        # obj[3] = r'Tj ( 0 obj << /Length 78 >> stream) Tj T* (\050) Tj'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        lst += ['3 0 R', f'{num} 0 R', '9 0 R']
        return lst
    elif size == 77:
        lst = []
        lst += streamnum(num)
        lst = lst[:-1]
        # obj[5] = r'Tj ( 0 obj << /Length 77 >> stream) Tj T* (\050) Tj'
        # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
        lst += ['5 0 R', f'{num} 0 R', '9 0 R']
        return lst
    elif size == 76:
        lst = []
        lst += streamnum(num)
        lst = lst[:-1]
        lst += ['7 0 R', f'{num} 0 R', '9 0 R']
        return lst
    else:
        lst = []
        lst += streamnum(num)
        # obj[6] = r'( 0 obj << /Length )'
        lst += ['6 0 R', '2 0 R']
        lst += streamnum(size)
        if strobj == 0:
            # obj[24] = r'( >> stream) Tj T* (\050) Tj'
            # obj[9] = r'Tj (\051) Tj T* (endstream endobj) Tj T*'
            lst += [f'24 0 R', f'{num} 0 R', '9 0 R']
        else:
            # obj[26] = r'( >> stream) Tj T*'
            # obj[27] = r'Tj T* (endstream endobj) Tj T*'
            lst += ['26 0 R', f'{strobj} 0 R', '27 0 R']
        return lst


def streamnum(n: int) -> List[str]:
    lst = []
    s = str(n)
    for i, o in obj.items():
        if o == f'({s})':
            return [f'{i} 0 R', '2 0 R']

    if len(s) > 1:
        prefix = f'({s[0:2]})'
        for i, o in obj.items():
            if o == prefix:
                lst += [f'{i} 0 R', '2 0 R']
                s = s[2:]
                break

    tail = []
    if len(s) > 1:
        suffix = f'({s[-2:]})'
        for i, o in obj.items():
            if o == suffix:
                tail += [f'{i} 0 R', '2 0 R']
                s = s[:-2]
                break

    for c in s:
        lst += [f'3{c} 0 R', '2 0 R']
    lst += tail
    return lst


# prints obj definition, such as:
# 20 0 obj << /Length 10 >> stream
# (%PDF-1.4)
# endstream endobj
def printdef(obj: Dict[int, str], num: int) -> None:
    if len(obj[num]) == 80:
        print(f'{num} 0 obj << /Length 80 >> stream')
    elif len(obj[num]) == 79:
        print(f'{num} 0 obj << /Length 79 >> stream')
    elif len(obj[num]) == 78:
        print(f'{num} 0 obj << /Length 78 >> stream')
    else:
        # obj[6] = r'( 0 obj << /Length )'
        print(f'{num}' + obj[6][1:-1] + str(len(obj[num])) + ' >> stream')
    print(obj[num])
    print('endstream endobj')


def stringobj(obj: Dict[int, str], n: int) -> int:
    if obj[n].startswith("("):
        return 0
    if n in {9, 8, 1, 3, 5, 7}:
        return 0
    for i, o in obj.items():
        if o == '({})'.format(obj[n]):
            return i
    raise Exception(f'no str obj for {n}')


if __name__ == '__main__':
    main()
