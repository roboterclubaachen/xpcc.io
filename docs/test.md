# test

Footnotes[^1] have a label[^2] and the footnote's content.

[^1]: This is a footnote content.
[^2]: A footnote on the label: "2".


First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

%%\makeatletter
\renewcommand*\env@matrix[1][*\c@MaxMatrixCols c]{%
  \hskip -\arraycolsep
  \let\@ifnextchar\new@ifnextchar
  \array{#1}}
\makeatother%%

When $a \neq 0$ and $\min_1(4x + e^4)$ and therefore $\|F(x^0) + F'(x^0)(x - x^0)\|_2 \rightarrow \min$.

<center>$$[A | b]^{(0)} = \begin{pmatrix}[cc|c]
2 & 2 & 2 \\
1 & 1 & 1 \\
2 & 3 & 4 \\
4 & 0 & 0
\end{pmatrix}$$</center>

blasdfa

$$\alpha_1 = \sqrt{2^2 + 1^2 + 2^2 + 4^2} = \sqrt{25} = 5$$

$$\rightarrow \quad v_1^T = \begin{pmatrix}
7 & 1 & 2 & 4
\end{pmatrix}\quad \rightarrow \quad \beta_1 = \frac{2}{7^2 + 1^2 + 2^2 + 4^2} = \frac{2}{70} = \frac{1}{35}$$

$$h_1 = v_1^T[A|b]^{(0)} = \begin{pmatrix}[cc|c]
35 & 21 & 21
\end{pmatrix}$$

$$r_1 = \beta_1 v_1 = \begin{pmatrix}
7/35 \\
1/35 \\
2/35 \\
4/35
\end{pmatrix}$$

$$H_1 = r_1 h_1 = \begin{pmatrix}[cc|c]
7 & 21/5 & 21/5 \\
1 & 3/5 & 3/5 \\
2 & 6/5 & 6/5 \\
4 & 12/5 & 12/5
\end{pmatrix}\quad \rightarrow \quad
[A|b]^{(1)} = \begin{pmatrix}[cc|c]
-5 & -11/5 & -11/5 \\
0 & 2/5 & 2/5 \\
0 & 9/5 & 9/5 \\
0 & -12/5 & -12/5
\end{pmatrix}$$

$$\alpha_2 = \sqrt{(2/5)^2 + (9/5)^2 + (-12/5)^2} = \frac{\sqrt{229}}{5} \approx 3.027$$

$$\rightarrow v_2^T = \begin{pmatrix}
3.427 & 9/5 & -12/5
\end{pmatrix}$$

$$[A|b]^{(2)} = \begin{pmatrix}[cc|c]
5 & 11/5 & 11/5 \\
0 & -3.027 & -3.027 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{pmatrix}$$

$$ \Rightarrow x^T = \begin{pmatrix}
0 & 1
\end{pmatrix}$$

The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium


Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

[link](http://example.com){: class="foo bar" title="Some title!" }
