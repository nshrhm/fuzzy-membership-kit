# Theory notes

## 1. Fuzzy set and membership function

Let \(U\) be the universe of discourse.  A fuzzy set \(A\) on \(U\) is represented by a membership function

\[
\mu_A: U \rightarrow [0,1],
\]

where \(\mu_A(u)\) denotes the degree to which \(u \in U\) belongs to \(A\).  When \(U\) is a numerical scale, such as a VAS score, the membership function is not only a mapping into \([0,1]\); it also encodes the semantic relationship between distances on the universe scale and membership values.

## 2. Classical membership functions

### 2.1 Triangular function

For \(a < b < c\), the triangular membership function is

\[
\mu(u;a,b,c)=
\begin{cases}
0, & u \le a,\\
\dfrac{u-a}{b-a}, & a < u \le b,\\
1-\dfrac{u-b}{c-b}, & b < u < c,\\
0, & c \le u.
\end{cases}
\]

It is continuous but not differentiable at \(a\), \(b\), and \(c\).

### 2.2 Trapezoidal functions

A rising trapezoidal shoulder is

\[
\mu_R(u;c,d)=
\begin{cases}
0, & u \le c,\\
\dfrac{u-c}{d-c}, & c < u \le d,\\
1, & d < u.
\end{cases}
\]

A falling shoulder is \(\mu_F(u;a,b)=1-\mu_R(u;a,b)\).  A trapezoidal pi function with plateau \([b,c]\) is

\[
\mu_\Pi(u;a,b,c,d)=
\begin{cases}
0, & u \le a,\\
\dfrac{u-a}{b-a}, & a < u \le b,\\
1, & b < u \le c,\\
1-\dfrac{u-c}{d-c}, & c < u < d,\\
0, & d \le u.
\end{cases}
\]

### 2.3 Gaussian function

For center \(m\) and scale \(\sigma>0\),

\[
\mu_G(u;m,\sigma)=\exp\left[-\frac{(u-m)^2}{2\sigma^2}\right].
\]

This function is smooth and has peak membership 1.  Unlike a probability density, it is not normalized to integrate to 1.  A limitation is that it reaches neither exact 0 nor exact 1 over an interval.

## 3. Zadeh-style S, Z, and pi functions

For \(\ell < r\), the S function is the quadratic spline

\[
S(u;\ell,r)=
\begin{cases}
0, & u \le \ell,\\
2\left(\dfrac{u-\ell}{r-\ell}\right)^2, & \ell < u \le \dfrac{\ell+r}{2},\\
1-2\left(\dfrac{u-r}{r-\ell}\right)^2, & \dfrac{\ell+r}{2}<u\le r,\\
1, & r < u.
\end{cases}
\]

The corresponding Z function is

\[
Z(u;\ell,r)=1-S(u;\ell,r).
\]

The pi function is obtained by combining S and Z:

\[
\Pi(u;a,b,c,d)=
\begin{cases}
S(u;a,b), & u \le c,\\
Z(u;c,d), & c < u.
\end{cases}
\]

with \(a<b\le c<d\).  These functions are \(C^1\): the function and first derivative are continuous, although the second derivative is generally not continuous at the spline knots.

## 4. Sigmoid-composed S function

A recent concern in membership-function design is that equal differences in \(u\) need not imply equal semantic differences everywhere on the universe scale.  Near a focal value, adjacent values may need clearly distinguishable memberships, whereas far away from the focal value, adjacent values may reasonably be less distinguishable.

The implementation therefore includes a sigmoid-composed S family.  First define the logistic transformation

\[
f(u;\alpha,u_*)=\frac{1}{1+\exp[-\alpha(u-u_*)]},
\]

where \(u_*\) is the focal value and \(\alpha\) is a gain parameter.  Given an upper quantile \(q\in(0.5,1)\) and a far value \(u_q\), set

\[
\alpha = \frac{\log\{q/(1-q)\}}{u_q-u_*}.
\]

This gives \(f(u_*;\alpha,u_*)=0.5\) and \(f(u_q;\alpha,u_*)=q\).  With the lower quantile \(p=1-q\), the sigmoid-composed S membership is

\[
\mu_{CS}(u;u_*,u_q,q)=S\left(f(u;\alpha,u_*);p,q\right).
\]

For the default \(q=0.9\), membership is 0.5 at \(u_*\) and reaches 1 at \(u_q\).  The slope is large near \(u_*\) and becomes progressively smaller as \(u\) moves away from the focal region.  Because a smooth sigmoid is composed with a \(C^1\) S function, the resulting membership function is at least \(C^1\).

## 5. Sigmoid-composed Z and pi functions

The decreasing counterpart is

\[
\mu_{CZ}(u;u_*,u_q,q)=Z\left(f(u;\alpha,u_*);1-q,q\right).
\]

A two-sided pi-like membership can be defined as the minimum of a rising composed S side and a falling composed Z side:

\[
\mu_{C\Pi}(u)=\min\{\mu_{CS}^{(L)}(u),\mu_{CZ}^{(R)}(u)\}.
\]

This parameterization is useful when the central region should have high membership and the tails should become gradually less distinguishable.

## 6. Reporting recommendation

A paper should report the membership family and the full parameterization.  For example:

\[
\mu_A(u)=S\left(\frac{1}{1+\exp[-\alpha(u-50)]};0.1,0.9\right),\quad
\alpha=\frac{\log(0.9/0.1)}{90-50}.
\]

This sentence identifies the universe scale, focal value, far value, quantile convention, and spline thresholds.
