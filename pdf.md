# Whitespace

## Syntax — Lexical Conventions

> The PDF character set is divided into three classes, called regular, delimiter, and white-space characters. This
> classification determines the grouping of characters into tokens. The rules defined in this sub-clause apply to
> all characters in the file except within strings, streams, and comments.
> 
> [...]
> 
> All white-space characters are equivalent, except in comments, strings, and streams. In all other
> contexts, PDF treats any sequence of consecutive white-space characters as one character.

An example can be seen in [this blog post](https://blog.idrsolutions.com/2011/05/understanding-the-pdf-file-format-%E2%80%93-carriage-returns-spaces-and-other-gaps/).

## Syntax - Name Objects & Dictionary Objects

> A slash character (/) introduces a name. The slash is not part of the name itself [...]
> There can be no white-space characters between the slash and the first
> character in the name. The name may include any regular characters, but not
> delimiter or white-space characters 

> The first element of each entry is the key and the second
> element is the value. The key must be a name

> A dictionary is written as a sequence of key-value pairs enclosed in double angle brackets (<<...>>)

## Syntax — Indirect Objects

> The definition of an indirect object in a PDF file shall consist of its object number and generation number
> (separated by white space), followed by the value of the object bracketed between the keywords obj and
> endobj.

## Syntax — Stream Objects

> A stream shall consist of a dictionary followed by zero or more bytes bracketed between the keywords stream
> (followed by newline) and endstream [...]
> 
> The keyword stream that follows the stream dictionary shall be followed by an end-of-line marker
> consisting of either a CARRIAGE RETURN and a LINE FEED or just a LINE FEED [...]
> 
> The sequence of bytes that make up a stream lie between the end-of-line marker following the
> stream keyword and the endstream keyword; the stream dictionary specifies the exact number of bytes. There
> should be an end-of-line marker after the data and before endstream; this marker shall not be included in the
> stream length. There shall not be any extra bytes, other than white space, between endstream and endobj.

## Syntax — File Structure

> As a matter of convention, the tokens in a PDF file are arranged into lines; [...]. However, to increase compatibility with other applications that process PDF files, lines that are not part of stream object data are limited to no more than 255 characters

# Page Contents

> A content stream [...]. The value may be either a single stream or an array of streams.
> If the value is an array, the effect shall be as if all of the streams in the array were concatenated

# Content Streams

> The instructions are represented in the form of PDF objects, using the same object syntax as
> in the rest of the PDF document. However, whereas the document as a whole is a
> static, random-access data structure, the objects in the content stream are intended to be interpreted and acted upon sequentially.

> A content stream, after decoding with any specified filters, is interpreted accord-
> ing to the PDF syntax rules described in Section 3.1, “Lexical Conventions.” It
> consists of PDF objects denoting operands and operators.

> An operand is a direct object belonging to any of the basic PDF data types except
> a stream. Dictionaries are permitted as operands only by certain specific opera-
> tors. Indirect objects and object references are not permitted at all.

> An operator is a PDF keyword that specifies some action to be performed, such as
> painting a graphical shape on the page. An operator keyword is distinguished
> from a name object by the absence of an initial slash character (/). Operators are
> meaningful only inside a content stream.
 
# Object Streams

> Beginning with PDF 1.5, indirect objects may reside in object streams (see 7.5.7, "Object Streams"). They are
> referred to in the same way; however, their definition shall not include the keywords obj and endobj, and their
> generation number shall be zero.

> a stream object in which a sequence of indirect objects may be stored, as an alternative to
> their being stored at the outermost file level.



```
apt-get update
apt-get install python3-pdfminer  # pdf2txt
apt-get install poppler-utils  # pdftotext

#validate pdf file:
apt-get install ghostscript
gs -sDEVICE=pdfwrite -o file.pdf
```

